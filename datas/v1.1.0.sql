CREATE TABLE `user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(64) DEFAULT '' COMMENT 'user name',
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  INDEX idx_name (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `foo` (
	`id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
