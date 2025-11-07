import time
import datetime

from typing import List, Dict, Optional

from pydantic import BaseModel


class DataObj(BaseModel):
    "init From Mysql Dict Data"
    
    @property
    def values(self) -> List:
        ...
    
    @property
    def PRIMARY_KEY(self):
        ...


class GetRecord(BaseModel):
    id: str
    record_id: str
    fields: Dict = {}

    
    @property
    def PRIMARY_KEY(self):
        return ...
    
    
    def _todatetime(self, timestamp: int) -> Optional[datetime.datetime]:
        """
        将datetime类型数据转为飞书时间戳
        """
        return datetime.datetime.fromtimestamp(timestamp/1000) if timestamp else None


class PostRecord():
    def __init__(self, obj: DataObj) -> None:
        self.obj = obj
        self.fields: Dict = {}
        self.record = {
            "fields": self.fields
        }
        self.record_id: str = None
    
    
    @property
    def PRIMARY_KEY(self):
        return self.obj.PRIMARY_KEY
    
    
    def _totimestamp(self, xtime: datetime.datetime) -> Optional[int]:
        """
        将datetime类型数据转为飞书时间戳
        """
        try:
            return int(time.mktime(xtime.timetuple())) * 1000 if xtime else None
        except Exception as e:
            return

