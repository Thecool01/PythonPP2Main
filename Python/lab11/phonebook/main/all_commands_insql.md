### 1) Creating the table contacts
```
    phonebookdb=# CREATE TABLE Contacts( 
    phonebookdb(# ID SERIAL PRIMARY KEY,
    phonebookdb(# name VARCHAR(100),
    phonebookdb(# phone VARCHAR(20) 
    phonebookdb(# );
```

### 2) FUNCTIONS
```
CREATE FUNCTION find_by_name(entered_value VARCHAR) RETURNS SETOF contacts AS 
$$
    SELECT * FROM contacts 
        WHERE name = entered_value;
$$ LANGUAGE SQL;
```
```
CREATE FUNCTION find_by_phone(entered_value VARCHAR) RETURNS SETOF contacts AS 
$$
    SELECT * FROM contacts 
    WHERE phone = entered_value;
$$ LANGUAGE SQL;
```