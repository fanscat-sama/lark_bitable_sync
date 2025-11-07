import datetime
from typing import Optional, List, Dict

from models.cloud_base import PostRecord, DataObj, GetRecord
from models.cloud_table import CloudTableNew


class ServerDataObj(DataObj):
    sid: str
    name: str
    owner: Optional[str]
    status: str
    ip_private: Optional[str]
    ip_public: Optional[str]
    create_time: datetime.datetime
    
    will_recycle: bool = False  # 是否即将回收
    cpu: Optional[int]
    ram: Optional[float]
    disk_hdd: Optional[float]
    disk_ssd: Optional[float]
    
    
    @property
    def PRIMARY_KEY(self):
        return self.sid



class ServerGetRecord(GetRecord):
    @property
    def PRIMARY_KEY(self):
        return self.fields['sid']


class ServerPostRecord(PostRecord):
    """
    将从数据库获取的Server_data_obj初始化成一个record
    """
    def __init__(self, obj: ServerDataObj) -> None:
        super().__init__(obj=obj)
        # 将ArpInfoDBObj对象的属性转换为字典
        self.obj = obj
        
        #!!! PostRecord.fields的每一个key的name 应当与多维表格的列名对应且完全一致
        self.fields.update({
            "sid": obj.sid,
            "机器名": obj.name,
            # owner字段应当从多维表格同步到数据库 此处不设置owner fields
            "状态": obj.status,
            "内网IP": obj.ip_private,
            "公网IP": obj.ip_public,
            "创建时间": self._totimestamp(obj.create_time),
            "是否回收": self.recycle_tatus,
            "机器资源配置": self.assets  # 从cpu, ram, disk_hdd, disk_ssd 转为assets
        })


    @property
    def recycle_tatus(self):
        "机器是否回收 将tinyint类型数据 0为False 1为True转为字符串"
        return "正常" if not self.obj.network_disconnect else "即将回收"
    
    
    @property
    def assets(self):
        "一台机器的assets - human read"
        # 获取各个硬件资源总量
        # 构造资产描述字符串
        assets = f"{self.obj.cpu}核{self.obj.ram}G内存"
        if self.obj.disk_hdd != 0:
            assets += f"{self.obj.disk_hdd}G HDD"
        if self.obj.disk_ssd != 0:
            assets += f"{self.obj.disk_ssd}G SSD"
        return assets


class ServersTable(CloudTableNew):

    def __init__(self, app_token="", table_id="", *args, **kwargs) -> None:
        super().__init__(app_token=app_token, table_id=table_id, GetRecordClass=ServerGetRecord, *args, **kwargs)


    def query_new_servers(self, days=1) -> List[ServerGetRecord]:
        """从多维表格 获取最近days天内新建的servers

        Args:
            days (int, optional): _description_. Defaults to 1.

        Returns:
            list: records of new servers
        """
        query_new_servers = f"today()-{days} <= CurrentValue.[创建时间]"
        new_records: List[ServerGetRecord] = self.get_cloudfile_records(filter=query_new_servers)
        return new_records
    
    
    def query_owner_servers(self, owners: List[str]) -> List[ServerGetRecord]:
        """_summary_

        Args:
            owners (List[str]): cnames

        Returns:
            list: _description_
        """
        contains = ",".join(f'"{s}"' for s in owners)
        query_owner_servers = f'CurrentValue.[owner].contains({contains})'
        new_records = self.get_cloudfile_records(filter=query_owner_servers)
        return new_records


if __name__ == "__main__":
    ...
