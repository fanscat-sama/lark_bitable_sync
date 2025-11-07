import os
from pymysql.cursors import DictCursor

log_defulat_dir = os.environ.get("CMDB_LOG_DIR", "/root/qt-cmdb/log/")


default_bitable_app_token = ""
default_bitable_table_id = ""

# 填写你的Lark表有权限的机器人的app_id和app_secret
default_lark_app_id = ""
default_lark_app_secret = ""

default_conn_settings = {
    'host': os.environ.get("DB_HOST", '127.0.0.1'),
    'port': os.environ.get("DB_PORT", 3306),
    'user': os.environ.get("DB_USER", 'root'),
    'db': os.environ.get("DB_NAME"),
    'passwd': os.environ.get("DB_PASSWORD"),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    # 'autocommit': True
}

