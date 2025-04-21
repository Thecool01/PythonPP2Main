### 1) Creating the table contacts
```
    phonebookdb=# CREATE TABLE Contacts( 
    phonebookdb(# ID SERIAL PRIMARY KEY,
    phonebookdb(# name VARCHAR(100),
    phonebookdb(# phone VARCHAR(20) 
    phonebookdb(# );
```

### 2) FUNCTIONS

#### 1

```
CREATE OR REPLACE FUNCTION search_contacts(pattern VARCHAR)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || pattern || '%' OR 
          c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
```
> In this functions || is connection symbol
> ILIKE is LIKE but Case-insensitive.

#### 2
```
CREATE OR REPLACE PROCEDURE upsert_user(
    user_name VARCHAR(100),
    user_phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- First try to update existing user
    UPDATE contacts 
    SET phone = user_phone 
    WHERE name = user_name;
    
    -- If no rows were updated, insert new user
    IF NOT FOUND THEN
        INSERT INTO contacts(name, phone)
        VALUES (user_name, user_phone);
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        -- Just re-raise the error with context
        RAISE EXCEPTION 'Error in upsert_user: %', SQLERRM;
END;
$$;
```
#### 3
```
CREATE OR REPLACE PROCEDURE insert_multiple_users(
    name_list VARCHAR[],
    phone_list VARCHAR[],
    INOUT invalid_records REFCURSOR = 'invalid_records'
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    current_name VARCHAR;
    current_phone VARCHAR;
    error_message TEXT;
BEGIN

    -- Create temporary table for invalid records
    CREATE TEMP TABLE IF NOT EXISTS temp_invalid_records (
        rec_name VARCHAR,
        rec_phone VARCHAR,
        rec_error_message TEXT
    ) ON COMMIT DROP;

    -- Clear any existing data
    TRUNCATE temp_invalid_records;

    -- Process each record
    FOR i IN 1..array_length(name_list, 1) LOOP
        current_name := name_list[i];
        current_phone := phone_list[i];
        error_message := NULL;

        -- Validate phone format
        IF current_phone IS NULL OR current_phone = '' THEN
            error_message := 'Phone is empty';
        ELSIF EXISTS (SELECT 1 FROM contacts WHERE name = current_name) THEN
            error_message := 'Name already exists!';
        END IF;

        -- Insert valid records, store invalid ones
        IF error_message IS NULL THEN
            INSERT INTO contacts(name, phone)
            VALUES (current_name, current_phone)
            ON CONFLICT (name) DO UPDATE
            SET phone = EXCLUDED.phone;
        ELSE
            INSERT INTO temp_invalid_records
            VALUES (current_name, current_phone, error_message);
        END IF;
    END LOOP;

    -- Open cursor for invalid records
    OPEN invalid_records FOR
    SELECT rec_name AS name, rec_phone AS phone, rec_error_message AS error_message
    FROM temp_invalid_records
    ORDER BY rec_name;


    -- Output summary
    RAISE NOTICE 'Processed % records', array_length(name_list, 1);
    RAISE NOTICE 'Successfully inserted/updated % records', 
        array_length(name_list, 1) - (SELECT COUNT(*) FROM temp_invalid_records);
    RAISE NOTICE 'Found % invalid records', 
        (SELECT COUNT(*) FROM temp_invalid_records);
END;
$$;
```

#### 4
```
CREATE OR REPLACE FUNCTION get_contacts_page(limit_per_page INT, page_number INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.phone
    FROM contacts c
    ORDER BY c.name, c.phone
    LIMIT limit_per_page
    OFFSET (page_number - 1) * limit_per_page;
END;
$$;

```

```
INSERT INTO contacts (name, phone)
VALUES
('Balnur', '87051237890'),
('Jane', '87098765432'),
('Niko', '87771234567'),
('Radmir', '87074561234'),
('Vladimir', '87762345678'),
('Vanessa', '87015678901'),
('Klara', '87083456789'),
('Umut', '87780987654'),
('Erasil', '87022113344'),
('Diana', '87750011222');

```

#### 5
```

CREATE OR REPLACE PROCEDURE delete_user_byname(
    user_name VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM contacts 
    WHERE name = user_name;
    
    
EXCEPTION
    WHEN OTHERS THEN
        -- Just re-raise the error with context
        RAISE EXCEPTION 'Error in upsert_user: %', SQLERRM;
END;
$$;

```


```

CREATE OR REPLACE PROCEDURE delete_user_byphone(
    user_phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM contacts 
    WHERE phone = user_phone;
    
    
EXCEPTION
    WHEN OTHERS THEN
        -- Just re-raise the error with context
        RAISE EXCEPTION 'Error in upsert_user: %', SQLERRM;
END;
$$;

```