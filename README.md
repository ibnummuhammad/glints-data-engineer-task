# glints-data-engineer-task
This is a home assignment task for Data Engineer role at Glints.

# Requirements
* Linux environment
* Docker

# How to Run
Before we can run the Airflow, we need to do some preparation.

## 1. Deploy containers
Deploy the docker containers by running code below.

    make start

This command will compose up the docker container, then deploy the necessary services. You should see the containers status like below.

    CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                   PORTS                              NAMES
    84e271291563   apache/airflow:2.3.0   "/usr/bin/dumb-init …"   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5884->8080/tcp             airflow-webserver
    08618ce7794a   apache/airflow:2.3.0   "/usr/bin/dumb-init …"   2 minutes ago   Up 2 minutes             8080/tcp, 0.0.0.0:8793->8793/tcp   airflow-scheduler
    9bc3f7682fe2   postgres:13            "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes (healthy)   5432/tcp                           postgres_src
    f59365d819ad   postgres:13            "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:5434->5432/tcp             postgres
    a4b957de7db5   postgres:13            "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes (healthy)   5432/tcp                           postgres_dst

## 2. Set up initial preparation
Set-up some initial preparation, such as table data source and airflow postgres connections.

    make setup

This command will set neccesary initialization in order to make the airflow data pipeline works automatically.

## 3. Inspect the data output
When the data extraction is done, we can inspect the output data by running the code below.

    make inspect

We can inspect the output data that has been stored in the postgres destination database with the expected output data as below.

     id | quantity | price |    date    
    ----+----------+-------+------------
      1 |        1 |    11 | 2019-09-01
      2 |        1 |    14 | 2019-09-02
      3 |        1 |   150 | 2019-09-03
      4 |        1 |     2 | 2019-09-04
      5 |        1 |    11 | 2019-09-05
      6 |        1 |   400 | 2019-09-06
      7 |        1 |    14 | 2019-09-07
      8 |        1 |   700 | 2019-09-08
      9 |        1 |   149 | 2019-09-12
     10 |        1 |    11 | 2019-09-13
     11 |        1 |   150 | 2019-09-14
     12 |        1 |    14 | 2019-09-15
     13 |        1 |    11 | 2019-09-16
     14 |        4 |     3 | 2019-09-17
     15 |        1 |    99 | 2019-09-18
     16 |        1 |    11 | 2019-09-22
     17 |        1 |   109 | 2019-09-23
     18 |        1 |    11 | 2019-09-24

## 4. Stop the services
After everything is done, we can shut down our services by executing the code below.

    make stop