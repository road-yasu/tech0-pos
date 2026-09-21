
CREATE TABLE IF NOT EXISTS customers (
  customer_id       INT AUTO_INCREMENT PRIMARY KEY,
  customer_name     VARCHAR(255) NOT NULL,
  phone_number      VARCHAR(255) NOT NULL,
  address           VARCHAR(500) NOT NULL,
  sex               TINYINT(1) NOT NULL,
  age               INT NOT NULL,
  discount_rate     INT NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS users (
  user_id       INT AUTO_INCREMENT PRIMARY KEY,
  user_name     VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tax (
  tax_id       INT AUTO_INCREMENT PRIMARY KEY,
  tax_rate     INT NOT NULL,
  start_at    DATETIME NOT NULL,
  finish_at   DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS books (
  book_id       INT AUTO_INCREMENT PRIMARY KEY,
  isbn          VARCHAR(13) NOT NULL,
  book_name     VARCHAR(255) NOT NULL,
  price         INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS orders (
  order_id       INT AUTO_INCREMENT PRIMARY KEY,
  customer_id    INT NOT NULL,
  user_id        INT NOT NULL,
  ordered_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtotal       INT NOT NULL,
  discount_rate  INT NOT NULL,
  tax_rate       INT NOT NULL,
  tax_amount     INT NOT NULL,
  total_amount   INT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS order_details (
  detail_id  INT AUTO_INCREMENT PRIMARY KEY,
  order_id   INT NOT NULL,
  book_id    INT NOT NULL,
  price      INT NOT NULL,
  quantity   INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;