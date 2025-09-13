CREATE TABLE `user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `user_name` varchar(64) DEFAULT '' COMMENT 'user name', -- @rename from=name
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  INDEX idx_name (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
