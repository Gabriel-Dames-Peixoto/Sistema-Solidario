CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    region VARCHAR(80) NOT NULL,
    coord_x DECIMAL(10,2) NOT NULL,
    coord_y DECIMAL(10,2) NOT NULL
);

CREATE TABLE donated_items (
    id INTEGER PRIMARY KEY,
    donor_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(60) NOT NULL,
    quantity INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    region VARCHAR(80) NOT NULL,
    coord_x DECIMAL(10,2) NOT NULL,
    coord_y DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (donor_id) REFERENCES users(id)
);

CREATE TABLE help_requests (
    id INTEGER PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL,
    category VARCHAR(60) NOT NULL,
    description TEXT NOT NULL,
    needed_quantity INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    region VARCHAR(80) NOT NULL,
    coord_x DECIMAL(10,2) NOT NULL,
    coord_y DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (beneficiary_id) REFERENCES users(id)
);

CREATE TABLE matching_history (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    request_id INTEGER NOT NULL,
    allocated_quantity INTEGER NOT NULL,
    estimated_distance DECIMAL(10,2) NOT NULL,
    score DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES donated_items(id),
    FOREIGN KEY (request_id) REFERENCES help_requests(id)
);

