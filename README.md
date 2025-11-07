# lark_bitable_sync

将自己的数据同步到飞书多维表格；Mysql和飞书多维表格数据同步

---

# Demo:

> SQL table: servers
>
> 其中sid为servers中的主键；
>
> 有owner，remark字段，需要从多维表格同步到数据库中（方便用户写入）
>
> ```
> app/demo/demo_sync_to_sql.py
> ```
>
> 而status，create_time，ip信息，机器资源，服务器名，从数据库同步到多维表格（基础信息，同时飞书应当限制这些字段不能让用户自行修改）
>
> ```
> app/demo/demo_sync_to_bitable.py
> ```
>
> 而后通过crontab定期执行即可，推荐运行频率：3k行，3分钟/次，并且错开同一个表的正向同步和反向同步间隔
>
> ```
> */3 * * * * root /usr/bin/python3  $DIR/app/demo/demo_sync_to_sql.py
> 2-59/3 * * * * root /usr/bin/python3  $DIR/app/demo/demo_sync_to_bitable.py
> ```
>
>
>
>
