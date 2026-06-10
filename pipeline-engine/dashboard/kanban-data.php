<?php
/**
 * Kanban Data Proxy — Pipeline-Aware
 * Serves tasks from JSON pipeline files (no DB required on DreamHost).
 * Called by kanban-dashboard.html to populate pipeline boards.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$tasks = [];

// Primary: read from SQLite kanban DB (try local, then DreamHost path)
$dbPaths = [
    '/home/bob/.hermes/kanban.db',
    '/home/dh_mwpxuu/mifeco.com/admin/kanban.db',
];
$dbPath = null;
foreach ($dbPaths as $p) {
    if (file_exists($p)) { $dbPath = $p; break; }
}
if (file_exists($dbPath)) {
    try {
        $db = new SQLite3($dbPath);
        $result = $db->query("
            SELECT id, title, body, assignee, status, priority, tenant, stage, created_at 
            FROM tasks 
            WHERE status != 'archived' 
            ORDER BY created_at ASC
        ");
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $tasks[] = [
                'id'        => $row['id'],
                'title'     => $row['title'],
                'body'      => $row['body'],
                'assignee'  => $row['assignee'] ?? '',
                'status'    => $row['status'] ?? 'ready',
                'priority'  => mapPriority((int)($row['priority'] ?? 2)),
                'pipeline'  => $row['tenant'] ?? 'default',
                'stage'     => (int)($row['stage'] ?? 1),
                'created_at'=> $row['created_at'] ? date('c', $row['created_at']) : null,
            ];
        }
        $db->close();
    } catch (Exception $e) {
        // DB not accessible, fall through to JSON
    }
}

// Fallback: read from JSON pipeline files (DreamHost / portable)
if (empty($tasks)) {
    $jsonDir = __DIR__;
    
    // Unified pipeline definitions
    $unifiedFile = $jsonDir . '/unified-pipeline.json';
    $pipelineDefs = [];
    if (file_exists($unifiedFile)) {
        $unified = json_decode(file_get_contents($unifiedFile), true);
        if (isset($unified['pipelines'])) {
            foreach ($unified['pipelines'] as $p) {
                $pipelineDefs[$p['id']] = $p;
            }
        }
    }
    
    // Pipeline data files
    $dataFiles = [
        'pipeline-books.json' => 'books',
        'pipeline-saas.json' => 'saas',
        'pipeline-consulting.json' => 'consulting',
    ];
    
    foreach ($dataFiles as $file => $type) {
        $path = $jsonDir . '/' . $file;
        if (!file_exists($path)) continue;
        $data = json_decode(file_get_contents($path), true);
        if (!$data) continue;
        
        $pipeline = $data['pipeline'] ?? [];
        $leads = $pipeline['leads'] ?? [];
        $stages = $pipeline['stages'] ?? [];
        
        // For consulting, check sub-pipelines
        if ($type === 'consulting') {
            $leads = [];
            foreach (['human', 'virtual'] as $sub) {
                if (isset($pipeline['pipelines'][$sub])) {
                    $subLeads = $pipeline['pipelines'][$sub]['leads'] ?? [];
                    foreach ($subLeads as &$lead) {
                        $lead['_sub'] = $sub;
                    }
                    $leads = array_merge($leads, $subLeads);
                }
            }
            // Use human consulting stages as default
            $stages = $pipeline['pipelines']['human']['stages'] ?? $stages;
        }
        
        foreach ($leads as $lead) {
            $pipelineId = $type;
            if ($type === 'consulting') {
                $pipelineId = ($lead['_sub'] === 'virtual') ? 'virtual-consulting' : 'human-consulting';
            }
            if ($type === 'books') {
                // Determine if this is books-creation or books-marketing based on stage names
                $firstStage = is_array($stages) ? reset($stages) : null;
                if ($firstStage && is_array($firstStage) && isset($firstStage['name'])) {
                    $name = $firstStage['name'];
                    if (stripos($name, 'marketing') !== false || stripos($name, 'promote') !== false || stripos($name, 'content') !== false) {
                        $pipelineId = 'books-marketing';
                    } else {
                        $pipelineId = 'books-creation';
                    }
                }
            }
            
            $stageId = (int)($lead['current_stage'] ?? $lead['stage'] ?? 1);
            
            $tasks[] = [
                'id'        => $lead['id'] ?? uniqid($type . '-'),
                'title'     => $lead['contact']['name'] ?? $lead['name'] ?? $lead['contact_name'] ?? $lead['title'] ?? 'Untitled',
                'body'      => $lead['notes'] ?? $lead['body'] ?? '',
                'assignee'  => getAssignee($type, $pipelineId),
                'status'    => mapStatus($lead['status'] ?? 'ready'),
                'priority'  => mapPriorityFromLead($lead),
                'pipeline'  => $pipelineId,
                'stage'     => $stageId,
                'created_at'=> $lead['created_at'] ?? $lead['created_date'] ?? null,
            ];
        }
    }
}

function getAssignee($type, $pipelineId) {
    if ($pipelineId === 'books-creation' || $pipelineId === 'books-marketing') {
        return $pipelineId === 'books-creation' ? 'writer' : 'marketing';
    }
    if ($pipelineId === 'saas') return 'sales';
    if ($pipelineId === 'human-consulting' || $pipelineId === 'virtual-consulting') return 'consultant';
    return 'agent';
}

function mapPriorityFromLead($lead) {
    // Higher priority for contacted/leads
    $stage = $lead['current_stage'] ?? $lead['stage'] ?? 1;
    $status = $lead['status'] ?? '';
    if ($stage >= 3 && $status !== 'new') return 'high';
    if ($stage >= 2) return 'normal';
    return 'low';
}

function mapPriority($p) {
    if ($p >= 3) return 'high';
    if ($p >= 2) return 'normal';
    return 'low';
}

function mapStatus($status) {
    $map = [
        'ready' => 'ready',
        'pending' => 'ready',
        'assigned' => 'assigned',
        'active' => 'active',
        'completed' => 'completed',
        'failed' => 'failed',
        'blocked' => 'blocked',
        'new' => 'ready',
        'contacted' => 'assigned',
        'contact' => 'assigned',
        'qualified' => 'assigned',
        'draft' => 'ready',
        'published' => 'completed',
    ];
    return $map[$status] ?? 'ready';
}

// Group by pipeline for the dashboard
$pipelines = [];
foreach ($tasks as $t) {
    $pl = $t['pipeline'];
    if (!isset($pipelines[$pl])) $pipelines[$pl] = [];
    $pipelines[$pl][] = $t;
}

echo json_encode([
    'tasks'      => $tasks,
    'pipelines'  => $pipelines,
    'updated_at' => date('c'),
    'source'     => empty($tasks) ? 'none' : 'json-files',
    'count'      => count($tasks),
], JSON_PRETTY_PRINT);
