const express = require("express");
const router = express.Router();

router.post("/generate", (req, res) => {
    res.json({ message: "Generate Certificate API" });
});

router.post("/bulk-upload", (req, res) => {
    res.json({ message: "Bulk Upload API" });
});

router.get("/verify/:id", (req, res) => {
    res.json({ message: "Verify Certificate API" });
});

router.get("/download/:id", (req, res) => {
    res.json({ message: "Download Certificate API" });
});

module.exports = router;