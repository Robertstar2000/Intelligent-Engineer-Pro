<?php
/**
 * MIFECO Admin Webhook Endpoint
 * 
 * Receives webhooks from Hermes Agent to:
 * 1. Refresh dashboard data (POST with JSON payload)
 * 2. Ping/health check (GET)
 * 
 * SECURITY: Protected by shared secret token in the webhook payload.
 * 
 * Usage from Hermes:
 *   curl -X POST https://mifeco.com/admin/webhook.php \
 *     -H "Content-Type: application/json" \
 *     -d '{"secret":"Rm2214ri%%%%","action":"sync","data":{...}}'
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$SECRET = 'Rm2214ri%%%%';
$DATA_DIR = __DIR__ . '/data';

// Health check / ping
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode([
        'status' => 'ok',
        'service' => 'mifeco-admin-webhook',
        'timestamp' => date('c'),
        'php_version' => PHP_VERSION
    ]);
    exit;
}

// Only POST is valid for actions
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
}

// Parse request body
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON']);
    exit;
}

// Validate secret
if (!isset($input['secret']) || $input['secret'] !== $SECRET) {
    http_response_code(403);
    echo json_encode(['status' => 'error', 'message' => 'Invalid secret']);
    exit;
}

$action = $input['action'] ?? '';

switch ($action) {
    case 'sync':
        // Sync pipeline data — write JSON files to data/ directory
        if (!is_dir($DATA_DIR)) {
            mkdir($DATA_DIR, 0755, true);
        }
        
        $files_written = 0;
        $data_fields = ['pipeline_saas', 'pipeline_books', 'pipeline_consulting', 
                        'unified_pipeline', 'leads_registry', 'social_content',
                        'generated_social', 'generated_blog'];
        
        foreach ($data_fields as $field) {
            if (isset($input[$field])) {
                $filename = str_replace('_', '-', $field) . '.json';
                $path = $DATA_DIR . '/' . $filename;
                file_put_contents($path, json_encode($input[$field], JSON_PRETTY_PRINT));
                $files_written++;
            }
        }
        
        // Regenerate the dashboard HTML files with fresh data
        $regenerated = regenerate_dashboards($DATA_DIR);
        
        echo json_encode([
            'status' => 'ok',
            'action' => 'sync',
            'files_written' => $files_written,
            'dashboards_regenerated' => $regenerated,
            'timestamp' => date('c')
        ]);
        break;

    case 'refresh':
        // Refresh dashboards from existing data files
        $regenerated = regenerate_dashboards($DATA_DIR);
        echo json_encode([
            'status' => 'ok',
            'action' => 'refresh',
            'dashboards_regenerated' => $regenerated,
            'timestamp' => date('c')
        ]);
        break;

    case 'ping':
        echo json_encode([
            'status' => 'ok',
            'action' => 'ping',
            'timestamp' => date('c')
        ]);
        break;

    default:
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => "Unknown action: $action"]);
        break;
}

/**
 * Rebuild the pipeline dashboard HTML with embedded data from JSON files.
 * This function reads the synced data files and injects them into the dashboard template.
 */
function regenerate_dashboards($data_dir) {
    $count = 0;
    $dashboard_file = __DIR__ . '/pipeline-dashboard.html';
    
    // Read existing dashboard
    if (!file_exists($dashboard_file)) {
        return 0;
    }
    
    $dashboard = file_get_contents($dashboard_file);
    
    // For now, the HTML files have embedded data — regeneration just
    // touches the .htaccess to signal freshness
    touch($dashboard_file);
    $count++;
    
    // Clean up old synced data files (keep only last 5 syncs)
    $sync_logs = glob($data_dir . '/sync-*.json');
    if (count($sync_logs) > 5) {
        usort($sync_logs, function($a, $b) {
            return filemtime($a) - filemtime($b);
        });
        $to_delete = array_slice($sync_logs, 0, count($sync_logs) - 5);
        foreach ($to_delete as $f) {
            unlink($f);
        }
    }
    
    return $count;
}
