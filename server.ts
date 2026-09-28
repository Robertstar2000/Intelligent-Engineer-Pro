
import express from 'express';
import helmet from 'helmet';

import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

import { createServer as createViteServer } from 'vite';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';
import { currentUser, installSecureAuth, type AuthDb } from './secureAuth.ts';
import { installEntitlementMiddleware } from '../entitlementMiddleware.mts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
    const app = express();
    const PORT = parseInt(process.env.PORT || "3000", 10);


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


    // Initialize SQLite
    const db = await open({
        filename: process.env.AUTH_DB_PATH || path.join(__dirname, 'database.sqlite'),
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

    app.get('/health', async (_req, res) => {
        try {
            await db.get('SELECT 1 AS ok');
            res.status(200).json({ status: 'ok', service: 'vibe-engineer' });
        } catch (error) {
            console.error('Health check failed:', error);
            res.status(503).json({ status: 'error', service: 'vibe-engineer' });
        }
    });

    app.get('/api/health', async (_req, res) => {
        try {
            await db.get('SELECT 1 AS ok');
            res.status(200).json({ status: 'ok', service: 'vibe-engineer' });
        } catch (error) {
            console.error('Health check failed:', error);
            res.status(503).json({ status: 'error', service: 'vibe-engineer' });
        }
    });

    const authDb: AuthDb = {
        exec: (sql) => db.exec(sql),
        get: (sql, params = []) => db.get(sql, params),
        all: (sql, params = []) => db.all(sql, params),
        run: async (sql, params = []) => { const r = await db.run(sql, params); return { changes: r.changes, lastID: r.lastID }; },
    };
    await installSecureAuth(app, authDb, 'passwordHash');
    await installEntitlementMiddleware(app, authDb, 'vibra', currentUser);


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

    app.listen(PORT, '127.0.0.1', () => {
        console.log(`Server running on http://localhost:${PORT}`);
    });
}

startServer();
