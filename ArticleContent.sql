SET FOREIGN_KEY_CHECKS = 0;
-- 删除已有表和触发器（如果存在）
DROP TRIGGER IF EXISTS before_insert_web_data_table;
DROP TABLE IF EXISTS web_data_table;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS article_rating;
-- 创建主表 web_data_table
CREATE TABLE web_data_table (
    id int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    formatted_id varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '格式化ID',
    title text NOT NULL COMMENT '标题',
    author varchar(100) DEFAULT NULL COMMENT '作者',
    info_type varchar(50) DEFAULT 'T0' COMMENT '信息类型',
    post_agency varchar(80) DEFAULT NULL COMMENT '发布机构',
    nation varchar(50) DEFAULT NULL COMMENT '国家',
    article_date DATE COMMENT '日期',
    link_url VARCHAR(500) UNIQUE COMMENT '链接URL',  -- 更改为 VARCHAR(500) 以支持唯一索引
    domain varchar(50) DEFAULT 'F0' COMMENT '领域',
    subject varchar(50) DEFAULT 'AG0' COMMENT '学科',
    text text DEFAULT NULL COMMENT '正文',
    average_rating DOUBLE DEFAULT NULL COMMENT '平均评分',
    rating_count INT DEFAULT NULL COMMENT '评分次数',
    PRIMARY KEY (id),
    UNIQUE KEY formatted_id (formatted_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 创建触发器 before_insert_web_data_table
DELIMITER $$

CREATE TRIGGER before_insert_web_data_table
BEFORE INSERT ON web_data_table
FOR EACH ROW
BEGIN
    -- 检查date字段是否为空
    IF NEW.article_date IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Date field cannot be NULL';
    END IF;

    -- 从date字段提取年月，并格式化为YYYYMM
    SET @year_month = DATE_FORMAT(NEW.article_date, '%Y%m');

    -- 初始化变量，用于存储当前年月的最大序列号
    SET @max_serial = 0;

    -- 查询当前年月已存在的formatted_id的最大序列号
    SELECT COALESCE(MAX(CAST(SUBSTRING(formatted_id, 8) AS UNSIGNED)), 0) INTO @max_serial
    FROM web_data_table
    WHERE formatted_id COLLATE utf8mb4_general_ci LIKE CONCAT(@year_month, '%');

    -- 计算新记录的序列号
    SET @new_serial = @max_serial + 1;

    -- 构造新的formatted_id
    SET NEW.formatted_id = CONCAT(@year_month, '-', LPAD(@new_serial, 4, '0'));
END$$


-- 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;