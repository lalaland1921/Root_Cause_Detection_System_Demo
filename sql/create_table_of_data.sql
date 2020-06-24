SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `table_of_data`
-- ----------------------------
DROP TABLE IF EXISTS `table_of_data`;
CREATE TABLE `table_of_data` (
`id` int(10) NOT NULL AUTO_INCREMENT,
`name` varchar(20) NULL comment '数据表名称',
`Timepoint` float NULL comment '时间戳',
`root_cause` varchar(10) NULL comment '根因',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sample_dataset
-- ----------------------------
INSERT INTO `table_of_data` VALUES ('0', 'sample_dataset','0',NULL);