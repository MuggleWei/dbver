# dbver

## 概述
用于生成不同版本间数据库表结构的更新与回滚语句

## 打包
运行 `pkg.sh`

## 运行
运行时需要有一个已经安装好的 MySQL 兼容数据库, 然后有两个不同版本的完整建表语句, 例如
`./bin/dbver diff --host=localhost --port=3306 --user=muggle --passwd=xxxxxx --src=datas/v1.0.0.sql --dst=datas/v1.1.0.sql`
