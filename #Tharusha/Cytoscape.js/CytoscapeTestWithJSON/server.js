const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('public')); // Serves files from the 'public' directory

// Route to reset JSON data when the page is loaded
app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'data.json');
    
    // Reset the JSON file
    fs.writeFile(filePath, '{}', 'utf8', (err) => {
        if (err) {
            console.error('Error resetting JSON file:', err);
        }
        // Serve the HTML page after resetting JSON
        res.sendFile(path.join(__dirname, 'public', 'index.html'));
    });
});

// Route to handle JSON updates
app.post('/update_json', (req, res) => {
    const data = req.body;
    const filePath = path.join(__dirname, 'data.json');

    fs.readFile(filePath, 'utf8', (err, jsonData) => {
        if (err) {
            console.error('Error reading file:', err);
            return res.status(500).send('Error reading file');
        }

        let json = {};
        try {
            json = JSON.parse(jsonData);
        } catch (e) {
            console.error('Error parsing JSON:', e);
            return res.status(500).send('Error parsing JSON');
        }

        // Update JSON with new data
        json[data.keyword] = data.details;

        fs.writeFile(filePath, JSON.stringify(json, null, 2), 'utf8', (err) => {
            if (err) {
                console.error('Error writing file:', err);
                return res.status(500).send('Error writing file');
            }
            res.json({ message: 'JSON updated successfully' });
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
