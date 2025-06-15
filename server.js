const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Mock data
let users = [
  { id: 1, name: 'Alice', carbonCredits: 120 },
  { id: 2, name: 'Bob', carbonCredits: 80 }
];

let rewards = [
  { id: 1, name: '10% discount', cost: 50 },
  { id: 2, name: 'Free coffee', cost: 20 }
];

let footprints = [
  { id: 1, userId: 1, amount: 12.5, date: '2024-05-01' },
  { id: 2, userId: 2, amount: 7.0, date: '2024-05-03' }
];

// Routes
app.get('/', (req, res) => {
  res.send('Carbon Wallet API');
});

// User routes
app.get('/api/users', (req, res) => {
  res.json(users);
});

app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === Number(req.params.id));
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }
  res.json(user);
});

app.post('/api/users', (req, res) => {
  const newUser = { id: Date.now(), ...req.body };
  users.push(newUser);
  res.status(201).json(newUser);
});

// Rewards routes
app.get('/api/rewards', (req, res) => {
  res.json(rewards);
});

app.post('/api/rewards/redeem', (req, res) => {
  const { userId, rewardId } = req.body;
  const user = users.find(u => u.id === userId);
  const reward = rewards.find(r => r.id === rewardId);
  if (!user || !reward) {
    return res.status(400).json({ message: 'Invalid user or reward' });
  }
  if (user.carbonCredits < reward.cost) {
    return res.status(400).json({ message: 'Insufficient credits' });
  }
  user.carbonCredits -= reward.cost;
  res.json({ message: 'Reward redeemed', user });
});

// Footprint routes
app.get('/api/footprints', (req, res) => {
  res.json(footprints);
});

app.post('/api/footprints', (req, res) => {
  const newFootprint = { id: Date.now(), ...req.body };
  footprints.push(newFootprint);
  res.status(201).json(newFootprint);
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
