### 1)
```
CREATE TABLE IF NOT EXISTS snake_records (
snakedb(# id SERIAL PRIMARY KEY,
snakedb(# nickname VARCHAR(50) NOT NULL,
snakedb(# score INTEGER NOT NULL,
snakedb(# level INTEGER NOT NULL);
CREATE TABLE
snakedb=# SELECT * FROM snake_records
snakedb-# ;
 id | nickname | score | level
----+----------+-------+-------
(0 rows)
```

``` Не забудь в ставить!
ALTER TABLE snake_records ADD COLUMN snake_size INTEGER DEFAULT 1;
```