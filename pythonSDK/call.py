# -*- coding=utf-8 -*-

import os
from PythonSDK.sigmacloud import API

# 以下是demo中用到的dicom图片资源，可根据需要替换
lung_det_path = os.path.dirname(os.path.abspath(__file__)) + "\\imgResource\\622747"
lung_followup_path_0 = os.path.dirname(os.path.abspath(__file__)) + "\\imgResource\\107434\\T0"
lung_followup_path_1 = os.path.dirname(os.path.abspath(__file__)) + "\\imgResource\\107434\\T1"
lung_unique_id = "1.3.12.2.1107.5.1.4.1336.30000014091500302045300006765"
t0 = "1.2.840.113654.2.55.22904755772537364426577602239104828910"
t1 = "1.2.840.113654.2.55.80716887202718212912842134755481869828"

# 初始化对象，进行api的调用工作
api = API()

# ----------------------------账户登录-------------------------------------
api.login("sigma", "test", '123456')


# ----------------------------肺结节检测部分--------------------------------
# 步骤一，上传dicom文件
upload_res = api.upload_multi(groupname=lung_unique_id,
                              pathname=lung_det_path,
                              dirname="/",
                              quantity=200)

# 步骤二，创建新job
api.new_job(job_type="lung_nodule_detection",
            account_name="sigma",
            user_name="test",
            study_id="1.2.276.0.37.1.88.200512.2667220",
            series_id=lung_unique_id,
            patient_id="622747",
            format="nii",
            filename=lung_unique_id + ".nii",
            priority="2",
            type="file")

# 步骤三，下载计算结果json文件
api.download_file(pathname=os.path.dirname(os.path.abspath(__file__)) + "\\" + lung_unique_id + ".json",
                  filename=lung_unique_id + ".json")


# ----------------------------肺结节随访检测部分----------------------------------
# 步骤一，上传dicom文件
api.upload_followup(groupname_0=t0,
                    groupname_1=t1,
                    pathname_0=lung_followup_path_0,
                    pathname_1=lung_followup_path_1,
                    quantity_0=134,
                    quantity_1=137)

# 步骤二，创建新job
api.new_followup_job(job_type="lung_nodule_followup",
                     account_name="sigma",
                     user_name="test",
                     patient_id="107434",
                     study_id="",
                     series_id_0=t0,
                     series_id_1=t1,
                     filename_0=t0 + ".nii",
                     filename_1=t1 + ".nii",
                     type="file",
                     format="nii")

# 步骤三，下载计算结果json文件
api.download_file(pathname=os.path.dirname(os.path.abspath(__file__)) + "\\" + t0 + "_" + t1 + "_followup_pair.json",
                  filename=t0 + "_" + t1 + "_followup_pair.json")


# 获取studylist
api.get_studylist()

# 获取job list
api.list_jobs(unique_id=lung_unique_id)

# 登出
api.logout()

