"use client";
import { useState } from "react";
import { useEffect } from "react";
import BarcodeScanner from "../_components/BarcodeScanner";

type Customer = {
    customer_id: number,
    discount_rate: number
}

type Book = {
    ISBN: string,
    book_id: number,
    book_name: string,
    price: number
}

type CartItem = Book & {quantity: number}

export default function Home() {
  const [customerIdQuery, setCustomerIdQuery] = useState("");
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [taxRate, setTaxRate] = useState<number | null>(null);
  const [isbnInput, setIsbnInput] = useState("");
  const [isScanning, setIsScanning] = useState(false);

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const discountRate = customer ?customer.discount_rate / 100 : 0;
  const discount = Math.floor(subtotal * discountRate);
  const tax = Math.floor((subtotal - discount) * (taxRate / 100));
  const total = subtotal - discount + tax;

  useEffect( () => {
    const loadTax = async () => {
        const res = await fetch("http://127.0.0.1:8000/tax");
        const data = await res.json();
        setTaxRate(data.tax);
    };
    loadTax();
}, []);

  const handleDetected = (isbn: string) => {
  setIsbnInput(isbn);
  setIsScanning(false);
  };

  const searchCustomerRate = async () => {
    if (customerIdQuery == "") { alert("会員IDを入力してください"); return; }
    const res = await fetch(`http://127.0.0.1:8000/customer/rate/{id}?customer_id=${customerIdQuery}`);
    const data: Customer = await res.json();
    if (!res.ok) {
        alert(data.detail);
        setCustomer(null);
        setCustomerIdQuery("");
        return;
    }
    setCustomer(data);
    setCustomerIdQuery("");
  }

  const addToCart = (book: Book) => {
    setCart((prev) => {
        const exists = prev.find((item) => item.ISBN === book.ISBN);
        if (exists) {
            return prev.map((item) => 
                item.ISBN === book.ISBN
                ? {...item, quantity: item.quantity + 1}
                : item
            );
        }
        return [...prev, {...book, quantity:1}];
    });
  };

  const searchAndAddCart = async () => {
    if (!isbnInput) {alert("ISBNを入力してください"); return;}
    const res = await fetch(`http://127.0.0.1:8000/books/${isbnInput}`);
    if (!res.ok) {
        return;
    }
    const data:Book = await res.json();
    addToCart(data);
    setIsbnInput("");
  }

  const changeQuantity = (isbn: string, diff: number) => {
    setCart((prev) => 
        prev.map((item) => 
            item.ISBN === isbn
            ? {...item, quantity: Math.max(1, item.quantity + diff)}
            : item
        )
    );
  };

  const removeItem = (isbn: string) => {
    setCart((prev) => prev.filter((item) => item.ISBN !== isbn));
  };

  const PurchaseItems = async () => {
    if (cart.length === 0){alert("カートの中身がありません。"); return;}
    const items = cart.map((item) => ({isbn: item.ISBN, quantity: item.quantity}))
    const customerId = customer ? customer.customer_id : null
    const json = JSON.stringify({customer_id: customerId, user_id: 1, items})
    const res = await fetch("http://127.0.0.1:8000/orders", {
        method: "POST",
        body: json,
        headers: {
            "Content-Type": "application/json",
        },
    });
    const data = await res.json();
    if (!res.ok) {
        alert(data.detail);
        return;
    }
    alert(`${data.detail}（注文番号: ${data.order_id}）`);
    setCart([]);
    setCustomer(null);
  };

  return (
    <main className="min-h-screen bg-gray-100 p-4">
         <div className="mx-auto max-w-md md:max-w-2xl space-y-4 rounded-lg border border-gray-300 bg-white p-4 shadow-sm">
            <div className="flex justify-end">
                <span className="rounded border border-gray-400 px-3 py-1 text-sm">ログインID</span>
            </div>
            <h1 className="text-center text-2xl font-bold">テクゼロン書店POS</h1>
            <div className="flex items-center gap-2">
                <input
                value={customerIdQuery}
                onChange={(e) => setCustomerIdQuery(e.target.value)}
                placeholder="会員IDを入力してください"
                className="w-48 rounded border border-gray-400 px-2 py-1 text-sm"
                />
                <button 
                onClick={searchCustomerRate}
                className="cursor-pointer rounded bg-gray-200 px-3 py-1 text-sm hover:bg-gray-300"
                >
                取得
                </button>
          <div 
          className={`flex-1 rounded border border-gray-400 px-2 py-1 text-center text-sm
          ${customer ? "font-bold text-gray-900" : "text-gray-400"}`}>
            {customer
            ? `ID: ${customer.customer_id} / 割引: ${customer.discount_rate}%引き`
            : "会員ID / 割引"}
          </div>
        </div>
        <div className="flex items-center justify-end gap-2">
            <input
            value={isbnInput}
            onChange={(e) => setIsbnInput(e.target.value)}
            placeholder="ISBNを入力してください"
            className="w-48 rounded border border-gray-400 px-2 py-1 text-sm"
            />
            <button
                onClick={() => setIsScanning(true)}
                className="cursor-pointer rounded border border-gray-400 px-2 py-1 text-sm hover:bg-gray-100"
            >
                📷
            </button>
            {isScanning && (
                <BarcodeScanner onDetected={handleDetected} onClose={() => setIsScanning(false)} />
            )}
            <button
                onClick={searchAndAddCart}
                className="cursor-pointer rounded border border-gray-400 px-2 py-1 text-sm hover:bg-gray-100"
            >
                取得
            </button>
        </div>
        <section className="rounded border border-gray-400 p-3">
        <h2 className="mb-2 text-center font-bold">購入リスト</h2>
            <ul className="space-y-2">
                {cart.map((item) => (
                <li key={item.ISBN} className="flex items-center gap-2">
                <div className="min-w-0 flex-1 rounded border border-gray-300 px-2 py-1">
                  <p className="min-w-0 flex-1 rounded border border-gray-300 px-2 py-1">{item.ISBN}</p>
                  <p className="truncate text-sm">{item.book_name}</p>
                  <p className="text-xs text-gray-500">
                    {item.ISBN} / ¥{item.price.toLocaleString()} / {item.quantity}冊
                  </p>
                </div>

                    <button 
                        onClick={() => changeQuantity(item.ISBN, 1)}
                        className="h-8 w-8 cursor-pointer rounded border border-gray-400 hover:bg-gray-100"
                    >
                        +
                    </button>
                    <button
                        onClick={() => changeQuantity(item.ISBN, -1)}
                        className="h-8 w-8 cursor-pointer rounded border border-gray-400 hover:bg-gray-100"
                    >
                        -
                    </button>
                    <button
                        onClick={() => removeItem(item.ISBN)}
                        className="cursor-pointer rounded border border-red-300 px-2 py-1 text-sm text-red-600 hover:bg-red-50"
                    >
                        削除
                    </button>
                </li>
                ))}
            </ul>
            </section>
        <section className="space-y-1 rounded border border-gray-400 p-3 text-sm">
          <div className="flex justify-between">
            <span>小計</span>
            <span>¥{subtotal.toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span>消費税</span>
            <span>¥{tax.toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span>割引</span>
            <span>-¥{discount.toLocaleString()}</span>
          </div>
          <div className="flex justify-between border-t border-gray-300 pt-2 text-lg font-bold">
            <span>合計金額</span>
            <span>¥{total.toLocaleString()}</span>
          </div>
        </section>
        <div className="flex items-end justify-between">
          <span className="rounded border border-gray-400 px-3 py-1 text-sm">
            税率 {taxRate}%
          </span>
          <button
            onClick={PurchaseItems}
            className="cursor-pointer rounded bg-blue-600 px-8 py-3 font-bold text-white hover:bg-blue-700"
          >
          決済
          </button>
        </div>
        </div>
    </main>
  );
}
