COPY sales(id, quantity, price, date)
FROM '/opt/data/sales_september_2019.csv' DELIMITER ',' CSV HEADER;