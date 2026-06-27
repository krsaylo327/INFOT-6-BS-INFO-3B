require('dotenv').config();

const express = require('express');
const app = express();

const PORT = 3000;


if (!process.env.SECRET_KEY) {
    console.log("ERROR: SECRET_KEY is missing!");
    process.exit(1);
}


const users = {
    1: {
        id: 1,
        name: "X",
        role: "Admin"
    },
    2: {
        id: 2,
        name: "Y",
        role: "User"
    }
};


app.get('/api/users/:id', (req, res) => {
    const id = req.params.id;

    if (users[id]) {
        res.json(users[id]);
    } else {
        res.status(404).json({
            error: "User not found"
        });
    }
});

app.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
});