# -*- coding=utf-8 -*-

"""
    a simple sigmacloud sdk
"""

import os
import json
import base64
import requests
from utils import (SigmaAuth, get_file_md5_digest)

# 添加API_Key 和 API Secret
API_KEY = "9OBDWTunZHjw=="
API_SECRET = "53gIkatMpTyatAZBy4="
SERVER = "http://192.168.1.128:7070"


class API(object):

    def __init__(self):
        if len(API_KEY) == 0 or len(API_SECRET) == 0:
            print('\n' + '请在' + os.path.realpath(__file__) + '文件中填写正确的API_KEY和API_SECRET' + '\n')
            return
        self.key = API_KEY
        self.secret = API_SECRET
        self.server = SERVER
        # 用token验证身份和用key+secret验证身份二选一即可
        self.token = ""
        # self.auth = SigmaAuth(self.key, self.secret)

    def login(self, account_name, user_name, password):
        """登入"""
        print("登录...")
        encode_password = base64.urlsafe_b64encode(password)
        resource = "/login?account_name={}&user_name={}&password={}&force_new=False".format(
            account_name, user_name, encode_password)
        request_url = "{}{}".format(self.server, resource)
        try:
            response = requests.get(request_url)
            print(response.status_code, response.text)
            jsondata = json.loads(response.text)
            self.token = jsondata["data"]["user_info"]["token"]
            print("token：{}".format(self.token))
        except Exception as e:
            print(e)

    def logout(self):
        """登出"""
        print("账户登出...")
        resource = "/logout"
        request_url = "{}{}".format(self.server, resource)
        headers = {"Sigma-Token": self.token}
        try:
            response = requests.delete(request_url, headers=headers)
            print(response.status_code, response.text)
        except Exception as e:
            print(e)

    def upload_multi(self, groupname, pathname, dirname, quantity=1, overwrite=1, converted=1):
        """上传文件（夹）的主方法"""
        upload_id = self.upload_multi_init(groupname, dirname, quantity, overwrite, converted)
        for root, dirs, files in os.walk(pathname):
            for name in files:
                filename = os.path.join(root, name)
                ret = self.upload_multi_part(upload_id, filename)
                if 'store_id' in ret.keys():
                    return ret

    def upload_multi_init(self, groupname, dirname, quantity, overwrite, converted):
        """上传文件夹的初始化"""
        contents = {
            "dirname": dirname,
            "quantity": quantity,
            "overwrite": overwrite,
            "converted": converted
        }
        url = self.server + "/accounts/sigma/store/uploads/{}/".format(groupname)
        headers = {"Sigma-Token": self.token}
        response = requests.post(url, data=json.dumps(contents), headers=headers)
        # response = requests.post(url, data=json.dumps(contents), auth=self.auth)
        jsondata = json.loads(response.text)
        return jsondata["data"]["upload_id"]

    def path_split(self, filename):
        """Split filename and get dirname and basename."""
        _filename = "/" + filename if filename[0] != "/" else filename
        items = _filename.split("/")
        dirname = "/"
        if len(items[:-1]) != 1:
            dirname = "/".join(items[:-1])
        basename = items[-1]
        return (dirname, basename)

    def upload_multi_part(self, upload_id, filename):
        """上传单一文件"""
        print("开始上传文件：{}...".format(filename))
        _dirname, _filename = self.path_split(filename)
        resource = "/accounts/sigma/store/uploads/" + "{}/?upload_id={}".format(_filename, upload_id)
        print(resource)
        url = "{}{}".format(self.server, resource)
        headers = {
            "Sigma-Token": self.token,
            "Content-Length": str(os.path.getsize(filename)),
            "Content-MD5": get_file_md5_digest(filename)
        }
        with open(filename, "rb") as f:
            response = requests.put(url, data=f.read(), headers=headers)
            # response = requests.put(url, data=f.read(), auth=self.auth)
            return json.loads(response.text)

    def new_job(self, job_type, account_name, user_name, study_id, series_id,
                patient_id, format, filename, priority, type):
        """创建肺结节检测任务"""
        print("开始创建肺结节检测任务...")
        request_data = {
            'account_name': account_name,
            'user_name': user_name,
            'study_id': study_id,
            'series_id': series_id,
            'patient_id': patient_id,
            'format': format,
            'filename': filename,
            'job_type': job_type,
            'priority': priority,
            'type': type
        }
        resource = "/accounts/sigma/jobs/"
        url = "{}{}".format(self.server, resource)
        headers = {"Sigma-Token": self.token}
        response = requests.post(url=url, data=json.dumps(request_data), headers=headers)
        # response = requests.post(url=url, data=json.dumps(request_data), auth=self.auth)
        print(response.status_code, response.text)

    def upload_followup(self, groupname_0, groupname_1, pathname_0, pathname_1, quantity_0, quantity_1):
        """上传两组dcm图像，用于计算followup任务"""
        print("开始上传随访图像...")
        self.upload_multi(groupname_0, pathname_0, "/", quantity_0)
        self.upload_multi(groupname_1, pathname_1, "/", quantity_1)

    def new_followup_job(self, job_type, account_name, user_name, patient_id, study_id,
                         series_id_0, series_id_1, filename_0, filename_1, type, format):
        """创建followup任务"""
        print("开始创建随访计算任务...")
        request_data = {
            'priority': '2',
            'job_type': job_type,
            't0': {
                'account_name': account_name,
                'user_name': user_name,
                'format': format,
                'patient_id': patient_id,
                'series_id': series_id_0,
                'study_id': study_id,
                'filename': filename_0,
                'type': type
            },
            't1': {
                'account_name': account_name,
                'user_name': user_name,
                'format': format,
                'patient_id': patient_id,
                'series_id': series_id_1,
                'study_id': study_id,
                'filename': filename_1,
                'type': type
            }
        }
        resource = "/accounts/sigma/jobs/"
        url = "{}{}".format(self.server, resource)
        headers = {"Sigma-Token": self.token}
        response = requests.post(url=url, data=json.dumps(request_data), headers=headers)
        # response = requests.post(url=url, data=json.dumps(request_data), auth=self.auth)
        print(response.status_code, response.text)

    def download_file(self, pathname, filename, group_name=None, username=None):
        """下载文件"""
        print("开始下载文件...")
        resource = "/accounts/sigma/store/downloads/" + "?filename={}".format(filename)
        url = "{}{}".format(self.server, resource)
        if group_name:
            url += "&group_name={}".format(group_name)
        if username:
            url += "&owner={}".format(username)
        headers = {"Sigma-Token": self.token}
        response = requests.get(url, headers=headers)
        print(response.status_code, response.text)
        with open(pathname, "wb") as w:
            w.write(response.content)

    def get_studylist(self):
        """获取study列表"""
        print("开始获取studylist信息...")
        resource = "/accounts/sigma/jobs/studylist/"
        url = "{}{}".format(self.server, resource)
        headers = {"Sigma-Token": self.token}
        response = requests.get(url, headers=headers)
        print(response.status_code, response.text)

    def list_jobs(self, unique_id):
        """获取unique_id对应的job信息"""
        print("开始罗列job信息...")
        resource = "/accounts/sigma/jobs/list/?unique_id=" + unique_id
        url = "{}{}".format(self.server, resource)
        headers = {"Sigma-Token": self.token}
        response = requests.get(url, headers=headers)
        print(response.status_code, response.text)

