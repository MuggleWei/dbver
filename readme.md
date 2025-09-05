# dbver

## 概述
`dbver` 是一个用于生成不同版本间数据库表结构的更新与回滚语句, 以及校验数据库表结构是否与指定建表语句匹配的工具

## 打包
运行 `pkg.sh`

## 运行

### diff 命令
`diff` 命令用于生成不同版本见数据库表结构的更新与回滚语句, 需要一个可以登录的 MySQL 兼容数据库, 以及两个已经准备好的不同版本的建表语句  
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
尚未实现
