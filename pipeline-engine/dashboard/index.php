<?php
/**
 * MIFECO Admin — Password Gate
 * 
 * Single login gate that protects all admin dashboard pages.
 * Uses PHP sessions, email = Robertstar@aol.com, password = Rm2214ri#
 * 
 * Features:
 * - Password-protected access to /admin/
 * - Session persists for 2 hours
 * - Auto-redirects to dashboard after login
 * - Logout support
 */

session_start();

$ADMIN_EMAIL = 'Robertstar@aol.com';
$ADMIN_PASSWORD = 'Rm2214ri#';
$SESSION_TIMEOUT = 7200; // 2 hours
$DASHBOARD_DIR = __DIR__;

// Session timeout check
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
    if (time() - $_SESSION['login_time'] > $SESSION_TIMEOUT) {
        $_SESSION = [];
        session_destroy();
        header('Location: ?expired=1');
        exit;
    }
    $_SESSION['login_time'] = time(); // Refresh
}

// Handle logout
if (isset($_GET['logout'])) {
    $_SESSION = [];
    session_destroy();
    header('Location: ?logged_out=1');
    exit;
}

// Handle login
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password'])) {
    if ($_POST['email'] === $ADMIN_EMAIL && $_POST['password'] === $ADMIN_PASSWORD) {
        $_SESSION['logged_in'] = true;
        $_SESSION['login_time'] = time();
        // Redirect to dashboard or specified page
        $redirect = isset($_GET['redirect']) ? $_GET['redirect'] : 'pipeline-dashboard.html';
        // Sanitize redirect path
        $redirect = basename($redirect);
        header('Location: ' . $redirect);
        exit;
    } else {
        $error = 'Invalid email or password';
    }
}

// Already logged in — show the dashboard menu
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MIFECO Admin — Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 800px;
                width: 100%;
                padding: 2rem;
            }
            h1 {
                font-size: 2rem;
                font-weight: 700;
                color: #00ffcc;
                margin-bottom: 0.5rem;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                color: #94a3b8;
                margin-bottom: 2rem;
                font-size: 0.95rem;
            }
            .menu-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }
            .menu-card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 1.5rem;
                text-decoration: none;
                color: #e2e8f0;
                transition: all 0.2s;
                display: flex;
                flex-direction: column;
            }
            .menu-card:hover {
                border-color: #00ffcc;
                transform: translateY(-2px);
                box-shadow: 0 4px 20px rgba(0,255,204,0.1);
            }
            .menu-card .icon { font-size: 2rem; margin-bottom: 0.75rem; }
            .menu-card .title { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem; color: #00ffcc; }
            .menu-card .desc { font-size: 0.85rem; color: #94a3b8; }
            .footer {
                margin-top: 2rem;
                text-align: center;
                font-size: 0.85rem;
                color: #64748b;
            }
            .footer a { color: #00ffcc; text-decoration: none; }
            .footer a:hover { text-decoration: underline; }
            .expired, .logout {
                text-align: center;
                padding: 0.75rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                font-size: 0.9rem;
            }
            .expired { background: #7f1d1d; color: #fca5a5; }
            .logout { background: #14532d; color: #86efac; }
            @media (max-width: 600px) {
                .menu-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <?php if (isset($_GET['expired'])): ?>
                <div class="expired">⚠ Session expired — please log in again</div>
            <?php endif; ?>
            <?php if (isset($_GET['logged_out'])): ?>
                <div class="logout">✓ Logged out successfully</div>
            <?php endif; ?>
            
            <h1>⚙ MIFECO Admin</h1>
            <p class="subtitle">Pipeline Management & Content Dashboard</p>
            
            <div class="menu-grid">
                <a href="pipeline-dashboard.html" class="menu-card">
                    <div class="icon">📊</div>
                    <div class="title">Pipeline Dashboard</div>
                    <div class="desc">Leads, stages, blockers across Books, SaaS & Consulting</div>
                </a>
                <a href="content-command-center.html" class="menu-card">
                    <div class="icon">📱</div>
                    <div class="title">Content Command Center</div>
                    <div class="desc">Blog posts, social media, emails — stats & management</div>
                </a>
                <a href="outreach-dashboard.html" class="menu-card">
                    <div class="icon">📧</div>
                    <div class="title">Outreach Dashboard</div>
                    <div class="desc">Email campaigns, social outreach, brand advocacy</div>
                </a>
                <a href="kanban-dashboard.html" class="menu-card">
                    <div class="icon">📋</div>
                    <div class="title">Kanban Board</div>
                    <div class="desc">Pipeline task board — Books, SaaS, Consulting, Marketing</div>
                </a>
                <a href="https://mifeco.com/consult/survey.php?backdoor=1" class="menu-card">
                    <div class="icon">💼</div>
                    <div class="title">Virtual Consulting</div>
                    <div class="desc">Business assessment — backdoor login, skip payment</div>
                </a>
                <a href="https://mifeco.com/admin" target="_blank" class="menu-card">
                    <div class="icon">⚙️</div>
                    <div class="title">Hermes Admin</div>
                    <div class="desc">Agent dashboard — system monitor, config, sessions, tools</div>
                </a>
                <a href="?logout=1" class="menu-card" style="border-color: #7f1d1d;">
                    <div class="icon">🚪</div>
                    <div class="title">Logout</div>
                    <div class="desc">End your admin session</div>
                </a>
            </div>
            
            <div class="footer">
                MIFECO Admin &middot; &copy; 2026 &middot; 
                <a href="https://mifeco.com" target="_blank">Back to mifeco.com</a>
            </div>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// Show login form
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIFECO Admin — Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 2.5rem;
            width: 380px;
            max-width: 90vw;
        }
        .login-box h1 {
            font-size: 1.5rem;
            color: #00ffcc;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .login-box p {
            text-align: center;
            color: #94a3b8;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }
        .login-box input[type="password"] {
            width: 100%;
            padding: 0.75rem 1rem;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #e2e8f0;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
            margin-bottom: 1rem;
        }
        .login-box input[type="password"]:focus {
            border-color: #00ffcc;
        }
        .login-box button {
            width: 100%;
            padding: 0.75rem;
            background: #00ffcc;
            color: #0f172a;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .login-box button:hover { opacity: 0.9; }
        .error {
            background: #7f1d1d;
            color: #fca5a5;
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            text-align: center;
            font-size: 0.9rem;
        }
        .hint {
            text-align: center;
            color: #475569;
            font-size: 0.8rem;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔐 MIFECO Admin</h1>
        <p>Enter credentials to access dashboards</p>
        
        <?php if ($error): ?>
            <div class="error">✗ <?= htmlspecialchars($error) ?></div>
        <?php endif; ?>
        
        <form method="POST">
            <input type="email" name="email" placeholder="Email" autofocus required style="margin-bottom: 0.75rem;">
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Unlock</button>
        </form>
        <div class="hint">Authorized personnel only</div>
    </div>
</body>
</html>
