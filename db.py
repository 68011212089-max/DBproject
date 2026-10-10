# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def blank_to_none(value):
    """ช่องที่ไม่ได้กรอกในฟอร์มจะส่งมาเป็น "" — แปลงเป็น None (= NULL ใน SQL)
    ใช้กับคอลัมน์ที่ว่างได้ เช่น return_date, paid_date  เพราะ MySQL ไม่รับ '' เป็น DATE"""
    return None if value in ("", None) else value


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


# ============================================================
# 1. CUSTOMER
# ============================================================

def search_customers(filters):
    sql = "SELECT * FROM customer WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("email"):
        sql += " AND email LIKE %s"
        params.append("%" + filters["email"] + "%")

    if filters.get("tier"):
        sql += " AND tier = %s"
        params.append(filters["tier"])

    sql += " ORDER BY cust_id"
    return run_query(sql, params)


def get_customer(cust_id):
    rows = run_query(
        "SELECT * FROM customer WHERE cust_id = %s",
        (cust_id,)
    )
    return rows[0] if rows else None


def create_customer(data):
    sql = """
        INSERT INTO customer (name, email, address, tier)
        VALUES (%s, %s, %s, %s)
    """

    return run_command(sql, (
        data["name"],
        data["email"],
        blank_to_none(data.get("address")),
        data.get("tier", "normal")
    ))


def update_customer(cust_id, data):
    sql = """
        UPDATE customer
        SET name=%s, email=%s, address=%s, tier=%s
        WHERE cust_id=%s
    """

    return run_command(sql, (
        data["name"],
        data["email"],
        blank_to_none(data.get("address")),
        data["tier"],
        cust_id
    ))


def delete_customer(cust_id):
    # ตารางที่มี ON DELETE CASCADE จะถูกจัดการโดยฐานข้อมูล
    # หากลูกค้ามีออเดอร์อยู่ อาจต้องจัดการออเดอร์ก่อน
    return run_command(
        "DELETE FROM customer WHERE cust_id = %s",
        (cust_id,)
    )


# ============================================================
# 2. PRODUCT
# ============================================================

def search_products(filters):
    sql = "SELECT * FROM product WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("category"):
        sql += " AND category = %s"
        params.append(filters["category"])

    sql += " ORDER BY product_id"
    return run_query(sql, params)


def get_product(product_id):
    rows = run_query(
        "SELECT * FROM product WHERE product_id = %s",
        (product_id,)
    )
    return rows[0] if rows else None


def create_product(data):
    sql = """
        INSERT INTO product (name, category, price, stock)
        VALUES (%s, %s, %s, %s)
    """

    return run_command(sql, (
        data["name"],
        data["category"],
        data["price"],
        data["stock"]
    ))


def update_product(product_id, data):
    sql = """
        UPDATE product
        SET name=%s, category=%s, price=%s, stock=%s
        WHERE product_id=%s
    """

    return run_command(sql, (
        data["name"],
        data["category"],
        data["price"],
        data["stock"],
        product_id
    ))


def delete_product(product_id):
    # หากสินค้าถูกอ้างอิงในออเดอร์ ตะกร้า หรือรีวิว
    # ฐานข้อมูลอาจปฏิเสธการลบตาม Foreign Key
    return run_command(
        "DELETE FROM product WHERE product_id = %s",
        (product_id,)
    )


# ============================================================
# 3. CUSTOMER_ADDRESS
# ============================================================

def search_customer_addresses(filters):
    sql = """
        SELECT ca.*, c.name AS customer_name
        FROM customer_address ca
        INNER JOIN customer c ON ca.cust_id = c.cust_id
        WHERE 1=1
    """
    params = []

    if filters.get("cust_id"):
        sql += " AND ca.cust_id = %s"
        params.append(filters["cust_id"])

    if filters.get("province"):
        sql += " AND ca.province = %s"
        params.append(filters["province"])

    sql += " ORDER BY ca.address_id"
    return run_query(sql, params)


def get_customer_address(address_id):
    rows = run_query(
        "SELECT * FROM customer_address WHERE address_id = %s",
        (address_id,)
    )
    return rows[0] if rows else None


def create_customer_address(data):
    sql = """
        INSERT INTO customer_address
        (cust_id, recipient_name, phone, address_detail,
         province, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    return run_command(sql, (
        data["cust_id"],
        data["recipient_name"],
        data["phone"],
        data["address_detail"],
        data["province"],
        data["postal_code"]
    ))


def update_customer_address(address_id, data):
    sql = """
        UPDATE customer_address
        SET cust_id=%s, recipient_name=%s, phone=%s,
            address_detail=%s, province=%s, postal_code=%s
        WHERE address_id=%s
    """

    return run_command(sql, (
        data["cust_id"],
        data["recipient_name"],
        data["phone"],
        data["address_detail"],
        data["province"],
        data["postal_code"],
        address_id
    ))


def delete_customer_address(address_id):
    # ออเดอร์ที่ใช้ที่อยู่นี้จะมี address_id เป็น NULL
    # ตาม ON DELETE SET NULL ใน Schema
    return run_command(
        "DELETE FROM customer_address WHERE address_id = %s",
        (address_id,)
    )


# ============================================================
# 4. SHOP_ORDER
# ============================================================

def search_orders(filters):
    sql = """
        SELECT
            o.order_id,
            o.cust_id,
            c.name AS customer_name,
            o.address_id,
            o.order_date,
            o.status,
            IFNULL(t.total, 0) AS total
        FROM shop_order o
        INNER JOIN customer c ON o.cust_id = c.cust_id
        LEFT JOIN (
            SELECT
                order_id,
                SUM(qty * unit_price) AS total
            FROM order_line
            GROUP BY order_id
        ) t ON o.order_id = t.order_id
        WHERE 1=1
    """
    params = []

    if filters.get("cust_id"):
        sql += " AND o.cust_id = %s"
        params.append(filters["cust_id"])

    if filters.get("status"):
        sql += " AND o.status = %s"
        params.append(filters["status"])

    sql += " ORDER BY o.order_id DESC"
    return run_query(sql, params)


def get_order(order_id):
    rows = run_query(
        "SELECT * FROM shop_order WHERE order_id = %s",
        (order_id,)
    )
    return rows[0] if rows else None


def check_can_ship(order_id):
    """จัดส่งได้เฉพาะออเดอร์ที่มีการชำระเงินสถานะ paid"""

    rows = run_query("""
        SELECT EXISTS (
            SELECT 1
            FROM payment
            WHERE order_id = %s
              AND status = 'paid'
        ) AS paid
    """, (order_id,))

    if not rows or not rows[0]["paid"]:
        raise ValueError(
            "ออเดอร์นี้ยังไม่ได้ชำระเงิน จัดส่งไม่ได้"
        )


def create_order(data):
    if data.get("status") == "shipped":
        raise ValueError(
            "ออเดอร์ใหม่ยังไม่ได้ชำระเงิน จัดส่งไม่ได้"
        )

    address_id = blank_to_none(data.get("address_id"))

    sql = """
        INSERT INTO shop_order
        (cust_id, address_id, order_date, status)
        VALUES (%s, %s, %s, %s)
    """

    return run_command(sql, (
        data["cust_id"],
        address_id,
        blank_to_none(data.get("order_date")),
        data.get("status", "pending")
    ))


def update_order(order_id, data):
    if data.get("status") == "shipped":
        check_can_ship(order_id)

    sql = """
        UPDATE shop_order
        SET cust_id=%s, address_id=%s, order_date=%s, status=%s
        WHERE order_id=%s
    """

    return run_command(sql, (
        data["cust_id"],
        blank_to_none(data.get("address_id")),
        blank_to_none(data.get("order_date")),
        data["status"],
        order_id
    ))


def delete_order(order_id):
    """ห้ามลบออเดอร์ที่มีรายการชำระเงิน"""

    rows = run_query("""
        SELECT EXISTS (
            SELECT 1 FROM payment WHERE order_id = %s
        ) AS has_payment
    """, (order_id,))

    if rows and rows[0]["has_payment"]:
        raise ValueError("ออเดอร์นี้มีข้อมูลการชำระเงิน ลบไม่ได้")

    # ลบรายการสินค้าในออเดอร์ก่อน
    run_command(
        "DELETE FROM order_line WHERE order_id = %s",
        (order_id,)
    )

    return run_command(
        "DELETE FROM shop_order WHERE order_id = %s",
        (order_id,)
    )


# ============================================================
# 5. ORDER_LINE
# ============================================================

def search_order_lines(filters):
    sql = """
        SELECT
            ol.order_id,
            ol.product_id,
            p.name AS product_name,
            ol.qty,
            ol.unit_price,
            ol.qty * ol.unit_price AS subtotal
        FROM order_line ol
        INNER JOIN product p ON ol.product_id = p.product_id
        WHERE 1=1
    """
    params = []

    if filters.get("order_id"):
        sql += " AND ol.order_id = %s"
        params.append(filters["order_id"])

    if filters.get("product_id"):
        sql += " AND ol.product_id = %s"
        params.append(filters["product_id"])

    sql += " ORDER BY ol.order_id, ol.product_id"
    return run_query(sql, params)


def create_order_line(data):
    sql = """
        INSERT INTO order_line
        (order_id, product_id, qty, unit_price)
        VALUES (%s, %s, %s, %s)
    """

    return run_command(sql, (
        data["order_id"],
        data["product_id"],
        data["qty"],
        data["unit_price"]
    ))


def update_order_line(order_id, product_id, data):
    sql = """
        UPDATE order_line
        SET qty=%s, unit_price=%s
        WHERE order_id=%s AND product_id=%s
    """

    return run_command(sql, (
        data["qty"],
        data["unit_price"],
        order_id,
        product_id
    ))


def delete_order_line(order_id, product_id):
    return run_command("""
        DELETE FROM order_line
        WHERE order_id=%s AND product_id=%s
    """, (order_id, product_id))


# ============================================================
# 6. PAYMENT
# ============================================================

def search_payments(filters):
    sql = """
        SELECT
            p.*,
            o.cust_id,
            c.name AS customer_name
        FROM payment p
        INNER JOIN shop_order o ON p.order_id = o.order_id
        INNER JOIN customer c ON o.cust_id = c.cust_id
        WHERE 1=1
    """
    params = []

    if filters.get("order_id"):
        sql += " AND p.order_id = %s"
        params.append(filters["order_id"])

    if filters.get("status"):
        sql += " AND p.status = %s"
        params.append(filters["status"])

    if filters.get("method"):
        sql += " AND p.method = %s"
        params.append(filters["method"])

    sql += " ORDER BY p.payment_id"
    return run_query(sql, params)


def get_payment(payment_id):
    rows = run_query(
        "SELECT * FROM payment WHERE payment_id = %s",
        (payment_id,)
    )
    return rows[0] if rows else None


def create_payment(data):
    sql = """
        INSERT INTO payment
        (order_id, method, amount, status, paid_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    status = data.get("status", "pending")
    paid_date = blank_to_none(data.get("paid_date"))

    if status == "paid" and not paid_date:
        # หากไม่ได้ระบุวัน ให้ใช้เวลาปัจจุบัน
        sql = """
            INSERT INTO payment
            (order_id, method, amount, status, paid_date)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        params = (
            data["order_id"],
            data["method"],
            data["amount"],
            status
        )
    else:
        params = (
            data["order_id"],
            data["method"],
            data["amount"],
            status,
            paid_date
        )

    return run_command(sql, params)


def update_payment(payment_id, data):
    sql = """
        UPDATE payment
        SET order_id=%s, method=%s, amount=%s,
            status=%s, paid_date=%s
        WHERE payment_id=%s
    """

    return run_command(sql, (
        data["order_id"],
        data["method"],
        data["amount"],
        data["status"],
        blank_to_none(data.get("paid_date")),
        payment_id
    ))


def delete_payment(payment_id):
    return run_command(
        "DELETE FROM payment WHERE payment_id = %s",
        (payment_id,)
    )


# ============================================================
# 7. REVIEW
# ============================================================

def search_reviews(filters):
    sql = """
        SELECT
            r.*,
            c.name AS customer_name,
            p.name AS product_name
        FROM review r
        INNER JOIN customer c ON r.cust_id = c.cust_id
        INNER JOIN product p ON r.product_id = p.product_id
        WHERE 1=1
    """
    params = []

    if filters.get("cust_id"):
        sql += " AND r.cust_id = %s"
        params.append(filters["cust_id"])

    if filters.get("product_id"):
        sql += " AND r.product_id = %s"
        params.append(filters["product_id"])

    if filters.get("rating"):
        sql += " AND r.rating = %s"
        params.append(filters["rating"])

    sql += " ORDER BY r.review_date DESC"
    return run_query(sql, params)


def create_review(data):
    sql = """
        INSERT INTO review
        (cust_id, product_id, rating, comment, review_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    return run_command(sql, (
        data["cust_id"],
        data["product_id"],
        data["rating"],
        blank_to_none(data.get("comment")),
        blank_to_none(data.get("review_date"))
    ))


def update_review(cust_id, product_id, data):
    sql = """
        UPDATE review
        SET rating=%s, comment=%s
        WHERE cust_id=%s AND product_id=%s
    """

    return run_command(sql, (
        data["rating"],
        blank_to_none(data.get("comment")),
        cust_id,
        product_id
    ))


def delete_review(cust_id, product_id):
    return run_command("""
        DELETE FROM review
        WHERE cust_id=%s AND product_id=%s
    """, (cust_id, product_id))


# ============================================================
# 8. CART
# ============================================================

def search_carts(filters):
    sql = """
        SELECT ca.*, c.name AS customer_name
        FROM cart ca
        INNER JOIN customer c ON ca.cust_id = c.cust_id
        WHERE 1=1
    """
    params = []

    if filters.get("cust_id"):
        sql += " AND ca.cust_id = %s"
        params.append(filters["cust_id"])

    sql += " ORDER BY ca.cart_id"
    return run_query(sql, params)


def get_cart(cart_id):
    rows = run_query(
        "SELECT * FROM cart WHERE cart_id = %s",
        (cart_id,)
    )
    return rows[0] if rows else None


def create_cart(data):
    sql = """
        INSERT INTO cart (cust_id, created_at)
        VALUES (%s, %s)
    """

    return run_command(sql, (
        data["cust_id"],
        blank_to_none(data.get("created_at"))
    ))


def update_cart(cart_id, data):
    sql = """
        UPDATE cart
        SET cust_id=%s
        WHERE cart_id=%s
    """

    return run_command(sql, (
        data["cust_id"],
        cart_id
    ))


def delete_cart(cart_id):
    # cart_item จะถูกลบตาม ON DELETE CASCADE
    return run_command(
        "DELETE FROM cart WHERE cart_id = %s",
        (cart_id,)
    )


# ============================================================
# 9. CART_ITEM
# ============================================================

def search_cart_items(filters):
    sql = """
        SELECT
            ci.cart_id,
            ci.product_id,
            p.name AS product_name,
            p.price,
            ci.qty,
            ci.qty * p.price AS subtotal
        FROM cart_item ci
        INNER JOIN product p ON ci.product_id = p.product_id
        WHERE 1=1
    """
    params = []

    if filters.get("cart_id"):
        sql += " AND ci.cart_id = %s"
        params.append(filters["cart_id"])

    if filters.get("product_id"):
        sql += " AND ci.product_id = %s"
        params.append(filters["product_id"])

    sql += " ORDER BY ci.cart_id, ci.product_id"
    return run_query(sql, params)


def create_cart_item(data):
    sql = """
        INSERT INTO cart_item (cart_id, product_id, qty)
        VALUES (%s, %s, %s)
    """

    return run_command(sql, (
        data["cart_id"],
        data["product_id"],
        data["qty"]
    ))


def update_cart_item(cart_id, product_id, data):
    sql = """
        UPDATE cart_item
        SET qty=%s
        WHERE cart_id=%s AND product_id=%s
    """

    return run_command(sql, (
        data["qty"],
        cart_id,
        product_id
    ))


def delete_cart_item(cart_id, product_id):
    return run_command("""
        DELETE FROM cart_item
        WHERE cart_id=%s AND product_id=%s
    """, (cart_id, product_id))


# ============================================================
# REPORT 1: DASHBOARD SUMMARY
# ============================================================

def report_summary():
    sql = """
        SELECT
            (SELECT COUNT(*) FROM customer) AS 'ลูกค้า',
            (SELECT COUNT(*) FROM product) AS 'สินค้า',
            (SELECT COUNT(*) FROM shop_order) AS 'ออเดอร์',
            (SELECT COUNT(*) FROM review) AS 'รีวิว',
            (SELECT COUNT(*) FROM customer
                WHERE tier = 'vip') AS 'VIP',
            (SELECT IFNULL(SUM(amount), 0)
                FROM payment
                WHERE status = 'paid') AS 'ยอดชำระเงินรวม',
            (SELECT COUNT(*) FROM cart) AS 'ตะกร้าสินค้า',
            (SELECT COUNT(*) FROM customer_address) AS 'ที่อยู่ลูกค้า'
    """

    return run_query(sql)[0]


# ============================================================
# REPORT 2: BEST SELLING PRODUCTS
# ============================================================

def report_best_selling():
    sql = """
        SELECT
            p.product_id,
            p.name AS product_name,
            SUM(ol.qty) AS total_qty
        FROM order_line ol
        INNER JOIN product p ON ol.product_id = p.product_id
        INNER JOIN shop_order so ON ol.order_id = so.order_id
        WHERE so.status != 'cancelled'
        GROUP BY p.product_id, p.name
        ORDER BY total_qty DESC
        LIMIT 5
    """

    return run_query(sql)


# ============================================================
# REPORT 3: CUSTOMERS ABOVE AVERAGE SPENDING
# ============================================================

def report_customers_above_avg():
    sql = """
        SELECT
            c.cust_id,
            c.name AS customer_name,
            SUM(ol.qty * ol.unit_price) AS total_spent
        FROM shop_order so
        INNER JOIN order_line ol ON so.order_id = ol.order_id
        INNER JOIN customer c ON so.cust_id = c.cust_id
        WHERE so.status != 'cancelled'
        GROUP BY c.cust_id, c.name
        HAVING total_spent > (
            SELECT AVG(customer_total)
            FROM (
                SELECT
                    so2.cust_id,
                    SUM(ol2.qty * ol2.unit_price) AS customer_total
                FROM shop_order so2
                INNER JOIN order_line ol2
                    ON so2.order_id = ol2.order_id
                WHERE so2.status != 'cancelled'
                GROUP BY so2.cust_id
            ) AS avg_spending
        )
        ORDER BY total_spent DESC
    """

    return run_query(sql)


# ============================================================
# REPORT 4: HIGH-RATED PRODUCTS
# ============================================================

def report_high_rated():
    sql = """
        SELECT
            p.product_id,
            p.name AS product_name,
            AVG(r.rating) AS avg_rating,
            COUNT(r.rating) AS review_count
        FROM review r
        INNER JOIN product p ON r.product_id = p.product_id
        GROUP BY p.product_id, p.name
        HAVING AVG(r.rating) >= 4
        ORDER BY avg_rating DESC
    """

    return run_query(sql)


# ============================================================
# REPORTS LIST
# ============================================================

REPORTS = [
    (
        "best-selling",
        "📈 สินค้าขายดี (Best Sellers)",
        report_best_selling
    ),
    (
        "top-customers",
        "🏅 ลูกค้าที่ซื้อมากกว่าค่าเฉลี่ย (Above Average)",
        report_customers_above_avg
    ),
    (
        "high-rated",
        "⭐ สินค้าคะแนนรีวิวเฉลี่ย ≥ 4",
        report_high_rated
    ),
]