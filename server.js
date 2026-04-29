const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Database setup
const db = new sqlite3.Database('./lisnave_data.db');

// Initialize database
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS cylinders (
    id TEXT PRIMARY KEY,
    type TEXT,
    zoneId TEXT,
    lat REAL,
    lng REAL,
    status TEXT,
    ts TEXT,
    worker TEXT,
    pres INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
  
  db.run(`CREATE TABLE IF NOT EXISTS workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
  
  // Insert default workers if empty
  db.get("SELECT COUNT(*) as count FROM workers", (err, row) => {
    if (row.count === 0) {
      const defaultWorkers = ['J. Ferreira','M. Santos','R. Costa','A. Lopes','C. Mendes','P. Sousa'];
      defaultWorkers.forEach(worker => {
        db.run("INSERT INTO workers (name) VALUES (?)", [worker]);
      });
    }
  });
});

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  // Send current data to new client
  loadAllData().then(data => {
    socket.emit('initialData', data);
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// API Routes
app.get('/api/cylinders', async (req, res) => {
  try {
    const cylinders = await loadCylinders();
    res.json(cylinders);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/cylinders', async (req, res) => {
  try {
    const cylinder = req.body;
    await saveCylinder(cylinder);
    
    // Broadcast to all connected clients
    const allData = await loadAllData();
    io.emit('dataUpdate', allData);
    
    res.json({ success: true, cylinder });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.put('/api/cylinders/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const cylinder = req.body;
    await updateCylinder(id, cylinder);
    
    // Broadcast to all connected clients
    const allData = await loadAllData();
    io.emit('dataUpdate', allData);
    
    res.json({ success: true, cylinder });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.delete('/api/cylinders/:id', async (req, res) => {
  try {
    const { id } = req.params;
    await deleteCylinder(id);
    
    // Broadcast to all connected clients
    const allData = await loadAllData();
    io.emit('dataUpdate', allData);
    
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/workers', async (req, res) => {
  try {
    const workers = await loadWorkers();
    res.json(workers);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Database functions
function loadCylinders() {
  return new Promise((resolve, reject) => {
    db.all("SELECT * FROM cylinders ORDER BY created_at", (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
}

function saveCylinder(cylinder) {
  return new Promise((resolve, reject) => {
    const sql = `INSERT OR REPLACE INTO cylinders 
                (id, type, zoneId, lat, lng, status, ts, worker, pres, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`;
    db.run(sql, [
      cylinder.id,
      cylinder.type,
      cylinder.zoneId,
      cylinder.lat,
      cylinder.lng,
      cylinder.status,
      cylinder.ts,
      cylinder.worker,
      cylinder.pres
    ], function(err) {
      if (err) reject(err);
      else resolve(this);
    });
  });
}

function updateCylinder(id, cylinder) {
  return new Promise((resolve, reject) => {
    const sql = `UPDATE cylinders SET 
                type=?, zoneId=?, lat=?, lng=?, status=?, ts=?, worker=?, pres=?, updated_at=CURRENT_TIMESTAMP 
                WHERE id=?`;
    db.run(sql, [
      cylinder.type,
      cylinder.zoneId,
      cylinder.lat,
      cylinder.lng,
      cylinder.status,
      cylinder.ts,
      cylinder.worker,
      cylinder.pres,
      id
    ], function(err) {
      if (err) reject(err);
      else resolve(this);
    });
  });
}

function deleteCylinder(id) {
  return new Promise((resolve, reject) => {
    db.run("DELETE FROM cylinders WHERE id=?", [id], function(err) {
      if (err) reject(err);
      else resolve(this);
    });
  });
}

function loadWorkers() {
  return new Promise((resolve, reject) => {
    db.all("SELECT name FROM workers ORDER BY name", (err, rows) => {
      if (err) reject(err);
      else resolve(rows.map(row => row.name));
    });
  });
}

async function loadAllData() {
  const cylinders = await loadCylinders();
  const workers = await loadWorkers();
  return { cylinders, workers };
}

// Start server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🚀 Lisnave Gas Tracker Server running on port ${PORT}`);
  console.log(`📱 Access: http://localhost:${PORT}`);
  console.log(`🔗 WebSocket ready for real-time sync`);
});
