# -*- ecoding: utf-8 -*-
# @ModuleName: wirtesql
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/9 9:55

import numpy as np


if __name__ == '__main__':
    str='''SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `sample_dataset`
-- ----------------------------
DROP TABLE IF EXISTS `sample_dataset`;
CREATE TABLE `sample_dataset` (
`id` int(10) NOT NULL AUTO_INCREMENT,
`reals` float NOT NULL comment '真实值',
`predict` float NOT NULL comment '预测值',
`a` varchar(10) NOT NULL comment 'a特征',
`b` varchar(10) NOT NULL comment 'b特征',
`c` varchar(10) NOT NULL comment 'c特征',
`d` varchar(10) NOT NULL comment 'd特征',
`anomaly` smallint(2) NULL comment '是否异常',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sample_dataset
-- ----------------------------
'''
    with open('sample_dataset.sql','w',encoding='utf-8') as ft:
        ft.write(str)
        with open('../B0/B_cuboid_layer_1_n_ele_1/1450653900.csv','r') as fs:
            data=fs.readlines()
            for i in range(1,len(data)):
                line='\',\''.join(data[i][:-1].split(','))

                str='INSERT INTO `sample_dataset` VALUES (NULL, \''+line+'\',NULL);\n'
                ft.write(str)
