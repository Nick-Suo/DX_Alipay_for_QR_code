/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.39 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `good_list` (
	`id` int (16),
	`good_name` char (48),
	`good_price` int (16),
	`good_size` int (16)
); 
insert into `good_list` (`id`, `good_name`, `good_price`, `good_size`) values('1','独面筋','16','5');
insert into `good_list` (`id`, `good_name`, `good_price`, `good_size`) values('2','煎烹大虾','33','5');
insert into `good_list` (`id`, `good_name`, `good_price`, `good_size`) values('3','八珍豆腐','24','3');
insert into `good_list` (`id`, `good_name`, `good_price`, `good_size`) values('4','麻婆豆腐','15','5');
insert into `good_list` (`id`, `good_name`, `good_price`, `good_size`) values('5','沙拉','20','4');
