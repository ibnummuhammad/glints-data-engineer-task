start:
	docker-compose up -d

setup:
	$(eval POSTGRES_SRC_IP= $(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_src))
	$(eval POSTGRES_DST_IP= $(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_dst))
	docker exec -it --user airflow airflow-webserver airflow connections add 'postgres_src' --conn-type 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-host '$(POSTGRES_SRC_IP)' --conn-port '5432'
	docker exec -it --user airflow airflow-webserver airflow connections add 'postgres_dst' --conn-type 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-host '$(POSTGRES_DST_IP)' --conn-port '5432'
	docker exec -it postgres_src psql -d airflow -U airflow -f /opt/query/create_table.sql
	docker exec -it postgres_src psql -d airflow -U airflow -f /opt/query/import_table.sql
	docker exec -it postgres_dst psql -d airflow -U airflow -f /opt/query/create_table.sql

inspect:
	docker exec -it postgres_dst psql -d airflow -U airflow -f /opt/query/select_table.sql

stop:
	docker-compose down