require('dotenv').config();
const express = require('express');
const app = express();

// Ensure SECRET_KEY present before starting the server
const SECRET_KEY = process.env.SECRET_KEY;
if (!SECRET_KEY) {
  console.error('ERROR: SECRET_KEY not found in environment. Exiting.');
  process.exit(1);
}

app.get('/api/users/:id', (req, res) => {
  const id = Number(req.params.id);

  if (id === 1) {
    return res.json({ id: 1, name: 'X', role: 'User Profile' });
  }

  if (id === 2) {
    return res.json({ id: 2, name: 'Y', role: 'User Profile' });
  }

  return res.status(404).json({ error: 'User not found' });
});

app.listen(3000, () => {
  console.log('Express server running on http://127.0.0.1:3000');
});
