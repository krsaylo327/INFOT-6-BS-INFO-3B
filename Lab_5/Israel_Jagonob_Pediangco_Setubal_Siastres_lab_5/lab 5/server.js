const express = require('express');
const Database = require('better-sqlite3');

const app = express();
const PORT = 3000;

app.use(express.json());

const db = new Database('shop.db');

db.exec(`
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
`);

// TEST
app.get('/api/greeting', (req, res) => {
    res.json({ message: "Hello! Your API is working." });
});

// CREATE
app.post('/api/products', (req, res) => {
    const { name, price } = req.body;

    const stmt = db.prepare('INSERT INTO products (name, price) VALUES (?, ?)');
    const result = stmt.run(name, price);

    res.json({ message: "Product added", id: result.lastInsertRowid });
});

// READ
app.get('/api/products', (req, res) => {
    const products = db.prepare('SELECT * FROM products').all();
    res.json(products);
});

// UPDATE
app.put('/api/products/:id', (req, res) => {
    const id = req.params.id;
    const { name, price } = req.body;

    const result = db.prepare(
        'UPDATE products SET name = ?, price = ? WHERE id = ?'
    ).run(name, price, id);

    if (result.changes === 0) {
        return res.status(404).json({ message: "Not found" });
    }

    res.json({ message: "Updated successfully" });
});

// DELETE
app.delete('/api/products/:id', (req, res) => {
    const id = req.params.id;

    const result = db.prepare(
        'DELETE FROM products WHERE id = ?'
    ).run(id);

    if (result.changes === 0) {
        return res.status(404).json({ message: "Not found" });
    }

    res.json({ message: "Deleted successfully" });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
