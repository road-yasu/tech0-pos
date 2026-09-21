from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def hello():
    return {"message": "hello"}

@app.get("/tax")
def get_tax():
    return {"tax_rate": 10}

@app.get("/books/{ISBN}")
def get_book(ISBN):
    if ISBN == "9784865933444":
        return {
            "id": 1,
            "ISBN": "9784865933444",
            "book_name": "黄金比率",
            "price": 900,
        }
    return {
        "error_code": "404",
        "message": "該当の書籍が見つかりませんでした"
    }