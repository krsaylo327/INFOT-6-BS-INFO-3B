require('dotenv').config();
const express = require('express');

const app = express();
const PORT = 3000;

// Check for SECRET_KEY
if (!process.env.SECRET_KEY) {
    console.log("Error: SECRET_KEY not set");
    process.exit(1);
}

// Route
app.get('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);

    if (id === 1) {
        return res.json({ id: 1, name: "Alice" });
    } else if (id === 2) {
        return res.json({ id: 2, name: "Bob" });
    } else {
        return res.status(404).json({ error: "User not found" });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});