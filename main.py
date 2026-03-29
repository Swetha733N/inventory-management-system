from db import connect_db

def add_product():
    name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)",
        (name, quantity, price)
    )

    product_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO transactions (product_id, type, quantity) VALUES (%s, %s, %s)",
        (product_id, "IN", quantity)
    )

    db.commit()
    print("✅ Product added!")


def view_products():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()

    print("\n📦 Inventory:")
    for row in results:
        print(row)


def update_stock():
    product_id = int(input("Enter product ID: "))
    change = int(input("Enter quantity (+add / -remove): "))

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE products SET quantity = quantity + %s WHERE product_id = %s",
        (change, product_id)
    )

    t_type = "IN" if change > 0 else "OUT"

    cursor.execute(
        "INSERT INTO transactions (product_id, type, quantity) VALUES (%s, %s, %s)",
        (product_id, t_type, abs(change))
    )

    db.commit()
    print("✅ Stock updated!")


def view_transactions():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT t.transaction_id, p.name, t.type, t.quantity, t.date
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
    """)

    results = cursor.fetchall()

    print("\n📜 Transactions:")
    for row in results:
        print(row)


while True:
    print("\n==== Inventory Management System ====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Stock")
    print("4. View Transactions")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_product()
    elif choice == "2":
        view_products()
    elif choice == "3":
        update_stock()
    elif choice == "4":
        view_transactions()
    elif choice == "5":
        break
    else:
        print("Invalid choice!")