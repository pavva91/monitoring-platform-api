# API for conflict monitoring platform

## Requirements

- Authentication with JWT
- Authorization (casbin)
    - https://dev.to/teresafds/authorization-on-fastapi-with-casbin-41og

## Run

### Install requirements.txt

```bash
pip install -r requirements.txt
```

### Init DB

From root:

Initialize .env for server

```bash
cp example.env .env
```

Initialize .env for docker:

```bash
cp ./docker/example.env ./docker/.env
```

Spin-up postgres:

```bash
cd docker
docker compose up
```

go back to root

```bash
cd ..
```

Init DB-Schema:

```bash
PGPASSWORD=your-password psql -h 127.0.0.1 -p 5432 -U postgres conflict < ./db/schema.sql
```

Import .csv:

```bash
DB_USER=your-password DB_PASS=your-username DB_NAME=conflict CSV_PATH=/path/to/csv/file.csv python db/import_csv.py
```

Enter 'conflict' DB:

```bash
PGPASSWORD=your-password psql -h 127.0.0.1 -p 5432 -U your-user conflict
```

check:

```sql
select * from conflict;
```

### Run the server

```bash
fastapi dev src/main.py
```
NOTE: The 'dev' mode includes hot-reload

To run without hot-reload:

```bash
fastapi run src/main.py
```

You will see the server on:
    - [http://localhost:8000](http://localhost:8000)

You will see the Swagger docs on:
    - [http://localhost:8000/docs](http://localhost:8000/docs)

You will see the Alternative API docs on:
    - [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Reset DB

On dev I usually setup docker in a way that the db is dropped when running:

```bash
cd docker
docker compose down
```

Then:

```bash
cd docker
docker compose up
```

will recreate 'conflict' empty db
then re-init the schema and re-import the .csv

## Example SQL

Enter psql:

```bash
PGPASSWORD=your-password psql -h 127.0.0.1 -p 5432 -U postgres conflict
```

Then you can run sql e.g.:

```sql
SELECT AVG(score) FROM conflict WHERE country='Algeria';
```

```sql
SELECT * FROM conflict WHERE LOWER(country)=LOWER('ALGERIA');
```

```sql
SELECT AVG(score) FROM conflict WHERE LOWER(country)=LOWER('ALGERIA');
```

```sql
SELECT * FROM conflict;
```

```sql
DROP DATABASE conflict;
```
