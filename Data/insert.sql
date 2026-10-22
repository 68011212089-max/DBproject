-- 1. ตารางลูกค้า
INSERT INTO customer (name, email,province_id , tier) VALUES
('สมชาย ใจดี', 'somchai@gmail.com', '52', 'normal'),
('สมหญิง รักเรียน', 'somying@gmail.com', '64', 'vip'),
('วิชัย มีสุข', 'wichai@gmail.com', '49', 'normal');


-- 2. ตารางสินค้า
INSERT INTO product (name, category, price, stock) VALUES
('Laptop', 'Electronics', 25000.00, 10),
('Mouse', 'Accessories', 350.00, 50),
('Keyboard', 'Accessories', 890.00, 30);


-- 3. ตารางที่อยู่ลูกค้า
-- province_id ต้องมีอยู่จริงในตาราง province
INSERT INTO customer_address
(cust_id, recipient_name, phone, address_detail, province_id, postal_code) VALUES
(1, 'สมชาย ใจดี', '0812345678', '123 หมู่ 1', 1, '40000'),
(2, 'สมหญิง รักเรียน', '0823456789', '45 ถนนหลัก', 2, '50000'),
(3, 'วิชัย มีสุข', '0834567890', '99 ถนนสุขุมวิท', 3, '10110');


-- 4. ตารางคำสั่งซื้อ
INSERT INTO shop_order
(cust_id, address_id, order_date, status) VALUES
(1, 1, '2026-10-01 09:00:00', 'pending'),
(2, 2, '2026-10-02 10:30:00', 'shipped'),
(3, 3, '2026-10-03 14:00:00', 'delivered');


-- 5. ตารางรายการสินค้าในคำสั่งซื้อ
INSERT INTO order_line
(order_id, product_id, qty, unit_price) VALUES
(1, 1, 1, 25000.00),
(1, 2, 2, 350.00),
(2, 3, 1, 890.00),
(3, 2, 1, 350.00);


-- 6. ตารางการชำระเงิน
INSERT INTO payment
(order_id, method, amount, status, paid_date) VALUES
(1, 'PromptPay', 25700.00, 'pending', NULL),
(2, 'Credit Card', 890.00, 'paid', '2026-10-02 11:00:00'),
(3, 'Bank Transfer', 350.00, 'paid', '2026-10-03 15:00:00');


-- 7. ตารางรีวิวสินค้า
INSERT INTO review
(cust_id, product_id, rating, comment, review_date) VALUES
(1, 1, 5, 'สินค้าดีมาก', '2026-10-01 12:00:00'),
(2, 3, 4, 'ใช้งานได้ดี', '2026-10-02 16:00:00'),
(3, 2, 5, 'คุ้มค่ากับราคา', '2026-10-03 17:00:00');


-- 8. ตารางตะกร้าสินค้า
INSERT INTO cart (cust_id, created_at) VALUES
(1, '2026-10-01 08:00:00'),
(2, '2026-10-02 09:00:00'),
(3, '2026-10-03 13:00:00');


-- 9. ตารางรายการสินค้าในตะกร้า
INSERT INTO cart_item (cart_id, product_id, qty) VALUES
(1, 2, 1),
(1, 3, 1),
(2, 1, 1),
(3, 2, 2);