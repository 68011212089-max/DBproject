-- schema.sql - ร้านค้าออนไลน์ (นิสิตออกแบบและเขียนเอง)
-- กติกา: 1 ออเดอร์มีหลายสินค้า (m:n: order × product ผ่าน order_line)
-- รีวิว = m:n (customer × product), การชำระเงิน 1:m จาก shop_order
-- ===============================================================

create table customer (
    cust_id int auto_increment primary key,
    -- todo: name, email, address, tier
    name varchar(50) not null,
    email varchar(100) not null unique,
    address varchar(100) not null,
    tier enum('normal', 'vip') not null
);

create table product (
    product_id int auto_increment primary key,
    -- todo: name, category, price, stock
    name varchar(50) not null,
    category varchar(50) not null,
    price int not null,
    stock int not null
);

create table shop_order (
    order_id int auto_increment primary key,
    -- todo: cust_id (fk), order_date, status enum('pending','shipped')
    -- * ไม่ต้องมีคอลัมน์ยอดรวม - คำนวณจาก order_line (ดู @ search_orders ใน db.py)
    cust_id int not null,
    order_date date,
    status enum('pending','shipped'), 
    foreign key (cust_id) references customer(cust_id)
);

create table order_line (
    -- m:n: shop_order × product
    -- todo: order_id (fk), product_id (fk), qty, unit_price ; primary key (order_id, product_id)
    order_id int not null,
    product_id int not null,
    qty int not null,
    unit_price int not null,
    primary key (order_id, product_id),
    foreign key (order_id)
        references shop_order(order_id),
    foreign key (product_id)
        references product(product_id)
);

create table review (
    -- m:n: customer × product
    -- todo: cust_id (fk), product_id (fk), rating, comment, review_date ; primary key (cust_id, product_id)
    cust_id int not null,
    product_id int not null,
    rating int not null,
    comment varchar(255),
    review_date date,
    primary key (cust_id, product_id),
    foreign key (cust_id)
        references customer(cust_id),
    foreign key (product_id)
        references product(product_id)
);

create table payment (
    -- 1:m จาก shop_order
    payment_id int auto_increment primary key,
    -- todo: order_id (fk), method, amount, paid_date
    order_id int not null,
    method varchar(50) not null,
    amount int not null,
    paid_date date,
    foreign key (order_id)
        references shop_order(order_id)
);

-- todo: insert ข้อมูลตัวอย่างตามตาราง
--
--    * ควรมีทั้งออเดอร์ที่ชำระเงินแล้ว (มีแถวใน payment) และที่ยังไม่ชำระ
--      ไว้ทดสอบการจัดส่ง/การกรอง