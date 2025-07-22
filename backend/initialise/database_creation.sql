CREATE DATABASE jmerch;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL CHECK (username ~ '^[a-z0-9_-]{4,}$'),
  email VARCHAR(255) UNIQUE NOT NULL CHECK (email ~ '^[-.\w]+@[-.\w]+\.[-.\w]{2,}$'),
  password VARCHAR NOT NULL,
  first_name VARCHAR CHECK (first_name ~ '^[a-zA-Z0-9_\s./-]{2,}$'),
  last_name VARCHAR CHECK (last_name ~ '^[a-zA-Z0-9_\s./-]{2,}$'),
  gender VARCHAR CHECK (lower(gender) IN ('male', 'female', 'non-binary', 'other')), 
  -- see shared constants for gender
  birthday DATE CHECK (
    birthday > CURRENT_DATE - INTERVAL '100 years'
    AND birthday <= CURRENT_DATE
  ),
  phone_number VARCHAR CHECK (phone_number ~ '^\+?[0-9](?:\s?\d){6,14}$'),
  profile_photo VARCHAR DEFAULT 'https://www.gravatar.com/avatar/?d=mp',
  default_shipping_address VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  product_name VARCHAR NOT NULL CHECK (product_name ~ '^[a-zA-Z0-9_\s./-]{2,}$'),
  product_description TEXT,
  owner_user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category VARCHAR NOT NULL CHECK (lower(category) IN ('tops', 'bottoms', 'headwear', 'bags', 'accessories', 'misc')),
  main_display_photo VARCHAR DEFAULT 'https://pixabay.com/illustrations/box-packaging-mockup-paper-box-6345764/',
  default_delivery_time INT DEFAULT 30 CHECK (default_delivery_time >= 1),
  viewable_to_users_list INt[] DEFAULT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_variants (
  id SERIAL PRIMARY KEY,
  main_product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  design_name VARCHAR NOT NULL CHECK (design_name ~ '^[a-zA-Z0-9_\s./-]{2,}$'),
  qty_inventory INT NOT NULL CHECK (qty_inventory >= 0 AND qty_inventory = floor(qty_inventory)),
  qty_available INT NOT NULL CHECK (qty_available >= 0 AND qty_available = floor(qty_available) AND qty_available <= qty_inventory),
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0.00),
  display_photo VARCHAR DEFAULT 'https://pixabay.com/illustrations/box-packaging-mockup-paper-box-6345764/',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cart (
  id SERIAL PRIMARY KEY,
  buyer_user_id INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cart_items (
  id SERIAL PRIMARY KEY,
  cart_id INT NOT NULL REFERENCES cart(id) ON DELETE CASCADE,
  product_variant_id INT NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
  qty INT NOT NULL CHECK (qty >= 0 AND qty = floor(qty)),
  viewable_to VARCHAR[] DEFAULT NULL
);