"""
将多维表格的业务数据写入SQL中
"""
from models.demo import ServersTable

from utils.db import get_db_cursor
from utils.logs import init_logger_obj
log = init_logger_obj()

table = ServersTable()

# 获取servers表中的所有记录
cloud_server_records = table.get_cloudfile_records()
update_servers_args = []
business_fields = ['owner', 'remark']

# 遍历记录
for record in cloud_server_records:
    fields = record.fields
    sid = fields.get('sid')
    if sid is None:
        continue
    #! 同步到servers表
    # 从cloudfile同步owner和remark
    update_value = {fname: fields.get(fname) for fname in business_fields}
    update_value['sid'] = sid
    
    # 将飞书人员字段转化为email-str
    owner_obj = update_value['owner']
    update_value['owner'] = owner_obj[0]['email'] if owner_obj else None
    update_value['remark'] = fields.get('remark')

    # 更新数据
    update_servers_args.append(update_value)


with get_db_cursor() as cur:
    servers_SQL = """
    INSERT INTO
        servers
        (sid, owner, remark)
    VALUES
        (%(sid)s,%(owner)s,%(remark)s)
    ON DUPLICATE KEY UPDATE
        owner = values(owner), 
        remark = values(remark)
    """
    r = cur.executemany(servers_SQL, args=update_servers_args)
    log.info(f"insert or update servers num:{r}")

