from datetime import datetime, date

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, Book, Tax, Customer

app = FastAPI()

@app.get('/hello')
def hello():
    return {"message": "hello"}

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
        "id": f.book_id,
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