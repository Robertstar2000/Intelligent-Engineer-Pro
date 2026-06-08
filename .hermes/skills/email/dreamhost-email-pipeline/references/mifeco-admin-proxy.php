<?php
/**
 * Plugin Name: MIFECO Admin Dashboard Proxy
 * Description: Reverse proxies /admin to the Hermes Agent native dashboard at 127.0.0.1:9119
 * Version: 1.0.0
 * Author: MIFECO
 */

if (!defined('ABSPATH')) exit;

class MIFECO_Admin_Proxy {
    
    // Hermes dashboard runs on localhost only
    private $proxy_target = 'http://127.0.0.1:9119';
    
    // Simple access token — must be present in the URL or cookie
    private $access_token = 'MIFECO_admin_2026';

    public function __construct() {
        add_action('init', [$this, 'handle_admin_proxy']);
    }

    /**
     * Intercept /admin requests and proxy to Hermes dashboard
     */
    public function handle_admin_proxy() {
        $request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
        $request_uri = rtrim($request_uri, '/');
        
        // Only handle /admin/* requests
        if (strpos($request_uri, '/admin') !== 0) {
            return;
        }

        // Allow /admin/auth for token-based login
        if ($request_uri === '/admin/auth') {
            $this->handle_auth();
            exit;
        }

        // Check for valid session or token
        session_start();
        $token = isset($_GET['token']) ? sanitize_text_field($_GET['token']) : '';
        
        if (!isset($_SESSION['mifeco_admin']) || $_SESSION['mifeco_admin'] !== true) {
            if ($token !== $this->access_token) {
                // Show login page
                $this->render_login_page();
                exit;
            }
            // Token valid — set session
            $_SESSION['mifeco_admin'] = true;
            $_SESSION['mifeco_admin_time'] = time();
        }

        // Session timeout — 2 hours
        if (time() - $_SESSION['mifeco_admin_time'] > 7200) {
            $_SESSION = [];
            session_destroy();
            $this->render_login_page('Session expired. Please log in again.');
            exit;
        }
        $_SESSION['mifeco_admin_time'] = time();

        // Handle logout
        if ($request_uri === '/admin/logout') {
            $_SESSION = [];
            session_destroy();
            wp_redirect(home_url('/admin'));
            exit;
        }

        // Proxy the request to Hermes dashboard
        $this->proxy_request($request_uri);
        exit;
    }

    /**
     * Handle token-based auth
     */
    private function handle_auth() {
        $token = isset($_GET['token']) ? sanitize_text_field($_GET['token']) : '';
        $redirect = isset($_GET['redirect']) ? esc_url_raw($_GET['redirect']) : home_url('/admin');
        
        if ($token === $this->access_token) {
            session_start();
            $_SESSION['mifeco_admin'] = true;
            $_SESSION['mifeco_admin_time'] = time();
            wp_redirect($redirect);
            exit;
        }
        
        wp_die('Invalid access token', 'Access Denied', ['response' => 403]);
    }

    /**
     * Reverse proxy to Hermes dashboard
     */
    private function proxy_request($request_uri) {
        // Strip /admin prefix for the proxy target
        $proxy_path = preg_replace('#^/admin#', '', $request_uri);
        if (empty($proxy_path)) {
            $proxy_path = '/';
        }
        
        $proxy_url = $this->proxy_target . $proxy_path;
        
        // Preserve query string
        if (!empty($_SERVER['QUERY_STRING'])) {
            $proxy_url .= '?' . $_SERVER['QUERY_STRING'];
        }

        // Build headers to forward
        $headers = [];
        foreach (['Accept', 'Accept-Language', 'Content-Type', 'X-Requested-With'] as $h) {
            $key = 'HTTP_' . str_replace('-', '_', strtoupper($h));
            if (isset($_SERVER[$key])) {
                $headers[] = $h . ': ' . $_SERVER[$key];
            }
        }

        // Forward the request
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $proxy_url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HEADER => true,
            CURLOPT_CUSTOMREQUEST => $_SERVER['REQUEST_METHOD'],
            CURLOPT_HTTPHEADER => $headers,
        ]);

        // Forward POST/PUT body
        if (in_array($_SERVER['REQUEST_METHOD'], ['POST', 'PUT', 'PATCH'])) {
            $body = file_get_contents('php://input');
            if (!empty($body)) {
                curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
            }
        }

        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $response_headers = substr($response, 0, $header_size);
        $response_body = substr($response, $header_size);
        $content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
        curl_close($ch);

        // Forward response headers (skip transfer-encoding and connection)
        $skip_headers = ['transfer-encoding', 'connection', 'keep-alive'];
        foreach (explode("\r\n", $response_headers) as $header) {
            $header_lower = strtolower($header);
            $skip = false;
            foreach ($skip_headers as $s) {
                if (strpos($header_lower, $s) === 0) {
                    $skip = true;
                    break;
                }
            }
            if (!$skip && !empty($header) && strpos($header, 'HTTP/') !== 0) {
                header($header);
            }
        }

        status_header($http_code);
        if ($content_type) {
            header('Content-Type: ' . $content_type);
        }
        
        echo $response_body;
    }

    /**
     * Render the admin login page
     */
    private function render_login_page($error = '') {
        $token_url = home_url('/admin/auth?token=' . $this->access_token);
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
                    width: 400px;
                    max-width: 90vw;
                }
                .login-box h1 { font-size: 1.5rem; color: #00ffcc; margin-bottom: 0.5rem; text-align: center; }
                .login-box p { text-align: center; color: #94a3b8; font-size: 0.9rem; margin-bottom: 1.5rem; }
                .login-box input[type="password"] {
                    width: 100%; padding: 0.75rem 1rem; background: #0f172a; border: 1px solid #334155;
                    border-radius: 8px; color: #e2e8f0; font-size: 1rem; outline: none; margin-bottom: 1rem;
                }
                .login-box input[type="password"]:focus { border-color: #00ffcc; }
                .login-box button {
                    width: 100%; padding: 0.75rem; background: #00ffcc; color: #0f172a;
                    border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer;
                }
                .login-box button:hover { opacity: 0.9; }
                .error { background: #7f1d1d; color: #fca5a5; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; text-align: center; font-size: 0.9rem; }
                .hint { text-align: center; color: #475569; font-size: 0.8rem; margin-top: 1rem; }
                .token-link { text-align: center; margin-top: 1rem; }
                .token-link a { color: #00ffcc; font-size: 0.85rem; text-decoration: none; }
                .token-link a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>🔐 MIFECO Admin</h1>
                <p>Access the Hermes Agent dashboard</p>
                <?php if ($error): ?>
                    <div class="error">⚠ <?= htmlspecialchars($error) ?></div>
                <?php endif; ?>
                <form method="POST" action="">
                    <input type="password" name="admin_password" placeholder="Password" autofocus required>
                    <button type="submit">Unlock</button>
                </form>
                <div class="token-link">
                    <a href="<?= esc_url($token_url) ?>">🔑 Direct access link (bookmark this)</a>
                </div>
                <div class="hint">Authorized personnel only</div>
            </div>
        </body>
        </html>
        <?php
    }
}

new MIFECO_Admin_Proxy();
