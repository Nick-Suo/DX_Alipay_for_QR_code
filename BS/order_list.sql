/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.39 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `order_list` (
	`id` int (11),
	`no` char (192),
	`time` datetime ,
	`status` char (48)
); 
insert into `order_list` (`id`, `no`, `time`, `status`) values('1','001','2020-05-07 17:48:25','已支付');
insert into `order_list` (`id`, `no`, `time`, `status`) values('6','001','2020-05-09 20:36:46','已支付');
