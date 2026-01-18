CREATE TABLE IF NOT EXISTS account_type (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS account (
    id BIGSERIAL PRIMARY KEY,
    account_type_id INTEGER NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account_type FOREIGN KEY(account_type_id) REFERENCES account_type(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logout (
    id BIGSERIAL PRIMARY KEY,
    account_id BIGSERIAL UNIQUE NOT NULL,
    last_logout_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account FOREIGN KEY(account_id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS conflict (
    id BIGSERIAL PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    admin1 VARCHAR(50) NOT NULL, -- NOTE: admin1 is not unique
    population INTEGER,
    events INTEGER NOT NULL,
    score INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
    id BIGSERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    conflict_id INTEGER NOT NULL,
    text VARCHAR(500) NOT NULL,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account FOREIGN KEY(account_id) REFERENCES account(id) ON DELETE CASCADE,
    CONSTRAINT fk_conflict FOREIGN KEY(conflict_id) REFERENCES conflict(id) ON DELETE CASCADE
);

INSERT INTO account_type (
    type
) VALUES
    ('admin'),
    ('reader');

INSERT INTO account (
    username,
    password_hash,
    account_type_id
) VALUES
    ('boss', '$2b$12$3P.DR/eXLknvKGVk8tOwH.Jk1w9ZIMzzc3lL85ftlMxYk6hJgaSji', 1);
