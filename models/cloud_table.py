import math
import requests

from typing import List, Dict, Optional
from retry import retry

from models.cloud_base import PostRecord, GetRecord
from config import settings
from utils.logs import init_logger_obj
log = init_logger_obj()


class CloudTable():
    """
    飞书多维表格- 飞书Api原生方法
    """
    fields = {}
    
    def __init__(self, app_token=settings.default_bitable_app_token, table_id=settings.default_bitable_table_id, GetRecordClass=Dict) -> None:
        self.header = self.get_headers()
        self.app_token = app_token
        self.table_id = table_id
        self.all_records = []
        self.email_userid_mapping = {
            "open_id": {},
            "union_id": {},
            "user_id": {},
        }
        self.GetRecordClass: Dict = GetRecordClass
        
    
    @retry(tries=3)
    def get_headers(self):
        # 用于发送消息的时候获取带有相关token的headers
        fs_get_token = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        data = {
            # 会议机器人机器人专属
            "app_id": settings.default_lark_app_id,
            "app_secret": settings.default_lark_app_secret,
        }
        headers = {
            "Content-Type": "application/json;charset=utf-8",
        }
        request = requests.post(url=fs_get_token, headers=headers, json=data)
        tenant_access_token = request.json()['tenant_access_token']
        headers["Authorization"] = f"Bearer {tenant_access_token}"
        return headers


    #! 多维表格记录相关Api
    @retry(tries=3)
    def get_user_userid(self, emails: List[str], user_id_type='open_id') -> Dict:
        """根据邮箱获取飞书的openId 并加载进对象变量中

        Args:
            emails (list): emails‘list

        Returns:
            dict: email's openid
        >>> _get_user_openid(["test@lark.cn", "good@lark.cn", "nobody@lark.cn"])
        {
            "test@lark.cn": "ou_xxxx",
            "good@lark.cn": "ou_yyyy",
        }
        >>> _get_user_openid(["nobody@lark.cn"])
        {}
        """
        # 避免重复查询飞书接口
        emails = [email for email in emails if email not in self.email_userid_mapping[user_id_type]]
        if emails:
            # 飞书一次只支持50个用户数据查询 所以要分次
            rq_times = math.ceil(len(emails)/50)
            # headers = self.get_headers()
            for i in range(rq_times):
                url = f"https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type={user_id_type}"
                payload = {
                    "emails": emails[50*i: 50*(i+1)]
                }
                response = requests.post(url, headers=self.header, json=payload)
                # email_openid_dict = {u.get('email'): u.get('user_id') for u in response.json()['data']['user_list'] if u.get('email') and u.get('user_id') is not None}
                for u in response.json()['data']['user_list']:
                    if u.get('email') and u.get('user_id'):
                        self.email_userid_mapping[user_id_type][u.get('email')] = u.get('user_id')
        return self.email_userid_mapping


    @retry(tries=3)
    def get_cloudfile_records(self, **extend_params) -> List:
        """获取所有的records

        Returns:
            list: records
        """
        self.all_records = []
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records?page_size=500"
        params = {
            "page_size": 500,
            "page_token": ""
        }
        # Add query records extend params
        for k, v in extend_params.items():
            params[k] = v

        while True:
            response = requests.get(url, headers=self.header, params=params)
            rd = response.json()['data']
            items = rd['items']
            if items:
                # 有可能第一次就是空查询
                self.all_records.extend(items)
            if rd.get('has_more'):
                params['page_token'] = rd['page_token']
            else:
                break
        return self.all_records


    @retry(tries=3)
    def update_cloudfile_records(self, records: List[Dict]):
        """更新records表

        Args:
            records (list): _description_
        Demo:
            records = [
            {
                "fields": {
                    "status": "running"
                },
                "record_id": "rec1"
            },
            {
                "fields": {
                    "status": "stopped"
                },
                "record_id": "rec2"
            }]
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/batch_update?user_id_type=open_id"
        # 飞书一次只支持500个数据的update 所以要分次
        rq_times = math.ceil(len(records)/500)
        result = []
        for i in range(rq_times):
            payload = {
                "records": records[500*i: 500*(i+1)]
            }
            response = requests.post(url, headers=self.header, json=payload)
            result.append(f"{response.status_code}, {response.json()['msg']}")
        return result


    @retry(tries=3)
    def create_cloudfile_records(self, records: list):
        """往表里插入records
        Args:
            records (list): [
                {
                "fields": {
                    "索引": "索引列多行文本类型",
                    "多行文本": "多行文本内容",
                    "数字": 100,
                    "单选": "选项3",
                    "多选": [
                    "选项1",
                    "选项2"
                    ],
                    "日期": 1674206443000,
                    "复选框": true,
                    "人员": [
                    {
                        "id": "ou_2910013f1e6456f16a0ce75ede950a0a"
                    },
                    {
                        "id": "ou_e04138c9633dd0d2ea166d79f548ab5d"
                    }
                    ],
                    "电话号码": "13026162666",
                    "超链接": {
                    "text": "飞书多维表格官网",
                    "link": "https://www.feishu.cn/product/base"
                    },
                    "附件": [
                    {
                        "file_token": "Vl3FbVkvnowlgpxpqsAbBrtFcrd"
                    }
                    ],
                    "单向关联": [
                    "recHTLvO7x",
                    "recbS8zb2m"
                    ],
                    "双向关联": [
                    "recHTLvO7x",
                    "recbS8zb2m"
                    ],
                    "地理位置": "116.397755,39.903179"
                }
                }
            ]
        """
        if not records:
            raise ValueError("records is empty")
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/batch_create?user_id_type=open_id"
        # 飞书一次只支持500个数据的create 所以要分次
        rq_times = math.ceil(len(records)/500)
        result = []
        for i in range(rq_times):
            payload = {
                "records": records[500*i: 500*(i+1)]
            }
            response = requests.post(url, headers=self.header, json=payload)
            result.append(f"{response.status_code}, {response.json()['msg']}")
        return result


    @retry(tries=3)
    def delete_cloudfile_records(self, records: List[str]):
        # 删除的多条记录id列表
        if not records:
            raise ValueError("records can not is empty")
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/batch_delete"
        rq_times = math.ceil(len(records)/500)
        result = []
        for i in range(rq_times):
            payload = {
                "records": records[500*i: 500*(i+1)]
            }
            response = requests.post(url, headers=self.header, json=payload)
            result.append(f"{response.status_code}, {response.json()['msg']}")
        return result
    

class CloudTableNew(CloudTable):
    
    @retry(tries=3)
    def get_cloudfile_records(self, **extend_params) -> List[GetRecord]:
        """获取所有的GetRecord类型的records
        Returns:
            List[GetRecord]
        """
        self.all_records = super().get_cloudfile_records(**extend_params)
        return [self.GetRecordClass(**r) for r in self.all_records]
    
    
    def insert_and_update_records(self, PostRecords: List[PostRecord]):
        # 插入和修改记录
        # 1. 先获取所有记录的PRIMARY_KEY
        # 2. 获取所有记录的PRIMARY_KEY对应的记录
        # 3. 遍历所有记录 如果PRIMARY_KEY存在 则update 如果不存在 则create
        # 4. 返回所有记录
        exist_records = self.get_cloudfile_records()
        # 建立一个逻辑主键PRIMARY_KEY和record_id的映射Dict
        exist_record = {
            Grecord.PRIMARY_KEY: Grecord.record_id for Grecord in exist_records if Grecord.fields and Grecord.PRIMARY_KEY
        }
        # PRIMARY_KEY不存在 create
        create_records = []
        # PRIMARY_KEY存在 update
        update_records = []
        for Precord in PostRecords:
            if Precord.PRIMARY_KEY in exist_record:
                Precord.record_id = exist_record[Precord.PRIMARY_KEY]
                Precord.record['record_id'] = Precord.record_id
                update_records.append(Precord.record)
                log.debug(f"update records: {Precord.PRIMARY_KEY}")
            else:
                create_records.append(Precord.record)
                log.debug(f"create records: {Precord.PRIMARY_KEY}")
        
        log.info(f"create_records num:{len(create_records)}")
        if create_records:
            result = super().create_cloudfile_records(create_records)
            log.info(result)
        log.info(f"update_records num:{len(update_records)}")
        if update_records:
            result = super().update_cloudfile_records(update_records)
            log.info(result)


if __name__ == "__main__":
    ...
