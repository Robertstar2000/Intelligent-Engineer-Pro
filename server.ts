
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import bcrypt from 'bcryptjs';
import { createServer as createViteServer } from 'vite';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
    const app = express();
    const PORT = parseInt(process.env.PORT || "3000", 10);

    app.use(cors());
    app.use(express.json({ limit: '50mb' }));
    app.use(helmet());

    app.post('/api/artifacts', async (req, res) => {
        try {
            const { app: appName, projectId, source, prompt, timestamp, generator, model, data, mimeType, structuredData } = req.body || {};
            if (appName !== 'Vibe Engineer' || !projectId || !source || !prompt || !data || generator !== 'Designer/Gemini') return res.status(400).json({ error: 'Invalid artifact payload' });
            const safeProjectId = String(projectId).replace(/[^a-zA-Z0-9_-]/g, '_');
            const safeSource = String(source).replace(/[^a-zA-Z0-9_-]/g, '_');
            const dir = path.join(__dirname, 'artifacts', safeProjectId);
            await fs.mkdir(dir, { recursive: true });
            const imagePath = path.join(dir, `${Date.now()}-${safeSource}.png`);
            const tempPath = `${imagePath}.tmp`;
            await fs.writeFile(tempPath, Buffer.from(String(data).replace(/^data:image\/[^;]+;base64,/, ''), 'base64'));
            await fs.rename(tempPath, imagePath);
            const provenance = { app: appName, projectId: safeProjectId, source, prompt, timestamp: timestamp || new Date().toISOString(), generator, model, mimeType: mimeType || 'image/png', path: imagePath, structuredData };
            await fs.writeFile(`${imagePath}.provenance.json`, JSON.stringify(provenance, null, 2));
            res.status(201).json(provenance);
        } catch (error: any) {
            res.status(500).json({ error: error.message });
        }
    });

    // Gemini same-origin proxy for restricted browser environments
    app.use('/gapi', async (req: any, res: any) => {
        try {
            const targetPath = req.originalUrl.replace(/^\/gapi/, '');
            const url = 'https://generativelanguage.googleapis.com' + targetPath;
            const fetchOpts: any = { method: req.method, headers: { 'Content-Type': 'application/json' } };
            const apiKey = req.headers['x-goog-api-key'] || req.query.key;
            if (apiKey) fetchOpts.headers['x-goog-api-key'] = apiKey;
            if (req.method !== 'GET' && req.method !== 'HEAD') fetchOpts.body = JSON.stringify(req.body);
            const r = await fetch(url, fetchOpts);
            const text = await r.text();
            res.status(r.status).set('Content-Type', r.headers.get('content-type') || 'application/json').send(text);
        } catch (e: any) {
            res.status(502).json({ error: 'gemini proxy failed: ' + e.message });
        }
    });


    // Firebase REST passthrough (same-origin shim)
    app.use('/fapi', async (req: any, res: any) => {
        try {
            const targetPath = req.originalUrl.replace(/^\/fapi/, '');
            const url = 'https://identitytoolkit.googleapis.com' + targetPath;
            const fetchOpts: any = { method: req.method, headers: { 'Content-Type': 'application/json' } };
            if (req.method !== 'GET' && req.method !== 'HEAD') fetchOpts.body = JSON.stringify(req.body);
            const r = await fetch(url, fetchOpts);
            const text = await r.text();
            res.status(r.status).set('Content-Type', r.headers.get('content-type') || 'application/json').send(text);
        } catch (e: any) {
            res.status(502).json({ error: 'fb proxy failed: ' + e.message });
        }
    });

    // Initialize SQLite
    const db = await open({
        filename: './database.sqlite',
        driver: sqlite3.Database
    });

    await db.exec(`
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            passwordHash TEXT,
            geminiKey TEXT,
            role TEXT,
            avatar TEXT
        )
    `);

    // Auth Routes
    app.post('/api/auth/signup', async (req, res) => {
        const { username, email, password, geminiKey } = req.body;
        try {
            const id = Math.random().toString(36).substring(2, 15);
            const passwordHash = await bcrypt.hash(password, 10);
            await db.run(
                'INSERT INTO users (id, username, email, passwordHash, geminiKey, role, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)',
                [id, username, email, passwordHash, geminiKey, 'Engineer', '👤']
            );
            const user = { id, username, email, geminiKey, role: 'Engineer', avatar: '👤' };
            res.json({ success: true, user });
        } catch (error: any) {
            res.status(400).json({ success: false, message: error.message });
        }
    });

    app.post('/api/auth/login', async (req, res) => {
        const { emailOrUsername, password } = req.body;
        try {
            const user = await db.get(
                'SELECT * FROM users WHERE email = ? OR username = ?',
                [emailOrUsername, emailOrUsername]
            );

            if (user && await bcrypt.compare(password, user.passwordHash)) {
                const { passwordHash, ...userWithoutPassword } = user;
                res.json({ success: true, user: userWithoutPassword });
            } else {
                res.status(401).json({ success: false, message: 'Invalid credentials' });
            }
        } catch (error: any) {
            res.status(500).json({ success: false, message: error.message });
        }
    });

    // Vite middleware for development
    if (process.env.NODE_ENV !== 'production') {
        const vite = await createViteServer({
            server: { middlewareMode: true },
            appType: 'spa',
        });
        app.use(vite.middlewares);
    } else {
        app.use(express.static(path.join(__dirname, 'dist')));
        app.get('*splat', (req, res) => {
            res.sendFile(path.join(__dirname, 'dist', 'index.html'));
        });
    }

    app.listen(PORT, '0.0.0.0', () => {
        console.log(`Server running on http://localhost:${PORT}`);
    });
}

startServer();
