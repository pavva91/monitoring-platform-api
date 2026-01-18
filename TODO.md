# Tasks on this project

1. create db schema (DONE)
2. import csv into db (DONE)
3. POST /register (DONE)
4. POST /login (DONE)
    - JWT-authentication (DONE)
    - JWT-invalidation (lower priority) (DONE)
5. POST /logout (lower priority) (DONE)
6. GET /conflictdata (DONE)
7. GET /conflictdata/:country (DONE)
8. GET /conflictdata/:country/riskscore (DONE)
9. POST /conflictdata/:admin1/userfeedback (DONE)
10. DELETE /conflictdata (DONE)
11. Implement authorization (with casbin) (DONE)
12. Complete docs (DONE)

# Future developments I would do

1. Setup redis as caching layer, both for:

- read-through with a TTL for endpoint results that don't change frequently, in this way the db is queried on read only at the cache-miss. (e.g. if the original data is bulk updated once every day, I would do a TTL that follows this bulk update's frequency, to give the consumer of the dataset performance without having stale date on the cache)
- write-behind (write first on the cache and then sync on the db) on the logout table (POST /logout), to limit the calls to the db, especially when checking if the JWT is still valid, because the endpoints that need authentication do this check every time and they will go to redis first. (e.g.: POST /conflictdata/:admin1/userfeedback )
