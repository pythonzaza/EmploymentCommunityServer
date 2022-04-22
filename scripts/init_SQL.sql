/*
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Schema         : EmploymentCommunity
 File Encoding         : 65001
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user 用户表
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '昵称',
  `account` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '密码',
  `email` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '邮箱',
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `register_time` datetime NULL DEFAULT NULL COMMENT '注册时间',
  `register_ip` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '注册ip',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `account`(`account`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  INDEX `password`(`password`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic  COMMENT='用户表';

-- ----------------------------
-- Table structure for enterprises 企业表
-- ----------------------------
CREATE TABLE `enterprises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '企业名称',
  `legal_person` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '法人',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '企业地址',
  `details` varchar(3000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '企业简介',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '企业统一社会信用码',
  `TYX_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '天眼查URL',
  `create_date` date DEFAULT NULL COMMENT '企业创建时间',
  `register_capital` int DEFAULT NULL COMMENT '注册资本, 单位:万',
  `create_time` datetime DEFAULT NULL COMMENT '资料添加时间',
  `create_user_id` int DEFAULT NULL COMMENT '添加用户id',
  `update_time` datetime DEFAULT NULL COMMENT '最后修改时间',
  `message_count` int DEFAULT '0' COMMENT '留言数量',
  `status` int DEFAULT '1' COMMENT '状态 1正常 -1删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`,`status`) USING BTREE,
  UNIQUE KEY `code` (`status`,`code`) USING BTREE,
  KEY `message_count` (`message_count`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
-- ----------------------------
-- Table structure for message_board 留言板
-- ----------------------------
CREATE TABLE `message_board` (
  `id` int NOT NULL AUTO_INCREMENT,
  `enterprise_id` int NOT NULL COMMENT '企业id',
  `reply_message_id` int DEFAULT '0' COMMENT '被回复留言id',
  `reply_user_id` int DEFAULT '0' COMMENT '被回复用户id',
  `reply_user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '被回复用户名',
  `user_id` int NOT NULL COMMENT '用户id',
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '用户名',
  `message` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '留言内容',
  `comment_number` int DEFAULT '0' COMMENT '评论次数',
  `like_number` int DEFAULT '0' COMMENT '点赞次数',
  `create_time` datetime DEFAULT NULL,
  `status` tinyint DEFAULT '1' COMMENT '状态, 1正常 -1删除',
  PRIMARY KEY (`id`),
  KEY `enterprise_id` (`enterprise_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin  COMMENT='留言板';

-- ----------------------------
-- Table structure for enterprises_log 企业资料修改记录
-- ----------------------------
CREATE TABLE `enterprises_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `enterprise_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `data` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `enterprise_id` (`enterprise_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `create_time` (`create_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
-- Table structure for user_login_log 用户登录日志表
-- ----------------------------
CREATE TABLE `user_login_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `login_ip` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登录ip',
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '城市',
  `coordinates` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '坐标',
  `is_login` bit(1) DEFAULT b'0' COMMENT '是否登录成功',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `verify` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '验证字段',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`,`create_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


SET FOREIGN_KEY_CHECKS = 1;
