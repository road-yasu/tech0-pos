# backend（テクゼロン書店POS API）

FastAPI ＋ SQLAlchemy ＋ MySQL（Azure）。

## 準備

```bash
cd backend
source venv/bin/activate
```

`backend/.env` に次の値を設定する（gitには入れない）。

| キー | 内容 |
| --- | --- |
| `HOST_NAME` / `PORT` / `DB_NAME` | MySQLの接続先 |
| `USER_NAME` / `PASSWORD` | MySQLのユーザーとパスワード |
| `JWT_SECRET_KEY` | JWTの署名用の秘密鍵。`python -c "import secrets; print(secrets.token_hex(32))"` で作る |
| `JWT_EXPIRE_MINUTES` | ログインの有効期限（分） |

## データ登録：`seed.py`

CSVからまとめて登録する。Azureのコンソールを開かずに済む。

```bash
python seed.py <books|users|customers> <CSVのパス>
# 例
python seed.py books seed_data/books.csv
```

- 同じデータがすでにある行は**スキップ**して、新しい行だけを登録する。何度実行しても二重登録にはならない
- 途中でエラーが出たら全体を取り消す（1件も登録されない）。CSVを直して、そのまま実行し直せばよい
- 最後に「登録 n件 / スキップ m件」と表示される

### CSVの形

1行目は列名にする。**カンマの後ろにスペースを入れない**（スペースも値の一部として読まれる）。

| テーブル | 列名（1行目） | 重複とみなす条件 |
| --- | --- | --- |
| books | `isbn,book_name,price` | 同じ `isbn` |
| users | `user_name,password` | 同じ `user_name` |
| customers | `customer_name,phone_number,address,sex,age,discount_rate` | 同じ `phone_number` |

- users の `password` は平文で書く。登録するときに `hash_password` で変換して `password_hash` に保存する
- customers の `phone_number` は書き方をそろえる（`090-1234-5678` と `09012345678` は別の番号として扱われる）

### 注意

- CSVは `backend/seed_data/` に置く。このフォルダは `.gitignore` で除外している（users.csv に平文のパスワードが入るため）
- 書き込み先は**Azureの本番のDB**。初めて使うCSVは、1〜2行で試してから全件を流す
- CSVを**Excelで開いて保存しない**。ISBNが `9.78406E+12` のような表示になって壊れ、電話番号は先頭の `0` が消える。VS Code などのテキストエディタで編集する
- Excelで作る場合は「CSV UTF-8」で保存する（普通の「CSV」は文字化けする）
- `customer_id = 1` は非会員用（`main.py` の `GUEST_CUSTOMER_ID`）。消さない

## データ確認：`check.py`

テーブルの全行を表示する。読むだけなので、何度実行しても安全。

```bash
python check.py <テーブル名>
# 例
python check.py books
```

指定できる名前：`users` / `books` / `customers` / `tax` / `orders` / `order_details` / `loginlogs`

- 引数なしで実行すると、使い方が表示される
- `users` の `password_hash` は表示しない
- 会員の名前・電話番号・住所も表示される。画面を共有するときは注意する
