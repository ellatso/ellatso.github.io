# Carbon Wallet Backend

This project now includes a simple Node.js Express backend that provides mock API routes used by the Carbon Wallet demo.

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server with nodemon:
   ```bash
   npm run dev
   ```
   or start normally:
   ```bash
   npm start
   ```

The server listens on port `3000` by default and exposes the following routes:

- `GET /api/users` - list all users
- `GET /api/users/:id` - fetch a single user
- `POST /api/users` - create a new user
- `GET /api/rewards` - list available rewards
- `POST /api/rewards/redeem` - redeem a reward
- `GET /api/footprints` - list all carbon footprints
- `POST /api/footprints` - add a new footprint record

These routes operate on in-memory mock data and are intended for local development and testing.
