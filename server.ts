
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import bcrypt from 'bcryptjs';
import { createServer as createViteServer } from 'vite';
import path from 'path';
import { fileURLToPath } from 'url';
import { createFirebaseIdentityHandler, verifyFirebaseToken } from './server/firebaseIdentity.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
    const app = express();
    const PORT = parseInt(process.env.PORT || "3000", 10);

    app.use(cors());
    app.use(express.json());
    app.use(helmet());

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

    app.get('/health', async (_req, res) => {
        try {
            await db.get('SELECT 1 AS ok');
            res.json({ status: 'ok', service: 'intelligent-engineer-pro' });
        } catch {
            res.status(503).json({ status: 'error', service: 'intelligent-engineer-pro' });
        }
    });

    // Uses the same Firebase identity as the current frontend. It grants no entitlement.
    app.get('/api/auth/firebase/me', createFirebaseIdentityHandler({
        projectId: process.env.FIREBASE_PROJECT_ID,
        verifyToken: verifyFirebaseToken,
    }));

    // Legacy SQLite routes remain separate until an explicit identity migration.
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

    app.use('/api', (_req, res) => {
        res.status(404).json({ error: 'API endpoint not found' });
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
        app.get('/{*splat}', (req, res) => {
            res.sendFile(path.join(__dirname, 'dist', 'index.html'));
        });
    }

    app.listen(PORT, '0.0.0.0', () => {
        console.log(`Server running on http://localhost:${PORT}`);
    });
}

startServer();
