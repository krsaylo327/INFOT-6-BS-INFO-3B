const express = require('express');
const Database = require('better-sqlite3');
const app = express();
const PORT = 3000;
app.use(express.json());

const db = new Database('shop.db');
console.log('Connected to shop.db');

try {
  db.exec(`CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL
  );`);
  console.log('Products table ready');
} catch (err) {
  console.error('Failed to create products table:', err.message);
}

app.get('/api/greeting', (req, res) => {
  res.status(200).json({ message: 'Henlo ur API is workin.' });
});

app.post('/api/echo', (req, res) => {
  const data = req.body;
  res.status(201).json({
    message: 'Data received successfully',
    data: data,
  });
});

app.get('/api/products', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM products').all();
    res.status(200).json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/products', (req, res) => {
  const { name, price } = req.body;
  if (!name || price === undefined) {
    return res.status(400).json({ error: 'name and price are required' });
  }

  try {
    const stmt = db.prepare('INSERT INTO products (name, price) VALUES (?, ?)');
    const info = stmt.run(name, price);
    res.status(201).json({ id: info.lastInsertRowid, name, price });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.put('/api/products/:id', (req, res) => {
  const id = req.params.id;
  const { name, price } = req.body;
  if (name === undefined || price === undefined) {
    return res.status(400).json({ error: 'name and price are required' });
  }

  try {
    const stmt = db.prepare('UPDATE products SET name = ?, price = ? WHERE id = ?');
    const info = stmt.run(name, price, id);
    if (info.changes === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    res.status(200).json({ id: Number(id), name, price });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/products/:id', (req, res) => {
  const id = req.params.id;
  try {
    const stmt = db.prepare('DELETE FROM products WHERE id = ?');
    const info = stmt.run(id);
    if (info.changes === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    res.status(200).json({ message: 'Product deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
