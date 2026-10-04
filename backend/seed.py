import csv
import sys

from database import SessionLocal
from models import Book, User, Customer
from security import hash_password


def seed_books(db, rows):
    added, skipped = 0, 0
    seen = set()
    for row in rows:
        isbn = row["isbn"].strip()
        exists = db.query(Book).filter(Book.isbn == isbn).first()
        if exists or isbn in seen:
            skipped += 1
            continue
        db.add(Book(
            isbn=isbn,
            book_name=row["book_name"],
            price=int(row["price"]),
        ))
        seen.add(isbn)
        added += 1
    return added, skipped

def seed_users(db, rows):
    added, skipped = 0, 0
    seen = set()
    for row in rows:
        user_name = row["user_name"].strip()
        exists = db.query(User).filter(User.user_name == user_name).first()
        if exists or user_name in seen:
            skipped += 1
            continue
        db.add(User(
            user_name=user_name,
            password_hash=hash_password(row["password"]),
        ))
        seen.add(user_name)
        added += 1
    return added, skipped

def seed_customers(db, rows):
    added, skipped = 0, 0
    seen = set()
    for row in rows:
        phone_number = row["phone_number"].strip()
        exists = db.query(Customer).filter(Customer.phone_number == phone_number).first()
        if exists or phone_number in seen:
            skipped += 1
            continue
        db.add(Customer(
            customer_name=row["customer_name"],
            phone_number=phone_number,
            address=row["address"],
            sex=int(row["sex"]),
            age=int(row["age"]),
            discount_rate=int(row["discount_rate"]),
        ))
        seen.add(phone_number)
        added += 1
    return added, skipped

def main():
    table, csv_path = sys.argv[1], sys.argv[2]
    with open(csv_path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    db = SessionLocal()
    try:
        if table == "books":
            added, skipped = seed_books(db, rows)
        elif table == "users":
            added, skipped = seed_users(db, rows)
        elif table == "customers":
            added, skipped = seed_customers(db, rows)
        else:
            print(f"未対応のテーブルです: {table}")
            return
        db.commit()
        print(f"{table}: 登録 {added}件 / スキップ {skipped}件")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()