const express = require("express");
const mysql = require("mysql");
const amqp = require("amqplib/callback_api");

const app = express();
app.use(express.json());

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "uts_eai",
});

// Connect to database
db.connect((err) => {
  if (err) {
    console.error("Error connecting to database:", err);
    return;
  }
  console.log("Connected to MySQL database");
});

// Connect to RabbitMQ
let channel;

amqp.connect("amqp://localhost", (err, conn) => {
  if (err) {
    console.error("Error connecting to RabbitMQ:", err);
    return;
  }
  console.log("Connected to RabbitMQ");

  conn.createChannel((err, ch) => {
    if (err) {
      console.error("Error creating channel:", err);
      return;
    }
    channel = ch;
    const exchange = "penjualan_logs";

    ch.assertExchange(exchange, "fanout", { durable: false });

    // Create a queue for this service
    ch.assertQueue("", { exclusive: true }, (err, q) => {
      if (err) {
        console.error("Error creating queue:", err);
        return;
      }
      console.log("Queue created:", q.queue);
      ch.bindQueue(q.queue, exchange, "");

      // Consume messages from the queue
      ch.consume(
        q.queue,
        (msg) => {
          const data = JSON.parse(msg.content.toString());
          console.log("Received message:", data);
        },
        { noAck: true }
      );
    });
  });
});

// Create a new penjualan
app.post("/create-penjualan", (req, res) => {
  const { PenjualanID, ProdukID, Jumlah } = req.body;
  if (!PenjualanID || !ProdukID || !Jumlah) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  db.query("SELECT Harga FROM produk WHERE ProdukID = ?", [ProdukID], (err, result) => {
    if (err) {
      console.error("Error fetching harga:", err);
      return res.status(500).json({ error: "Internal server error" });
    }

    if (result.length === 0) {
      return res.status(404).json({ error: "Produk not found" });
    }

    const Harga = result[0].Harga;
    const TotalHarga = Jumlah * Harga;

    const sql =
      "INSERT INTO penjualan (PenjualanID, ProdukID, Jumlah, TotalHarga) VALUES (?, ?, ?, ?)";
    db.query(sql, [PenjualanID, ProdukID, Jumlah, TotalHarga], (err) => {
      if (err) {
        console.error("Error creating penjualan:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      const message = JSON.stringify({
        action: "CREATE",
        PenjualanID,
        ProdukID,
        Jumlah,
        TotalHarga,
      });
      channel.publish("penjualan_logs", "", Buffer.from(message));
      res.json({ message: "Penjualan created successfully", PenjualanID });
    });
  });
});

// Get all penjualan
app.get("/show-penjualan/", (req, res) => {
  const sql = `
        SELECT penjualan.PenjualanID, produk.ProdukID, produk.Nama, produk.Harga, penjualan.Jumlah, 
               penjualan.TotalHarga
        FROM penjualan 
        JOIN produk ON penjualan.ProdukID = produk.ProdukID
        ORDER BY penjualan.PenjualanID ASC`;
  db.query(sql, (err, result) => {
    if (err) {
      console.error("Error fetching penjualan:", err);
      return res.status(500).json({ error: "Internal server error" });
    }
    res.json(result);
  });
});

// Get penjualan by id
app.get("/show-penjualan/:PenjualanID", (req, res) => {
  const PenjualanID = parseInt(req.params.PenjualanID);
  db.query(
    "SELECT penjualan.PenjualanID, produk.ProdukID, produk.Nama, produk.Harga, penjualan.Jumlah, penjualan.TotalHarga FROM penjualan JOIN produk ON penjualan.ProdukID = produk.ProdukID WHERE penjualan.PenjualanID = ?",
    [PenjualanID],
    (err, result) => {
      if (err) {
        console.error("Error fetching penjualan:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      if (result.length > 0) {
        res.json(result[0]);
      } else {
        res.status(404).json({ error: "Penjualan not found" });
      }
    }
  );
});

// Update penjualan by id
app.put("/update-penjualan/:PenjualanID", (req, res) => {
  const PenjualanID = parseInt(req.params.PenjualanID);
  const { ProdukID, Jumlah } = req.body;
  if (!ProdukID || !Jumlah) {
    return res.status(400).json({ error: "Missing required fields" });
  }
  db.query("SELECT Harga FROM produk WHERE ProdukID = ?", [ProdukID], (err, result) => {
    if (err) {
      console.error("Error fetching harga:", err);
      return res.status(500).json({ error: "Internal server error" });
    }
    if (result.length === 0) {
      return res.status(404).json({ error: "Produk not found" });
    }
    const Harga = result[0].Harga;
    const TotalHarga = Jumlah * Harga;
    const sql = "UPDATE penjualan SET ProdukID=?, Jumlah=?, TotalHarga=? WHERE PenjualanID=?";
    db.query(sql, [ProdukID, Jumlah, TotalHarga, PenjualanID], (err) => {
      if (err) {
        console.error("Error updating penjualan:", err);
        return res.status(500).json({ error: "Internal server error" });
      }
      const message = JSON.stringify({
        action: "UPDATE",
        id: PenjualanID,
        ProdukID,
        Jumlah,
        TotalHarga,
      });
      channel.publish("penjualan_logs", "", Buffer.from(message));
      res.json({ message: "Penjualan updated successfully", id: PenjualanID });
    });
  });
});

// Delete penjualan by id
app.delete("/delete-penjualan/:PenjualanID", (req, res) => {
  const PenjualanID = parseInt(req.params.PenjualanID);
  const sql = "DELETE FROM penjualan WHERE PenjualanID=?";
  db.query(sql, [PenjualanID], (err, result) => {
    if (err) {
      console.error("Error deleting penjualan:", err);
      res.status(500).json({ error: "Internal server error" });
      return;
    }
    const message = JSON.stringify({ action: "DELETE", id: PenjualanID });
    channel.publish("penjualan_logs", "", Buffer.from(message));
    res.json({ message: "Penjualan deleted successfully", id: PenjualanID });
  });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Close database connection when the app is terminated
process.on("SIGINT", () => {
  console.log("Closing MySQL connection...");
  db.end((err) => {
    if (err) {
      console.error("Error closing MySQL connection:", err);
    } else {
      console.log("MySQL connection closed");
    }
    process.exit();
  });
});
