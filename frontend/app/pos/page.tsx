"use client";
import { useState } from "react";
import { useEffect } from "react";
import styles from "./page.module.css";

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
  const [bookQuery, setBookQuery] = useState("");
  const [cart, setCart] = useState<CartItem[]>([]);
  const [taxRate, setTaxRate] = useState<number | null>(null);

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const discountRate = customer ?customer.discount_rate / 100 : 0;
  const discount = Math.floor(subtotal * discountRate);
  const tax = Math.floor((subtotal - discount) * taxRate);
  const total = subtotal - discount + tax;

  useEffect( () => {
    const loadTax = async () => {
        const res = await fetch("http://127.0.0.1:8000/tax");
        const data = await res.json();
        setTaxRate(data.tax);
    };
    loadTax();
}, []);

  const searchCustomerRate = async () => {
    const res = await fetch(`http://127.0.0.1:8000/customer/rate/{id}?customer_id=${customerIdQuery}`);
    const data: Customer = await res.json();
    setCustomer(data);
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
    const res = await fetch(`http://127.0.0.1:8000/books/${bookQuery}`);
    if (!res.ok) {
        return;
    }
    const data:Book = await res.json();
    console.log(data);
    addToCart(data);
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

  const sumTotal = () => {

  }

  return (
    <div>
        <p>ログインID</p>
        <h1>テクゼロンPSOシステム</h1>
        <p>会員</p>
        <input
          value={customerIdQuery}
          onChange={(e) => setCustomerIdQuery(e.target.value)}
          placeholder="会員IDを入力してください"
        />
      <button onClick={searchCustomerRate}>取得</button>
      <p>会員ID：{customer && customer.customer_id}</p>
      <p>割引率：{customer && customer.discount_rate}%</p>

        <p>書籍検索</p>
        <input
          value={bookQuery}
          onChange={(e) => setBookQuery(e.target.value)}
          placeholder="ISBNを入力してください"
        />
      <button onClick={searchAndAddCart}>取得</button>
      <h2>購入リスト</h2>
        <div>
          <ul>
            {cart.map((item) => (
              <li key={item.ISBN}>
                {item.ISBN}: {item.book_name} / {item.price}円 / {item.quantity}
                <button onClick={() => changeQuantity(item.ISBN, 1)}>+</button>
                <button onClick={() => changeQuantity(item.ISBN, -1)}>-</button>
                <button onClick={() => removeItem(item.ISBN)}>削除</button>
              </li>
            ))}
          </ul>
        </div>
        <p>小計:{subtotal.toLocaleString()}円</p> 
        <p>消費税:{tax.toLocaleString()}円</p>
        <p>割引額:{discount.toLocaleString()}円</p>
        <p>合計:{total.toLocaleString()}円</p>
    </div>
  );
}
