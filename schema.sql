-- schema.sql - ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
-- กติกา: 1 ออเดอร์มีหลายสินค้า (M:N: order × product ผ่าน order_line)
-- รีวิว = M:N (customer × product), การชำระเงิน 1:M จาก shop_order
-- ===============================================================

CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    -- TODO: name, email, address, tier
    name varchar(50) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    address varchar(100) NOT NULL,
    tier varchar(50) NOT NULL
);

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    -- TODO: name, category, price, stock
    name varchar(50) NOT NULL,
    category varchar(50) NOT NULL,
    price int NOT NULL,
    stock int NOT NULL
);

CREATE TABLE shop_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    -- TODO: cust_id (FK), order_date, status ENUM('pending','shipped')
    -- * ไม่ต้องมีคอลัมน์ยอดรวม - คำนวณจาก order_line (ดู @ search_orders ใน db.py)
    cust_id int NOT NULL,
    order_date date,
    status ENUM('pending','shipped'),

    FOREIGN KEY (cust_id) REFERENCES customer(cust_id)
);

CREATE TABLE order_line (       -- M:N: shop_order × product
    -- TODO: order_id (FK), product_id (FK), qty, unit_price ; PRIMARY KEY (order_id, product_id)
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    unit_price INT NOT NULL,

    PRIMARY KEY (order_id, product_id),

    FOREIGN KEY (order_id)
        REFERENCES shop_order(order_id),

    FOREIGN KEY (product_id)
        REFERENCES product(product_id)
);

CREATE TABLE review (           -- M:N: customer × product
    -- TODO: cust_id (FK), product_id (FK), rating, comment, review_date ; PRIMARY KEY (cust_id, product_id)
    cust_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(255),
    review_date DATE,

    PRIMARY KEY (cust_id, product_id),

    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id),

    FOREIGN KEY (product_id)
        REFERENCES product(product_id)
);

CREATE TABLE payment (           -- 1:M จาก shop_order
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    -- TODO: order_id (FK), method, amount, paid_date
    order_id INT NOT NULL,
    method VARCHAR(50) NOT NULL,
    amount INT NOT NULL,
    paid_date DATE,

    FOREIGN KEY (order_id)
        REFERENCES shop_order(order_id)
);

-- TODO: INSERT ข้อมูลตัวอย่างตามตาราง
--
--    * ควรมีทั้งออเดอร์ที่ชำระเงินแล้ว (มีแถวใน payment) และที่ยังไม่ชำระ
--      ไว้ทดสอบการจัดส่ง/การกรอง