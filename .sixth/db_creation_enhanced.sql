-- ============================================
-- Atliq Tees Database - Enhanced Version
-- ============================================

CREATE DATABASE IF NOT EXISTS atliq_tshirts;
USE atliq_tshirts;

DROP PROCEDURE IF EXISTS PopulateTShirts;
DROP TABLE IF EXISTS discounts;
DROP TABLE IF EXISTS t_shirts;

-- ============================================
-- T-SHIRTS TABLE
-- ============================================
CREATE TABLE t_shirts (
    t_shirt_id INT AUTO_INCREMENT PRIMARY KEY,
    brand ENUM('Van Heusen', 'Levi', 'Nike', 'Adidas') NOT NULL,
    color ENUM('Red', 'Blue', 'Black', 'White') NOT NULL,
    size ENUM('XS', 'S', 'M', 'L', 'XL') NOT NULL,
    price INT CHECK (price BETWEEN 10 AND 50),
    stock_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY brand_color_size (brand, color, size),
    INDEX idx_brand (brand),
    INDEX idx_color (color),
    INDEX idx_price (price)
);

-- ============================================
-- DISCOUNTS TABLE
-- ============================================
CREATE TABLE discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    t_shirt_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    discount_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id) ON DELETE CASCADE,
    INDEX idx_t_shirt (t_shirt_id),
    INDEX idx_dates (start_date, end_date)
);

-- ============================================
-- STORED PROCEDURE - POPULATE WITH SAMPLE DATA
-- ============================================
DELIMITER $$
CREATE PROCEDURE PopulateTShirts()
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE max_records INT DEFAULT 80;
    DECLARE v_brand ENUM('Van Heusen', 'Levi', 'Nike', 'Adidas');
    DECLARE v_color ENUM('Red', 'Blue', 'Black', 'White');
    DECLARE v_size ENUM('XS', 'S', 'M', 'L', 'XL');
    DECLARE v_price INT;
    DECLARE v_stock INT;

    SET SESSION rand_seed1 = UNIX_TIMESTAMP();

    WHILE counter < max_records DO
        SET v_brand = ELT(FLOOR(1 + RAND() * 4), 'Van Heusen', 'Levi', 'Nike', 'Adidas');
        SET v_color = ELT(FLOOR(1 + RAND() * 4), 'Red', 'Blue', 'Black', 'White');
        SET v_size = ELT(FLOOR(1 + RAND() * 5), 'XS', 'S', 'M', 'L', 'XL');
        SET v_price = FLOOR(15 + RAND() * 36); -- Price between 15-50
        SET v_stock = FLOOR(20 + RAND() * 200); -- Stock between 20-220

        BEGIN
            DECLARE CONTINUE HANDLER FOR 1062 BEGIN END; -- Handle duplicate
            INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
            VALUES (v_brand, v_color, v_size, v_price, v_stock);
            SET counter = counter + 1;
        END;
    END WHILE;
END$$
DELIMITER ;

-- ============================================
-- EXECUTE POPULATION
-- ============================================
CALL PopulateTShirts();

-- ============================================
-- INSERT SAMPLE DISCOUNT DATA
-- ============================================
INSERT INTO discounts (t_shirt_id, pct_discount, discount_name, start_date, end_date)
SELECT 
    t_shirt_id,
    CASE 
        WHEN MOD(t_shirt_id, 5) = 0 THEN 10.00
        WHEN MOD(t_shirt_id, 5) = 1 THEN 15.00
        WHEN MOD(t_shirt_id, 5) = 2 THEN 20.00
        WHEN MOD(t_shirt_id, 5) = 3 THEN 25.00
        ELSE 5.00
    END,
    CONCAT('Spring Sale - ', brand, ' ', color),
    DATE_SUB(CURDATE(), INTERVAL 7 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY)
FROM t_shirts
LIMIT 15;

-- ============================================
-- VERIFY DATA
-- ============================================
SELECT COUNT(*) as total_shirts FROM t_shirts;
SELECT COUNT(*) as total_discounts FROM discounts;
SELECT brand, COUNT(*) as count, SUM(stock_quantity) as total_stock
FROM t_shirts
GROUP BY brand;

-- ============================================
-- USEFUL VIEWS (OPTIONAL)
-- ============================================

CREATE OR REPLACE VIEW v_inventory_summary AS
SELECT 
    brand,
    color,
    COUNT(*) as size_count,
    SUM(stock_quantity) as total_stock,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM t_shirts
GROUP BY brand, color;

CREATE OR REPLACE VIEW v_discount_details AS
SELECT 
    d.discount_id,
    t.brand,
    t.color,
    t.size,
    t.price,
    d.pct_discount,
    ROUND(t.price * (1 - d.pct_discount/100), 2) as discounted_price,
    d.discount_name,
    d.start_date,
    d.end_date,
    DATEDIFF(d.end_date, CURDATE()) as days_remaining
FROM discounts d
JOIN t_shirts t ON d.t_shirt_id = t.t_shirt_id;

CREATE OR REPLACE VIEW v_low_stock_alert AS
SELECT 
    t_shirt_id,
    brand,
    color,
    size,
    stock_quantity,
    CASE 
        WHEN stock_quantity < 30 THEN 'CRITICAL'
        WHEN stock_quantity < 50 THEN 'LOW'
        ELSE 'OK'
    END as stock_status
FROM t_shirts
WHERE stock_quantity < 50
ORDER BY stock_quantity ASC;
