const express = require('express');
const app = express();
const PORT = 3000;

// Middleware (to read JSON)
app.use(express.json());

// GET endpoint
app.get('/api/greeting', (req, res) => {
    res.status(200).json({
        message: "Hello! Your API is working."
    });
});

// POST endpoint
app.post('/api/echo', (req, res) => {
    

    res.status(200).json(req.body);
    });


// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});