CREATE TABLE IF NOT EXISTS dim_customers(
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE,
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_products(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price NUMERIC
);

CREATE TABLE IF NOT EXISTS fact_orders(
    order_id INT PRIMARY KEY,
    order_timestamp TIMESTAMP,
    customer_id INT REFERENCES dim_customers(customer_id),
    product_id INT REFERENCES dim_products(product_id),
    quantity INT,
    total_amount NUMERIC,
    currency VARCHAR(10),
    status VARCHAR(20)
);

