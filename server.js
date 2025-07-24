// server.js
const express = require('express');
const sql = require('mssql');
const cors = require('cors');

const app = express();
const PORT = 1433;

app.use(cors());

// SQL Server connection config
const config = {
    user: 'voiceadmin',
    password: 'Voice@dm!n',    
    server: 'jdbc:sqlserver://july-hackathon.database.windows.net:1433', // e.g., 'localhost'
    database: 'voice_nba',
    options: {
        encrypt: true,
        trustServerCertificate: true,
    },
};

app.get('/api/tickets', async (req, res) => {
    try {
        await sql.connect(config);
        const result = await sql.query(`
            SELECT ticket_number, 
                   creation_date, 
                   current_Status, 
                   assigned_to, 
                   priority, 
                   subject, 
                   any_other_comments
            FROM voice_nba.dbo.voice_tickets;
        `);
        res.json(result.recordset);
    } catch (err) {
        console.error(err);
        res.status(500).send('Server error');
    }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));