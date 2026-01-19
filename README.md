# API for conflict monitoring platform

## Requirements

- Authentication with JWT
- Authorization (casbin)

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

**_NOTE_**: create jwt secret e.g.:

```bash
python
```

```python
import secrets
secrets.token_hex(32)
```

copy this value into .env (JWT_SECRET)

**_NOTE_**: e.g. JWT_ALGORITHM=HS256


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
fastapi dev --port 8000 src/main.py
```
**_NOTE_**: The 'dev' mode includes hot-reload

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

The preloaded 'admin' user credentials are:
- username: boss
- password: asdf

You can use the interactive OpenAPI UI:
- [http://localhost:8000/docs](http://localhost:8000/docs)

or import the postman collection:
- [./docs/api_postman_collection.json](./docs/api_postman_collection.json)

or use curl directly:
- [Go to curl commands](#curl-commands)

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

Top 10 countries by events:
```sql
SELECT * FROM conflict ORDER BY events DESC LIMIT 10;
```

The average risk score of the country with the region of most events:

```sql
SELECT AVG(score)
FROM conflict
WHERE country IN (
    SELECT country
    FROM conflict
    ORDER BY events DESC LIMIT 1
);
```

All countries with their average risk, ordered by it

```sql
SELECT country, AVG(score)
FROM conflict
GROUP BY country
ORDER BY AVG(score) DESC;
```

Top 20 countries ordered by average risk;

```sql
SELECT country, AVG(score)
FROM conflict
GROUP BY country
ORDER BY AVG(score) DESC
LIMIT 20;
```

Sum of total events in a country:

```sql
SELECT SUM(events)
FROM conflict
WHERE country='Belgium';
```

Top 20 countries by total number of events in the country:

```sql
SELECT country, SUM(events) AS total_events
FROM conflict
GROUP BY country
ORDER BY SUM(events) DESC
LIMIT 20;
```

Get average events per person for the country

```sql
SELECT SUM(events)::NUMERIC / SUM(population)::NUMERIC AS division
FROM conflict
WHERE country = 'Italy';
```

Get list of countries ordered by the number of events per person, in the country:

```sql
SELECT
    country,
    SUM(events)::NUMERIC / SUM(population)::NUMERIC AS events_per_person
FROM conflict
GROUP BY country
ORDER BY division DESC;
```
**_NOTE_**: The result is not clean yet, probably because of some missing population data, I think.

**_SOLUTION_**: To clean the data that we have, I take advantage of the CTE (Common Table Expression) to save the result of the query into a table, making the queries also more readable and - most notably - reusable, for more complex queries. For now I just remove the average data that is null, to get a more realistic ordering.

```sql
WITH group_events_population_ratio AS (
    SELECT
            country,
            SUM(events)::NUMERIC / SUM(population)::NUMERIC AS events_per_person
    FROM conflict
    GROUP BY country
    ORDER BY events_per_person DESC
)
SELECT *
FROM group_events_population_ratio
WHERE events_per_person IS NOT NULL;
```

Inspect the query plan for a query, for example, analyze the last one, with the CTE:

```sql
EXPLAIN (ANALYZE, BUFFERS)
WITH group_events_population_ratio AS (
    SELECT
        country,
        SUM(events)::NUMERIC / SUM(population)::NUMERIC AS events_per_person
    FROM conflict
    GROUP BY country
    ORDER BY events_per_person DESC
)
SELECT *
FROM group_events_population_ratio
WHERE events_per_person IS NOT NULL;
```

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

## curl commands

### POST /register

Create new 'reader' user:

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/register \
  --header 'content-type: application/json' \
  --data '{
  "username":"alice",
  "password":"secret"
}'
```

### POST /login

1. login with admin role user

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/login \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data 'username=boss&password=asdf'
```

2. login with normal "reader" role user

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/login \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data 'username=alice&password=secret'
```

### POST /logout

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/logout \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJleGFtcGxlLm9yZyIsInN1YiI6ImFsaWNlIiwicm9sZSI6InJlYWRlciIsImlhdCI6MTc2ODc3NzI0OC4xMjg2NCwiZXhwIjoxNzY4ODYzNjQ4LjEyODY0fQ.z-ypdyn8n-UUdoCDzS_WxTKA3JsUT5QStOOLDDleu3I'
```

### GET /conflictdata

```bash
curl --request GET \
  --url 'http://localhost:8000/api/v1/conflictdata?page=1&size=50&countries=italy&countries=germany' | jq -r .
```

### GET /conflictdata/{country}

```bash
curl --request GET \
  --url http://localhost:8000/api/v1/conflictdata/spain
```

### GET /conflictdata/{country}/riskscore

```bash
curl --request GET \
  --url http://localhost:8000/api/v1/conflictdata/spain/riskscore
```

### GET /conflictdata/{admin1}/userfeedback

too short feedback:

```bash
curl --request POST \
  --url http://localhost:8000/api/v1/conflictdata/marche/userfeedback \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJleGFtcGxlLm9yZyIsInN1YiI6ImFsaWNlIiwicm9sZSI6InJlYWRlciIsImlhdCI6MTc2ODc3NzcyNS4wMzcwNzEsImV4cCI6MTc2ODg2NDEyNS4wMzcwNzF9.QC6dTEpZPP1kzT7BmwHgwE9EsP-sIsHYfJnq6pqjTqs' \
  --header 'content-type: application/json' \
  --data '{
  "text":"short"
}'
```

A valid feedback:
```bash
curl --request POST \
  --url http://localhost:8000/api/v1/conflictdata/marche/userfeedback \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJleGFtcGxlLm9yZyIsInN1YiI6ImFsaWNlIiwicm9sZSI6InJlYWRlciIsImlhdCI6MTc2ODc3NzcyNS4wMzcwNzEsImV4cCI6MTc2ODg2NDEyNS4wMzcwNzF9.QC6dTEpZPP1kzT7BmwHgwE9EsP-sIsHYfJnq6pqjTqs' \
  --header 'content-type: application/json' \
  --data '{
  "text":"a valid feedback to marche"
}'
```

### DELETE /conflictdata

Delete by admin1:
```bash
curl --request DELETE \
  --url 'http://localhost:8000/api/v1/conflictdata?admin1=Sardegna' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJleGFtcGxlLm9yZyIsInN1YiI6ImJvc3MiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3Njg3NzkwMTkuMzM1NzAxLCJleHAiOjE3Njg4NjU0MTkuMzM1NzAxfQ.IqiKzeWzlWhewthkXYgjeLmKNFD54cynOju_BEywqAU'
```

Delete by country:

```bash
curl --request DELETE \
  --url 'http://localhost:8000/api/v1/conflictdata?country=Algeria' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJleGFtcGxlLm9yZyIsInN1YiI6ImJvc3MiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3Njg3NzkwMTkuMzM1NzAxLCJleHAiOjE3Njg4NjU0MTkuMzM1NzAxfQ.IqiKzeWzlWhewthkXYgjeLmKNFD54cynOju_BEywqAU'
```

## Pyenv (venv)

I developed using the latest python (3.14.2), but it also compatible with python 3.10

From project root:

```bash
pyenv install 3.14.2
```

```bash
pyenv virutalenv 3.14.2 your-virtual-env-project-3.14.2
```

```bash
pyenv local your-virtual-env-project-3.14.2
```
