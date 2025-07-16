CREATE DATABASE jmerch;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL CHECK (username ~ '^[a-z0-9_-]{4,}$'),
  email VARCHAR(255) UNIQUE NOT NULL CHECK (email ~ '^[-.\w]+@[-.\w]+\.[-.\w]{2,}$'),
  password VARCHAR NOT NULL,
  first_name VARCHAR CHECK (first_name ~ '^[a-zA-Z0-9\s]{2,}$'),
  last_name VARCHAR CHECK (last_name ~ '^[a-zA-Z0-9\s]{2,}$'),
  gender VARCHAR CHECK (lower(gender) IN ('male', 'female', 'non-binary', 'other')), 
  -- see shared constants for gender
  birthday DATE CHECK (
    birthday > CURRENT_DATE - INTERVAL '100 years'
    AND birthday <= CURRENT_DATE
  ),
  phone_number VARCHAR CHECK (phone_number ~ '^\+?[1-9](?:\s?\d){6,14}$'),
  profile_photo VARCHAR DEFAULT 'https://www.gravatar.com/avatar/?d=mp',
  default_shipping_address VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
