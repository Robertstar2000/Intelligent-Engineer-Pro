# DreamHost to Local Python API — SSH Reverse Tunnel Setup

## Problem
DreamHost PHP cant reach Python API on port 8190 (NAT/firewall).
Public IP 97.91.18.250:8190 is unreachable from DreamHost.

## Solution: SSH Reverse Tunnel
SSH from local machine to DreamHost with -R flag:
 ssh -R 8190:localhost:8190 dh_mwpxuu@ssh.mifeco.com -N

This makes DreamHost localhost:8190 forward to local port 8190.

Persistent version uses paramiko in /tmp/reverse_tunnel.py

## PHP Config
Change PYTHON_API_URL in DreamHost config.php:
 FROM: http://97.91.18.250:8190
 TO:   http://127.0.0.1:8190

## Key Files
- Tunnel script: /tmp/reverse_tunnel.py
- API server: /mnt/usb_4tb/consulting/api/api_server.py
- Venv with paramiko: /tmp/tunnel-env/
- Monitor cron (5min): job 20aa67570b2d

## Install Paramiko
 uv venv /tmp/tunnel-env
 uv pip install paramiko --python /tmp/tunnel-env/bin/python

## Test from DreamHost via SSH
 curl -s http://127.0.0.1:8190/api/generate-questions \
   -H 'Content-Type: application/json' \
   -d '{"api_key":"mifeco-local-api-key-change-this","business_role":"owner"}'
