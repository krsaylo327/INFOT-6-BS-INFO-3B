const express = require('express');
const Database = require('better-sqlite3');

const app = express();
const PORT = 3000;

app.use(express.json());

const db = new Database('shop.db');
console.log("Connected to SQLite database (shop.db)");

db.exec(`
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price NUMERIC
    )
`);

app.get('/api/products', (req, res) => {
    try {
        const stmt = db.prepare("SELECT * FROM products");
        const rows = stmt.all();
        res.status(200).json(rows);
    } catch (err) {
        res.status(500).json({
            message: "Error fetching products",
            error: err.message
        });
    }
});

app.post('/api/products', (req, res) => {
    try {
        const { name, price } = req.body;

        if (!name || price == null) {
            return res.status(400).json({
                message: "Name and price are required"
            });
        }

        const stmt = db.prepare(
            "INSERT INTO products (name, price) VALUES (?, ?)"
        );

        const result = stmt.run(name, price);

        res.status(201).json({
            message: "Product added successfully",
            product: {
                id: result.lastInsertRowid,
                name,
                price
            }
        });

    } catch (err) {
        res.status(500).json({
            message: "Error inserting product",
            error: err.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});