import express from 'express';
import { JSONFilePreset } from 'lowdb/node';

const app = express();
const port = 3000;

// Set up lowdb
const defaultData = { videos: [] };
const db = await JSONFilePreset('db.json', defaultData);

// Serve static files from the root directory
app.use(express.static('.'));

// API endpoint to get videos
app.get('/api/videos', async (req, res) => {
  await db.read();
  res.json(db.data.videos);
});

app.listen(port, () => {
  console.log(`TikTok clone server listening at http://localhost:${port}`);
});
