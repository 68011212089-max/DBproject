-- ============================================================
--  schema.sql — ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
--  กติกา: 1 ออเดอร์มีหลายสินค้า (M:N: order × product ผ่าน order_line),
--         รีวิว = M:N (customer × product), การชำระเงิน 1:M จาก shop_order
-- ============================================================
CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, email, address, tier
);
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, category, price, stock
);
CREATE TABLE shop_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: cust_id (FK), order_date, status ENUM('pending','shipped')
    -- ★ ไม่ต้องมีคอลัมน์ยอดรวม — คำนวณจาก order_line (ดู search_orders ใน db.py)
);
CREATE TABLE order_line (         -- M:N: shop_order × product
    -- TODO: order_id (FK), product_id (FK), qty, unit_price ; PRIMARY KEY (order_id, product_id)
    order_id INT, product_id INT
);
CREATE TABLE review (             -- M:N: customer × product
    -- TODO: cust_id (FK), product_id (FK), rating, comment, review_date ; PRIMARY KEY (cust_id, product_id)
    cust_id INT, product_id INT
);
CREATE TABLE payment (            -- 1:M จาก shop_order
    payment_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: order_id (FK), method, amount, paid_date
);
-- TODO: INSERT ข้อมูลตัวอย่างทุกตาราง
--   ★ ควรมีทั้งออเดอร์ที่ชำระเงินแล้ว (มีแถวใน payment) และที่ยังไม่ชำระ ไว้ทดสอบการจัดส่ง/การลบ
