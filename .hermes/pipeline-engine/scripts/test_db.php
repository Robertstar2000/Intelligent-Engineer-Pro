<?php
// Test script for DreamHost kanban DB access
header('Content-Type: text/plain');

// Test 1: DB exists?
$dbPath = '/home/dh_mwpxuu/mifeco.com/admin/kanban.db';
echo "DB exists: " . (file_exists($dbPath) ? 'YES' : 'NO') . "\n";

// Test 2: Can we read?
$db = new SQLite3($dbPath);
$r = $db->query('SELECT COUNT(*) FROM tasks');
$count = $r->fetchArray()[0];
echo "Task count: $count\n";

// Test 3: Pipeline breakdown
$r2 = $db->query('SELECT tenant, stage, COUNT(*) as cnt FROM tasks GROUP BY tenant, stage ORDER BY tenant, stage');
echo "\nPipeline breakdown:\n";
while ($row = $r2->fetchArray(SQLITE3_ASSOC)) {
    echo "  {$row['tenant']} stage {$row['stage']}: {$row['cnt']}\n";
}
$db->close();
