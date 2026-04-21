const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

const Database = require('better-sqlite3');
const db = new Database('shop.db');

db.exec(`
  CREATE TABLE IF NOT EXISTS products (
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
  stmt.run(name, price);
  res.status(201).json({ message: 'Product added successfully' });
});

app.put('/api/products/:id', (req, res) => {
  const id = req.params.id;
  const { name, price } = req.body;

  const stmt = db.prepare('UPDATE products SET name = ?, price = ? WHERE id = ?');
  const result = stmt.run(name, price, id);

  if (result.changes === 0) {
    return res.status(404).json({ message: 'Product not found' });
  }

  res.status(200).json({ message: 'Product updated successfully' });
});

app.delete('/api/products/:id', (req, res) => {
  const id = req.params.id;

  const stmt = db.prepare('DELETE FROM products WHERE id = ?');
  const result = stmt.run(id);

  if (result.changes === 0) {
    return res.status(404).json({ message: 'Product not found' });
  }

  res.status(200).json({ message: 'Product deleted successfully' });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
