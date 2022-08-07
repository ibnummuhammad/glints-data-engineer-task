deploy:
	docker-compose up -d

setup:
	$(eval POSTGRES_SRC_IP= $(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_src))
	$(eval POSTGRES_DST_IP= $(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_dst))
	docker exec -it --user airflow airflow-webserver airflow connections add 'postgres_src' --conn-type 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-host '$(POSTGRES_SRC_IP)' --conn-port '5432'
	docker exec -it --user airflow airflow-webserver airflow connections add 'postgres_dst' --conn-type 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-host '$(POSTGRES_DST_IP)' --conn-port '5432'
	docker exec -it postgres_src psql -d airflow -U airflow -c "CREATE TABLE IF NOT EXISTS sales(id SERIAL,quantity INT,price INT,date DATE,PRIMARY KEY (id));"
	docker exec -it postgres_src psql -d airflow -U airflow -c "COPY sales(id, quantity, price, date) FROM '/opt/data/sales_september_2019.csv' DELIMITER ',' CSV HEADER;"

stop:
	docker-compose down