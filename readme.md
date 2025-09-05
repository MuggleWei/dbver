# dbver

## 概述
`dbver` 是一个以版本视角, 管理数据库表结构的工具, 功能包括
* 生成不同版本间数据库表结构的更新与回滚语句
* 检测数据库表结构是否与指定建表语句匹配

## 打包
运行 `pkg.sh`

## 运行

### diff 命令
`diff` 命令用于生成不同版本间数据库表结构的更新与回滚语句, 需要一个可以登录的 MySQL 兼容数据库, 以及两个已经准备好的不同版本的建表语句  
```
./bin/dbver diff \
	--host=localhost \
	--port=3306 \
	--user=muggle \
	--passwd=xxxxxx \
	--src=datas/v1.0.0.sql \
	--dst=datas/v1.1.0.sql
```

### check 命令
`check` 命令用于检测数据库表结构是否与指定建表语句匹配
```
./bin/dbver check \
	--host=localhost \
	--port=3306 \
	--user=muggle \
	--passwd=xxxxxx \
	--database=v1_0_0 \
	--dst=datas/v1.1.0.sql
```
