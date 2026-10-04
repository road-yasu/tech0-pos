import sys

from database import SessionLocal
from models import User, Book, Customer, Tax, Order, OrderDetail, LoginLogs

# テーブル名
TABLES = {
    "users": User,
    "books": Book,
    "customers": Customer,
    "tax": Tax,
    "orders": Order,
    "order_details": OrderDetail,
    "loginlogs": LoginLogs,
}

# 画面に出さない列
HIDDEN_COLUMNS = {"password_hash"}


def main():
    if len(sys.argv) != 2:
        print(f"使い方: python check.py <{'|'.join(TABLES)}>")
        return
    model = TABLES.get(sys.argv[1])
    if model is None:
        print(f"未対応のテーブルです: {sys.argv[1]}")
        return

    db = SessionLocal()
    try:
        rows = db.query(model).all()
        columns = [c.name for c in model.__table__.columns
                   if c.name not in HIDDEN_COLUMNS]

        print(f"{sys.argv[1]}: {len(rows)}件")
        print(" | ".join(columns))
        for row in rows:
            print(" | ".join(str(getattr(row, c)) for c in columns))
    finally:
        db.close()


if __name__ == "__main__":
    main()