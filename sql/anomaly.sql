SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `anomaly`
-- ----------------------------
DROP TABLE IF EXISTS `anomaly`;
CREATE TABLE `anomaly` (
`id` int(10) NOT NULL AUTO_INCREMENT,
`real` float NOT NULL DEFAULT comment '真实值',
`predict` float NOT NULL DEFAULT comment '预测值',
`deviation` float NOT NULL DEFAULT comment '偏离值',
`a` char(10) float NOT NULL DEFAULT comment 'a特征',
`b` char(10) float NOT NULL DEFAULT comment 'b特征',
`c` char(10) float NOT NULL DEFAULT comment 'c特征',
`d` char(10) float NOT NULL DEFAULT comment 'd特征',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;