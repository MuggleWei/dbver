# dbver

## 概述
`dbver` 是一个以版本视角, 管理数据库表结构的工具, 功能包括
* 将 sql 文件规范化
* 通过不同版本的建表语句, 生成不同版本间数据库表结构的更新与回滚语句
* 检测数据库表结构是否与指定建表语句匹配

## 打包
运行 `pkg.sh`

## 运行

### normal 命令
`normal` 命令生成规范化的 sql 文件
```
./bin/dbver normal \
	--host=localhost \
	--port=3306 \
	--user=mugglewei \
	--passwd=xxxxxx \
	--src=datas/v1.0.0.sql
```
注意
* 这里需要连接可以连接的 MySQL 兼容数据库, 一定不要使用生产库, 最好是一个本地开发库, 因为此命令会自动删除和生成对应的 database

### diff 命令
`diff` 命令用于生成不同版本间数据库表结构的更新与回滚语句
```
./bin/dbver diff \
	--host=localhost \
	--port=3306 \
	--user=mugglewei \
	--passwd=xxxxxx \
	--src=datas/v1.0.0.sql \
	--dst=datas/v1.1.0.sql
```
注意
* 这里需要连接可以连接的 MySQL 兼容数据库, 一定不要使用生产库, 最好是一个本地开发库, 因为此命令会自动删除和生成对应的 database

### check 命令
`check` 命令用于检测数据库表结构是否与指定建表语句匹配
```
./bin/dbver check \
	--host=localhost \
	--port=3306 \
	--user=mugglewei \
	--passwd=xxxxxx \
	--database=v1_0_0 \
	--dst=datas/v1.1.0.sql
```
注意
* 这里需要连接可以连接的 MySQL 兼容数据库, 这条命令不会创建任何 database, 只是将 sql 文件与 database 进行对比, 可以安全的在生产环境使用
