# **SigmaCloud DR帮助文档**

### 关于login/logout的操作
|API|描述| 
|:--|:--|
|Login|登入，会返回token,用于鉴权|
|Logout|登出|

### 关于store的操作
|API|描述| 
|:--|:--|
|Upload|上传文件，上传一组dcm分2步：1.先调用POST方法，2.调用PUT方法|
|DownloadFile|下载文件，用于下载json文件（ai检测结果）|

### 关于job的操作  
|API|描述|
|:--|:--|
|NewJob|创建job|
|GetJob|获取job信息|
|ListJobs|获取job信息列表|
|GetJobStudyList|获取studylist|


### 关于login/logout的操作
#### Login
#####  描述
```
    用户登入
```
##### 调用url
```
    https://api.12sigma.ai/login
```
##### 调用方法
```
    GET
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|

##### 请求参数
|参数名|类型|是否必选|参数说明| 
|:--|:--|:--|:--|
|account_name|字符串|必选|账户名|
|user_name|字符串|必选|用户名|
|password|字符串|必选|密码| 
|force_new|字符串|必选|是否强制登录，踢session，默认值"False"|

##### 返回值示例
###### 请求成功返回示例
```
{
    "url": "",
    "message": "User login successfully.",
    "message_chs": "用户登录成功.",
    "data": {
        "user_info": {
            "account_id": "5c23a24a411a",
            "password": "1cb4c12ef1dbb18503347623aaf5b3d442fcac",
            "description": "12sigma",
            "access_key": "9OBDzzzzXHjw==",
            "display_name": "test",
            "name": "test",
            "mobile": "18888888888",
            "token": "eyJhbm6XjGncYzKw_gHP_k=",
            "user_level": "12sigma",
            "secret_key": "53gIkatMIatAZBy4=",
            "_id": "5c23a24ae411e",
            "type": "User",
            "email": "test@12sigma.ai",
            "sys_user": false
        },
        "user_name": "test",
        "account_name": "sigma"
    },
    "error": {
        "message": "",
        "code": "",
        "message_chs": ""
    }
}   

```
##### 请求失败返回示例
```
     {"message": "", 
      "message_chs": "", 
       "data": {}, "url": "",
       "error": {"code": e.error_code_name, 
                     "message": e.message,
                     "message_chs": e.message_chs}}

```

#### Logout
#####  描述
```
    用户登出
```
##### 调用url
```
    https://api.12sigma.ai/logout
```
##### 调用方法
```
    DELETE
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|必选|登录接口返回的token信息|

##### 返回值示例
###### 请求成功返回示例
```
{
	"url": "",
	"message": "User logout successfully!",
	"message_chs": "用户登出成功",
	"data": {},
	"error": {
		"message": "",
		"code": "",
		"message_chs": ""
	}
}

```

### 关于store的操作  
#### Upload（POST）
#####  描述
```
   每个DR检测，需要一张dcm文件，上传第一步是调用POST方法，获得upload_id
```
##### 文件要求
```
    文件格式：dcm
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/store/uploads/<groupname>/
    提示：这个groupname要求是series_id
```
##### 调用方法
```
    POST
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|参数名|是否必选|参数说明| 
|Sigma-Token|是|登录接口返回的token信息|


##### 请求参数
|参数名|类型|是否必选|参数说明| 
|:--|:--|:--|:--|
|groupname|字符串|必选|要求是series_id,来标识这组dcm图|
|quantity|字符串|必选|要求是这个series的dcm实际总数，DR检测一般写“1”|
|converted|字符串|必选|是否dcm转nii，需要写"1"|
|overwrite|字符串|必选|是否覆盖同名文件，需要写"1"|


##### 请求数据范例
```
    groupname=series_id,
    quantity=1,
    overwrite=1,
    converted=1
```


##### 返回值示例
###### 请求成功返回示例
```
{
	"url": "",
	"message": "Initial multi upload",
	"message_chs": "初始化分块上传",
	"data": {
		"upload_id": "54f49e2435e211e9980aac1f6b91e556_182"
	},
	"error": {
		"message": "",
		"code": "",
		"message_chs": ""
	}
}

```

#### Upload（PUT）
#####  描述
```
    Upload用于上传单个dcm文件，每个PUT请求上传一张dcm
```
##### 文件要求
```
    文件格式：dcm
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/store/uploads/<filename>/
```
##### 调用方法
```
    PUT
```

##### 请求Header
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|必选|登录接口返回的token信息|
|Content-Length|必选|文件大小|
|Content-MD5|必选|文件的md5值|

##### 请求参数
|参数名|类型|是否必选|参数说明| 
|:--|:--|:--|:--|
|filename|字符串|必选|文件名|
|upload_id|字符串|必选|此值为POST上传返回的upload_id|


##### 返回值示例
###### 请求成功返回示例
```
{
   'url': '', 
   'message': 'Upload C:\\Users\\12sigma\\Desktop\\1961551\\a_0136.dcm succeed', 
   'message_chs': '文件 C:\\Users\\12sigma\\Desktop\\1961551\\a_0136.dcm 上传成功', 
   'data': {
	        	'upload_id': 'eef5653a35e211e9980aac1f6b91e556_182'
    }, 
   'error': {
	        	'message': '',
		        'code': '',
		        'message_chs': ''
	}
}

```


#### DownloadFile
##### 描述
```
    DownloadFile用于下载文件，一般是计算结果json文件，或者下载单张dcm文件
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/store/downloads/
```
##### 调用方法
```
    GET
```
##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|

##### 请求参数
|名称|类型|是否必须|描述| 
|:--|:--|:--|:--|
|filename|字符串|必选|文件名|


##### 返回值示例
###### 请求成功返回示例
```
返回文件流
```

### 关于job的操作
#### NewJob
##### 描述
```
    NewJob用于创建Dr结节检测
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/jobs/"
```
##### 调用方法
```
    POST
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|

##### 请求参数
|名称|类型|是否必须|描述| 
|:--|:--|:--|:--|
|account_name|字符串|是|账户名|
|user_name|字符串|是|用户名|
|study_id|字符串|是||
|series_id|字符串|是|数据全局唯一ID|
|patient_id|字符串|是|患者id|
|format|字符串|是|数据文件类型，默认传“dcm”|
|filename|字符串|是|数据文件名称，例如“xxxx.dcm”|
|job_type|字符串|是|计算job的类型，例如：DR检测（lung_dr_detection）|
|priority|字符串|是|优先级，默认传 2|
|type|字符串|是|默认写“file”|
|notify|字符串|否|是否在计算成功后通知调用方，"1"表示通知，"0"表示不通知|
|notify_url|字符串|否|如果notify参数是"1"，则此参数需要填写，例如："http://xxx/"|
|notify_info|字典|否|如果有额外信息需要传入，可以写在这里|

##### 请求数据json范例
```
    request_data = {
        'account_name': 'accunt_1',
        'user_name': 'user_1',
        'study_id': '11111.11111.11111',
        'series_id': '222.222.222',
        'patient_id': '622747',
        'format': 'dcm',
        'filename': '222.222.222.dcm',
        'job_type': 'lung_dr_detection',
        'priority': '2',
        'type': 'file'
    }
```

##### 返回值示例
###### 请求成功返回示例
```
{
	"url": "",
	"message": "new job successfully!",
	"message_chs": "新建作业成功！",
	"data": {
		"job_id": "job-bca0e97a-253d-11e9-980a-ac1f6b91e556"
	},
	"error": {
		"message": "",
		"code": "",
		"message_chs": ""
	}
}
```
###### 请求失败返回示例
```
{
	"url": "",
	"message": "",
	"message_chs": "",
	"data": {},
	"error": {
		"message": "Invalid input, the input job type is invalid!",
		"code": "InvalidParameter",
		"message_chs": "输入错误，输入的作业类型（job_type）参数非法!"
	}
}
```

#### GetJob
##### 描述
```
    获取job信息
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/jobs/<job_id>/
```
##### 调用方法
```
    GET
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|


##### 请求参数
|名称|类型|是否必须|描述| 
|:--|:--|:--|:--|
|job_id|字符串|是|拼接在url中|

##### 返回值示例
###### 请求成功返回示例
```
{
	"url": "",
	"message": "get job information successfully!",
	"message_chs": "获取作业信息成功!",
	"data": {
		"status": "success",
		"tasks": [{
			"status": "waiting",
			"timestamp": null,
			"task_id": "task-eb1248dc-2f54-11e9-980a-ac1f6b91e556"
		}],
		"job_id": "job-eb1243dc-2f54-11e9-980a-ac1f6b91e556",
		"end_ts": 1550037822.648161,
		"start_ts": 1550037738.013482,
		"user_name": "test",
		"account_name": "sigma"
	},
	"error": {
		"message": "",
		"code": "",
		"message_chs": ""
	}
}

```
###### 请求失败返回示例
```
{
	"url": "",
	"message": "",
	"message_chs": "",
	"data": {},
	"error": {
		"message": "An internal exception is raised, message: get job information failed, the job is not exist or deleted.",
		"code": "InternalServerError",
		"message_chs": "服务内部错误"
	}
}

```
#### ListJobs
##### 描述
```
    ListJobs用于获取作业列表
```
##### 调用url
```
    http://api.12sigma.ai/accounts/<res_account_name>/jobs/list/?unique_id=xxxxxx
```
##### 调用方法
```
    GET
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|

##### 请求参数
|参数名|类型|是否必选|参数说明| 
|:--|:--|:--|:--|
|unique_id|字符串|是|即series_id，序列号|

##### 返回值示例
###### 请求成功返回示例
```
{
	'url': '', 
	'message': 'list jobs successfully!', 
	'message_chs': '获取作业列表成功!', 
	'data': {
		'jobs': [
		{
			'status': 'success',
			'job_id': '5c738d2be05cc13ee089c4f0',
			'job_type': 'lung_dr_detection',
			'end_ts': 1551076735.489463,
			'start_ts': 1551076651.455676,
			'patient_id': '622747',
			'series_id': '1.3.12.2.1107.5.1.4.1336.30000014091500302045300006765',
			'study_id': '1.2.276.0.37.1.88.200512.2667220',
			'user_name': 'test',
			'account_name': 'sigma'
		},
		......
		],
		'total_number': 4
	}, 
	'error': {
		'message': u '',
		'code': u '',
		'message_chs': u ''
	}
}
```

#### GetStudylist
##### 描述
```
    GetStudylist用于获取患者的Studylist信息
```
##### 调用url
```
    https://api.12sigma.ai/accounts/<res_account_name>/jobs/studylist/
```

##### 调用方法
```
    GET
```

##### 请求头
|Header名|是否必选|参数说明| 
|:--|:--|:--|
|Sigma-Token|是|登录接口返回的token信息|

##### 请求参数
|参数名|类型|是否必选|参数说明| 
|:--|:--|:--|:--|
|patient_id|字符串|否|患者id|
|patient_name|字符串|否|患者name|
|accession_number|字符串|否||
|study_id|字符串|否||
|study_description|字符串|否|study描述|
|study_start|字符串|否|开始日期，形如20190221|
|study_end|字符串|否|结束日期，形如20190221|
|start_time|字符串|否|开始时间的时间戳|
|end_time|字符串|否|结束时间的时间戳|
|job_type|字符串|否|job类型|

##### 返回值示例
###### 请求成功返回示例
```
{
	"url": "",
	"message": "list jobs successfully!",
	"message_chs": "\u83b7\u53d6\u4f5c\u4e1a\u5217\u8868\u6210\u529f!",
	"data": {
		"studies": [{
			"AccessionNumber": "1801200026",
			"account": "sigma",
			"StudyDate": "20180120",
			"series": {
				"1_2_840_113619_2_261_4_2147483647_1516461913_240563": {
					"Rows": 2012,
					"SeriesTime": "092513.000",
					"ContentDate": "20180120",
					"ProtocolName": "\u80f8\u90e8",
					"WindowCenter": [3238.0, 3238.0, 3238.0],
					"Columns": 2012,
					"SeriesDate": "20180120",
					"SeriesNumber": 10126,
					"ImageOrientationPatient": "",
					"SliceThickness": "",
					"AcquisitionNumber": "",
					"ConvolutionKernel": "",
					"Manufacturer": "\"GE Healthcare\"",
					"ModalitiesInStudy": "",
					"WindowWidth": [2561.0, 1920.0, 3841.0],
					"SeriesDescription": "Chest",
					"job": {
						"status": "success",
						"priority": 1,
						"job_type": "lung_dr_detection",
						"job_id": "5ca31952e05cc1013639756f"
					},
					"PatientPosition": "",
					"SpacingBetweenSlices": "",
					"ImageType": "['ORIGINAL', 'PRIMARY']",
					"SOPClassUID": "Digital X-Ray Image Storage - For Presentation",
					"BodyPartExamined": "CHEST",
					"FrameOfReferenceUID": "",
					"StationName": "Not Initialized",
					"SeriesInstanceUID": "1.2.840.113619.2.261.4.2147483647.1516461913.240563",
					"Modality": "DX",
					"quantity": 1
				}
			},
			"StudyDescription": "",
			"InstitutionName": "",
			"PatientBirthDate": "19930720",
			"PatientID": "P00152126",
			"PatientAge": 24,
			"PatientSex": "M",
			"StudyInstanceUID": "1.84.83.83.838485.20180120.202677",
			"StudyTime": "092509.000",
			"StudyID": "1",
			"PatientName": "",
			"job_type": ["lung_dr_detection"]
		}],
		"total_study_count": 1
	},
	"error": {
		"message": "",
		"code": "",
		"message_chs": ""
	}
}

```
###### 请求失败返回示例
```
{
	"url": "",
	"message": "",
	"message_chs": "",
	"data": {},
	"error": {
		"message": "list study failed!",
		"code": "ListStudyListError",
		"message_chs": ""
	}
}
```

##### 当前API特有的ERROR_MESSAGE
|HTTP状态码（status）|错误码（Error Code）|错误消息（Error Message）|描述（Description）| 
|:---|:---|:---|:---|
|500|ListStudyListError|list study failed, error!||

