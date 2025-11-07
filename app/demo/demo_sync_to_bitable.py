from utils.db import get_db_cursor
from models.demo import ServerDataObj, ServerPostRecord, ServersTable

from log import init_logger_obj
log = init_logger_obj()

# where 判断和from table按需修改即可
sync_query_sql = """
SELECT     
    *
FROM 
    servers
WHERE
    ...
"""


table = ServersTable()

with get_db_cursor() as cur:
    cur.execute(sync_query_sql)

    DBobj_list = [ServerDataObj(**r) for r in cur.fetchall()]
    PostRecords = [ServerPostRecord(obj=o) for o in DBobj_list]

    table.insert_and_update_records(PostRecords=PostRecords)
