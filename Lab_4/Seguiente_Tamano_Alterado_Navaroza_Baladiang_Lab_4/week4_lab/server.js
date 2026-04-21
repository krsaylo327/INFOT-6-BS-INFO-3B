const express=require('express');
const app = express();
// Middleware to parse incoming JSON payloads 
app.use(express.json()); 
// Endpoint 1: Open POST endpoint for JSON serialization testing 
app.post('/api/users', (req, res) => { 
    console.log("Received data:", req.body); 
    res.status(201).json({ message: "User successfully created", data: req.body }); 
});

app.get('/api/secure-basic', (req, res) => {
    const authHeader = req.headers.authorization || '';
    const b64auth = authHeader.split(' ')[1] || '';
    const [login, password] = Buffer.from(b64auth, 'base64').toString().split(':');

    if (login === 'admin' && password === 'secret123') { 
        res.status(200).json({ message: "Basic Auth Successful. Welcome Admin." });
        } else { 
            res.setHeader('WWW-Authenticate', 'Basic'); 
            res.status(401).json({ error: "401 Unauthorized: Invalid Credentials" }); 
        } 
    });

app.get('/api/secure-key', (req, res) => { 
    const apiKey = req.headers['x-api-key']; 
    if (apiKey === 'lab-key-999') { 
        res.status(200).json({ message: "API Key Accepted. Access Granted." }); 
    } else { 
        res.status(401).json({ error: "401 Unauthorized: Missing or Invalid API Key" }); 
    } 
}); 
app.post('/api/register', (req, res) => { 
    const authHeader = req.headers.authorization; 
    if (authHeader === 'Bearer token-xyz-789') { 
        res.status(201).json({ message: "Registration Complete", payload: req.body }); 
    } else { 
        res.status(401).json({ error: "401 Unauthorized: Invalid Bearer Token" }); 
    } 
}); 
app.listen(3000, () => { 
    console.log('Local API Server running on http://localhost:3000'); 
});