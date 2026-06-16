# SSH Reverse Tunnel for DreamHost → Local Service

## When to Use
When a PHP app on DreamHost needs to call a Python API (or any service) running on your local machine, and:
- The local machine is behind NAT/firewall (no public port available)
- You have SSH access to DreamHost
- You can't use cloudflared/ngrok (no public tunnel endpoint)

## The Technique: SSH Reverse Tunnel via Paramiko

DreamHost's SSH server allows remote port forwarding (`-R`). This means: "when someone connects to DreamHost's localhost:PORT, forward that connection to my local machine's localhost:PORT."

### Architecture
```
DreamHost PHP → http://127.0.0.1:8190 → [SSH tunnel] → your-machine:8190 (Python API)
```

The PHP code connects to `http://127.0.0.1:8190` on DreamHost. The SSH tunnel makes DreamHost's localhost:8190 forward through the SSH connection to your machine's port 8190.

### Setup Script

```python
# /tmp/reverse_tunnel.py
import paramiko, socket, select, threading, time

HOST = "ssh.mifeco.com"
USER = "dh_mwpxuu"
PASS = "your-password"
REMOTE_PORT = 8190
LOCAL_PORT = 8190

def forward_tunnel(transport, remote_port, local_host, local_port):
    def handler(chan, host, port):
        sock = socket.socket()
        try:
            sock.connect((host, port))
        except Exception:
            chan.close()
            return
        while True:
            r, w, x = select.select([sock, chan], [], [])
            if sock in r:
                data = sock.recv(1024)
                if len(data) == 0: break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0: break
                sock.send(data)
        chan.close()
        sock.close()

    transport.request_port_forward("", remote_port)
    print(f"Tunnel active: DreamHost:{remote_port} -> {local_host}:{local_port}")
    while transport.is_active():
        chan = transport.accept(1000)
        if chan is None: continue
        thr = threading.Thread(target=handler, args=(chan, local_host, local_port))
        thr.setDaemon(True)
        thr.start()

while True:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS, timeout=15,
                     allow_agent=False, look_for_keys=False)
        forward_tunnel(client.get_transport(), REMOTE_PORT, "127.0.0.1", LOCAL_PORT)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}. Reconnecting in 10s...")
        time.sleep(10)
```

### Deployment Steps

1. **Start your local service first** (e.g., Python API on port 8190)
2. **Start the tunnel**: `python3 /tmp/reverse_tunnel.py` (or use cron/systemd)
3. **Update PHP config** to use `http://127.0.0.1:8190` instead of the public IP
4. **Deploy updated config** to DreamHost via SFTP
5. **Test**: SSH to DreamHost, `curl http://127.0.0.1:8190/api/health`

### Making It Persistent

Use a cron job to monitor and restart:

```
# Cron: every 5 minutes, check if tunnel is running
*/5 * * * * pgrep -f reverse_tunnel.py > /dev/null || (cd /tmp && python3 reverse_tunnel.py &)
```

Or create a systemd user service that runs the tunnel script with `Restart=always`.

### Pitfalls

- **DreamHost must allow remote port forwarding**: Test with `ssh -R 8191:localhost:8190 dh_mwpxuu@ssh.mifeco.com` first. If it hangs or errors, the feature may be disabled.
- **Port conflicts**: If another user/service on DreamHost is already using the remote port, the tunnel will fail. Try a different port.
- **Tunnel dies on disconnect**: The script above auto-reconnects. Without auto-reconnect, the tunnel dies if the SSH connection drops.
- **PHP must use 127.0.0.1, not the public IP**: The whole point is that DreamHost's localhost forwards through the tunnel. Using the public IP bypasses the tunnel.
- **Firewall on your local machine**: Make sure your local firewall allows connections on the port (it should since it's localhost→localhost).

### Verifying the Tunnel Works

```bash
# From your machine, SSH to DreamHost and test:
ssh dh_mwpxuu@ssh.mifeco.com
curl -s http://127.0.0.1:8190/api/generate-questions -H 'Content-Type: application/json' -d '{"api_key":"...","business_role":"owner"}'
```

If this returns a response, the tunnel is working.
