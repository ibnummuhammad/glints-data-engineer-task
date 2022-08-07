CREATE TABLE IF NOT EXISTS sales(
    id SERIAL,
    quantity INT,
    price INT,
    date DATE,
    PRIMARY KEY (id)
);