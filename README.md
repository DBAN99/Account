<<<<<<< HEAD
# Account API






=======
# Account API

### 가계부 DB 스키마

CREATE TABLE `register_form` (
  `user_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_email` varchar(60),
  `user_password` text NOT NULL,
  `user_del` varchar(2) NOT NULL DEFAULT 0
);

CREATE TABLE `account_memo` (
  `user_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_amount` text,
  `user_memo` text,
  `user_del` varchar(2) NOT NULL DEFAULT 0,
  `memo_del` varchar(2) NOT NULL DEFAULT 0
);

ALTER TABLE `register_form` ADD FOREIGN KEY (`user_id`) REFERENCES `account_memo` (`user_id`);

ALTER TABLE `register_form` ADD FOREIGN KEY (`user_del`) REFERENCES `account_memo` (`user_del`);
>>>>>>> 990f2ac6aeaad4eb6e9b25fe6dfb44610808552a
