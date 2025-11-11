from utils.db import get_db_cursor
#* 1. 此处改为你自己的数据对应的类型 
# from models.demo import YourDemoDataObj, YourDemoPostRecord, YourDemotable
from models.demo import ServerDataObj, ServerPostRecord, ServersTable

from log import init_logger_obj
log = init_logger_obj()

# where 判断和from table按需修改即可
#* 2. 修改此处为你自己的demo查询语句
sync_query_sql = """
SELECT     
    *
FROM 
    servers
WHERE
    ...
"""

#* 3. 初始化你自己的Table对象
# table = YourDemotableTable()
table = ServersTable()

with get_db_cursor() as cur:
    cur.execute(sync_query_sql)

    #* 4. 获取数据库数据
    # DataObj_list = [YourDemoDataObj(**r) for r in cur.fetchall()]
    DataObj_list = [ServerDataObj(**r) for r in cur.fetchall()]
    #* 5. DataObj转为PostRecord
    # PostRecords = [YourDemoPostRecord(obj=o) for o in DataObj_list]
    PostRecords = [ServerPostRecord(obj=o) for o in DataObj_list]

    table.insert_and_update_records(PostRecords=PostRecords)
