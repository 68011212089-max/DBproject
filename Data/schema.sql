-- schema.sql - ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
-- กติกา: 1 ออเดอร์มีหลายสินค้า (m:n: order × product ผ่าน order_line)
-- รีวิว = m:n (customer × product), การชำระเงิน 1:m จาก shop_order
-- ===============================================================
-- 1. ตารางลูกค้า
CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(255),
    tier ENUM('normal', 'vip') NOT NULL DEFAULT 'normal'
);

-- 2. ตารางสินค้า
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    CHECK (price >= 0),
    CHECK (stock >= 0)
);

-- 3. ตารางที่อยู่ลูกค้า
CREATE TABLE customer_address (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address_detail VARCHAR(255) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id)
        ON DELETE CASCADE
);

-- 4. ตารางคำสั่งซื้อ
CREATE TABLE shop_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    address_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM(
        'pending',
        'shipped',
        'delivered',
        'cancelled'
    ) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id),
    FOREIGN KEY (address_id)
        REFERENCES customer_address(address_id)
        ON DELETE SET NULL
);

-- 5. ตารางรายการสินค้าในคำสั่งซื้อ
CREATE TABLE order_line (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id)
        REFERENCES shop_order(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product(product_id),
    CHECK (qty > 0),
    CHECK (unit_price >= 0)
);

-- 6. ตารางการชำระเงิน
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM(
        'pending',
        'paid',
        'failed'
    ) NOT NULL DEFAULT 'pending',
    paid_date DATETIME,
    FOREIGN KEY (order_id)
        REFERENCES shop_order(order_id)
        ON DELETE CASCADE,
    CHECK (amount >= 0)
);

-- 7. ตารางรีวิวสินค้า
CREATE TABLE review (
    cust_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(255),
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cust_id, product_id),
    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product(product_id)
        ON DELETE CASCADE,
    CHECK (rating BETWEEN 1 AND 5)
);

-- 8. ตารางตะกร้าสินค้า
CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cust_id)
        REFERENCES customer(cust_id)
        ON DELETE CASCADE
);

-- 9. ตารางรายการสินค้าในตะกร้า
CREATE TABLE cart_item (
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    PRIMARY KEY (cart_id, product_id),
    FOREIGN KEY (cart_id)
        REFERENCES cart(cart_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES product(product_id),
    CHECK (qty > 0)
);
-- todo: insert ข้อมูลตัวอย่างตามตาราง
--
--    * ควรมีทั้งออเดอร์ที่ชำระเงินแล้ว (มีแถวใน payment) และที่ยังไม่ชำระ
--      ไว้ทดสอบการจัดส่ง/การกรอง