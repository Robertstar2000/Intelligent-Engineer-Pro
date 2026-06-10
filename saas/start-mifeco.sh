#!/bin/bash
# MIFECO Startup — launches all three SaaS apps + dashboard
DIR="/home/bob/saas"

echo "🚀 MIFECO Operations Startup"
echo "================================"

# Start Project Hypatia Pro on :3001
cd "$DIR/Project_Hypatia_Pro"
PORT=3001 nohup npx tsx server.ts > /tmp/hypatia-pro.log 2>&1 &
echo "  🔬 Hypatia Pro    → :3001  (PID $!)"

# Start PMA on :3002
cd "$DIR/Project_Management_Accelerator"
PORT=3002 nohup npx tsx server.ts > /tmp/pma.log 2>&1 &
echo "  📊 PMA Accelerator → :3002  (PID $!)"

# Start VibraEngineer on :3003
cd "$DIR/VibraEngineer"
PORT=3003 nohup npx tsx server.ts > /tmp/vibraengineer.log 2>&1 &
echo "  🔧 VibraEngineer   → :3003  (PID $!)"

# Wait for apps to start
sleep 4

# Start Dashboard on :5540
cd "$DIR/mifeco-dashboard"
nohup python3 app.py > /tmp/mifeco-dashboard.log 2>&1 &
echo "  🖥️  MIFECO Dashboard → :5540  (PID $!)"

echo ""
echo "✅ All services started!"
echo "   Dashboard: http://localhost:5540"
