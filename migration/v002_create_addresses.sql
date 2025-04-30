CREATE TABLE addresses (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Auto-increment primary key
    user_id INT NOT NULL, -- Foreign key to the users table
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100) NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES users(id) -- Ensures referential integrity
);
