import math
from datetime import datetime
from security import verify_password
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from models import User, Book, Tax, Customer, Order, OrderDetail, LoginLogs
from schemas import OrderRequest, LoginRequest

GUEST_CUSTOMER_ID = 1 # 非会員のID

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/hello')
def hello():
    return {"message": "hello"}

@app.post('/login')
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    # 1. user_name で User を1件検索する
    user = db.query(User).filter(User.user_name == req.user_name).first()
    # 2. 見つからない、または verify_password が False なら
    #    401エラー「IDまたはパスワードが違います」
    if user is None or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="名前またはパスワードが違います")
    # 3. LoginLog を保存する（IPは request.client.host で取れます）
    db.add(
        LoginLogs(
            user_id = user.user_id,
            ip_address = request.client.host if request.client else None,
        )
    )
    db.commit()
    # 4. user_id と user_name を返す
    return {"user_id": user.user_id, "user_name": user.user_name}

@app.get("/tax")
def get_tax(db: Session = Depends(get_db)):
    now = datetime.now()
    f = db.query(Tax).where(Tax.start_at <= now, Tax.finish_at >= now).first()
    if not f:
        raise HTTPException(status_code=404, detail="見つかりません。")
    return {
        "tax": f.tax_rate
    }

@app.get("/books/{ISBN}")
def get_book(ISBN: str, db: Session = Depends(get_db)):
    if len(ISBN) != 13:
        raise HTTPException(status_code=422, detail="ISBNの桁数が違います。")
    f = db.query(Book).filter(Book.isbn == ISBN).first()
    if not f:
        raise HTTPException(status_code=404, detail="書籍が見つかりません。")
    return {
        "book_id": f.book_id,
        "ISBN": f.isbn,
        "book_name": f.book_name,
        "price": f.price,
    }

@app.get("/customer/rate/{id}")
def get_customer_rate(customer_id:int, db:Session = Depends(get_db)):
    if not customer_id:
        raise HTTPException(status_code=422, detail="idがありません。")
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="顧客情報が見つかりません。")
    return {
        "customer_id": customer_id,
        "discount_rate": customer.discount_rate,
    }

@app.post("/orders")
def register_orders(req: OrderRequest, db: Session = Depends(get_db)):
    if not req:
        raise HTTPException(status_code=400, detail="購入リストが空です")
    
    lines = []
    subtotal = 0
    for item in req.items:
        book = db.query(Book).filter(Book.isbn == item.isbn).first()
        if book is None:
            raise HTTPException(status_code=404, detail=f"書籍が見つかりません: {item.ISBN}")
        subtotal += book.price * item.quantity
        lines.append((book, item.quantity))
    
    discount_rate = 0
    customer_id = req.customer_id if req.customer_id is not None else GUEST_CUSTOMER_ID
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="会員が見つかりません")
    discount_rate = customer.discount_rate

    tax_rate = db.query(Tax).order_by(Tax.tax_id.desc()).first().tax_rate

    discount = math.floor(subtotal * (discount_rate / 100))
    tax = math.floor((subtotal - discount) * (tax_rate / 100))
    total = subtotal - discount + tax

    try :
        order = Order(
            customer_id = customer_id,
            user_id = req.user_id,
            subtotal = subtotal,
            discount_rate = discount_rate,
            tax_rate = tax_rate,
            tax_amount = tax,
            total_amount = total,
        )
        db.add(order)
        db.flush()

        for book, qty in lines:
            db.add(OrderDetail(
                order_id=order.order_id,
                book_id=book.book_id,
                price=book.price,
                quantity=qty,
            ))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="登録に失敗しました")
    
    return {"order_id": order.order_id, "total_amount": total, "detail": "登録が完了しました"}