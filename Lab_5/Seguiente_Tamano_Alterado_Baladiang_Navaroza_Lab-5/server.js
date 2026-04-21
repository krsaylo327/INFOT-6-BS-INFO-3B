const express = require('express');
const Database = require('better-sqlite3');

const app = express();
app.use(express.json());

// ✅ Use in-memory database for easy setup (no file permissions issues)
const db = new Database(':memory:');

console.log("Database connected successfully");

db.exec(`
  CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price NUMERIC
  )
`);

app.get('/api/products', (req, res) => {
  const stmt = db.prepare('SELECT * FROM products');
  const products = stmt.all();
  res.json(products);
});

app.post('/api/products', (req, res) => {
  const { name, price } = req.body;

  const stmt = db.prepare('INSERT INTO products (name, price) VALUES (?, ?)');
  const result = stmt.run(name, price);

  res.status(201).json({
    message: 'Product added successfully',
    id: result.lastInsertRowid
  });
});

app.put('/api/products/:id',(req,res) => {
    const { id } = req.params;
    const { name, price } = req.body;

    const stmt = db.prepare(
        'UPDATE products SET name = ?, price = ? WHERE id = ?'
    );

    const result = stmt.run(name, price, id);

    if (result.changes === 0 ) {
        return res.status(404).json({ message: 'Product not found' });
    }

    res.json({ message: 'Product updated successfully'});
});

app.delete('/api/products/:id', (req, res) => {
    const { id } = req.params;

    const stmt = db.prepare(
        'DELETE FROM products WHERE id = ?'
    );

    const result = stmt.run(id);

    if (result.changes === 0 ) {
        return res.status(404).json({ message: 'Product not found' });
    }

    res.json({ message: 'Product deleted successfully' });
});

app.listen(3000, () => {
  console.log("Server running on http:/localhost:3000");
});