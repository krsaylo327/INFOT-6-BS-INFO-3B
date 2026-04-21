const express =require('express');
const Database = require('better-sqlite3');

const app =express();
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

app.get('/api/greeting', (req, res) => {
    res.status(200).json({
        message: "Hello! Your API is working."
    });
});

app.post('/api/echo', (req, res) => {
    res.status(200).json(req.body);
});


app.get('/api/products', (req, res) =>{
    const stmt =db.prepare('SELECT * FROM products');
    const products = stmt.all();

    res.status(200).json(products);
});

app.post('/api/products', (req, res) => {
    const {name, price} = req.body;

    const stmt = db.prepare('INSERT INTO products (name,price) VALUES (?, ?)');
    const result = stmt.run(name, price);

    res.status(201).json({
        message:"Product added successfully",
        id: result.lastInsertRowid
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});


