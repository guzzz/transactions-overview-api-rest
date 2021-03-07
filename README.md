**Project based in API REST - PYTHON/DJANGO**

- A simple API that allows us to register users' transactions and have an overview of how they are using their money.

---

# TRANSACTIONS OVERVIEW API REST 

The main functionalities of this API are:

1. Register an user. The data inputs of each user are name, email (unique) and age.
2. Register a transaction. The data inputs of each transaction are reference (unique), account, date, amount, type, category and user.
3. Return the user's summary by account that shows the balance of the account, total inflow and total outflows.
4. Return the user's summary by category that shows the sum of amounts per transaction category.

---

## Swagger

This API uses Swagger as a documentation tool.

* In this project the root is redirecting to this swagger documentation endpoint. It can be accessed in http://localhost:8000/ 

---

## Endpoints

If you rather use Postman to test the endpoints, they are listed below:

1. **(GET)** **_"/users/"_** - *Returns all users registered.*
2. **(POST)** **_"/users/"_** - *Register new user.*
3. **(GET)** **_"/users/{id}"_** - *Returns a specific user.*
4. **(GET)** **_"/transactions/"_** - *Returns all transactions registered.*
5. **(POST)** **_"/transactions/"_** - *Register new transaction(s). Accepts JSON or list.*
6. **(POST)** **_"/force-bulk-transactions/"_** - *Register new transactions. Only accept lists.*
7. **(GET)** **_"/summary-accounts/{id}/"_** - *Returns the user's summary by account.*
8. **(GET)** **_"/summary-categories/{id}/"_** - *Returns the user's summary by category.*

Observations:

It is possible to use bulk creation in the endpoints: **5** and **6** . The first endpoint (/transactions/) abort all inserts if there are some validation errors, and runs a partial insert if there are some integration errors. The other one (/force-bulk-transactions/), just aborts the failed transactions, running always a partial insert.

---

## Endpoints - EXTRA

Some date filters were implemented in the: **(GET)** **_"/summary-accounts/{id}/"_** endpoint. If there's no requested date range, all transactions would be considered.

Example - Filter by date:

* start_date=2020-01-11
* end_date=2021-02-10

_If you would like, you can use those filters in **Postman**. The Swagger UI, is not displaying filters for this retrieve endpoint._

---

## Utils

I've created 15 Makefile commands to use in this project. However, you'll just need to use 5 of them to run locally:

* **_make setup_**: To set up the entire environment to run the project. Only need to use this command once.
* **_make start_**: Create the project's container and run the project.
* **_make stop_**: Stop the project's container.
* **_make tests_**: Run all tests in the project.
* **_make clean_**: Clean this project's containers, image, volumes and network from your computer. It's recommended to read this Makefile command before you use it, to make sure that you do not have other projects with similar names.

---

## Django Admin

This API model's are also registered on the Django Admin.

_To make it easy to analyse this project... when the project runs for the first time, one super user is automatically created (username:admin, password:transactions1234). You'll have to use this user to access the admin area. If you'ld like, you can create your own super user with the "make createsuperuser" command and delete the previous one in the Django admin._

_Django's admin can be accessed in:_ http://localhost:8000/admin/

---

## Run Locally


1. Make sure you have the Docker and Docker-compose installed.
2. You'll also need to generate one Django **SECRET KEY** and insert it in the **_develop.env_** file. I've already inserted a random secret key in the file, however is highly recommended to change it by a new one. (The key can be generated here: https://djecrety.ir/)
3. In the first time running the project (and just in the first one) you will have to use the command _make setup_ to create the project's image.
4. Then, use _make start_ to run it locally. Next time, you will just have to use _make start_ and _make stop_ commands.
5. This project runs in: http://localhost:8000/

---

## Tests

There are 20 tests being tested in this project. The characteristics of this tests can be readden below:

1. Three unit tests running in the users app.
2. Three unit tests and fourteen integration tests running in the transactions app.
3. There is a specific command to run the tests (**_make tests_**). However, the tests also runs when it's necessary to build the project's image. 

---

## Logs

There are 3 ways to analyse logs in this application:

1. **_make start_api_**.
2. **_make start_**, then **_make logs_**.
3. **_make start_api_** and **_make logs_** (in separated tabs).

---

## Requirements

* **DOCKER-COMPOSE**: 1.27.4
* **DOCKER**: 19.03.13

