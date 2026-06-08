---
name: nomachine-unattended-access
description: "Install and configure NoMachine for unattended remote desktop access on Linux. Covers downloading (bypassing JS redirects), installation, config for no-approval access, and user setup."
category: devops
tags: [remote-desktop, nomachine, linux, unattended, systemd]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# NoMachine Unattended Remote Access Setup

Use this skill when the user wants to install NoMachine and configure it for external/remote access without requiring anyone at the physical machine to approve connections.

## Prerequisites

- Linux with X11 display (`DISPLAY=:0`, `XDG_SESSION_TYPE=x11`)
- GDM/LightDM/SDDM running
- sudo access
- System username and password

## Steps

### 1. Detect current state

```bash
dpkg -l | grep -i nomachine || echo "not installed"
uname -m  # x86_64 or aarch64
echo $DISPLAY $XDG_SESSION_TYPE
```

### 2. Download NoMachine

**PITFALL**: Direct `wget`/`curl` to `https://download.nomachine.com/...` URLs will fail with HTML redirects (NoMachine requires browser cookies/sessions). You must use the CDN URLs directly:

For amd64/x86_64:
```
https://web9001.nomachine.com/download/9.4/Linux/nomachine_9.4.14_1_amd64.deb
```

For i386:
```
https://web9001.nomachine.com/download/9.4/Linux/nomachine_9.4.14_1_i386.deb
```

Use the browser tool to navigate to `https://www.nomachine.com/download` -> click "NoMachine for Linux" -> extract the actual download URL if the version changes.

```bash
cd /tmp
wget -q --show-progress -O nomachine.deb "https://web9001.nomachine.com/download/9.4/Linux/nomachine_9.4.14_1_amd64.deb"
file /tmp/nomachine.deb  # Should say "Debian binary package", NOT "HTML document"
```

### 3. Install the package

**PITFALL**: If sudo requires a password, you cannot use `sudo` interactively from non-PTY terminal. You MUST pipe via `echo "password" | sudo -S`.

```bash
echo "USER_PASSWORD" | sudo -S dpkg -i /tmp/nomachine.deb
sudo apt-get install -f -y  # Fix any dependency issues
```

### 4. Configure for unattended access

**PITFALL**: Writing the config via `echo "..." | sudo -S bash -c "..."` with multiple commands often fails due to escaping/timing issues. Write a script file first, then execute it.

Create `/tmp/nm_config.sh`:
```bash
#!/bin/bash
cd /usr/NX/etc

# Enable UPnP for port forwarding
sed -i "s/^#EnableUPnP none/EnableUPnP all/" server.cfg

# Physical desktop access for all user types
sed -i "s/^#PhysicalDesktopAccess administrator,trusted,system,guest,owner/PhysicalDesktopAccess administrator,trusted,system,guest,owner/" server.cfg

# Physical desktop mode: interactive (full control)
sed -i "s/^#PhysicalDesktopMode 2/PhysicalDesktopMode 2/" server.cfg

# No acceptance popup needed for admin/trusted/owner
sed -i "s/^#PhysicalDesktopAccessNoAcceptance administrator,trusted,owner/PhysicalDesktopAccessNoAcceptance administrator,trusted,owner/" server.cfg

# Allow all user types to accept connections (no popup)
sed -i "s/^#PhysicalDesktopAcceptUsers owner/PhysicalDesktopAcceptUsers all/" server.cfg

echo "DONE"
```

Then run:
```bash
echo "USER_PASSWORD" | sudo -S bash /tmp/nm_config.sh
```

Verify:
```bash
grep -n "^EnableUPnP\|^PhysicalDesktopAccess\|^PhysicalDesktopMode\|^PhysicalDesktopAccessNoAcceptance\|^PhysicalDesktopAcceptUsers" /usr/NX/etc/server.cfg
```

### 5. Restart NoMachine server

```bash
sudo -S /usr/NX/bin/nxserver --restart
```

### 6. Add user to NoMachine

**PITFALL**: `nxserver --passwd` will fail with "NX password DB is disabled" if authorization uses system accounts (`AuthorizationPassword` not set). This means NoMachine uses the system PAM authentication - the user just enters their OS username/password, no separate NX password needed.

```bash
echo "USER_PASSWORD" | sudo -S /usr/NX/bin/nxserver --useradd <username>
```

### 7. Verify everything

```bash
/usr/NX/bin/nxserver --status
systemctl list-unit-files | grep nx
ss -tlnp | grep 4000
```

Expected: nxserver, nxnode, nxd all enabled. Port 4000 listening on 0.0.0.0.

## Connection Info

- Port: 4000
- Protocol: NX (encrypted)
- Auth: System username/password
- Desktop: Connect to running physical display

## Auto-Start Configuration (Ensures Persistence After Reboot)

NoMachine installs as a systemd service by default. To ensure it starts automatically after reboot or power outage:

```bash
# Check if nxserver service is enabled (will start on boot)
systemctl is-enabled nxserver.service

# If not enabled, enable it:
echo "USER_PASSWORD" | sudo -S systemctl enable nxserver.service

# Verify it's active and enabled:
systemctl status nxserver.service
# Should show: loaded active running and enabled
```

## Key Pitfalls Summary

1. **Download redirects**: NoMachine CDN requires browser cookies. Use `web9001.nomachine.com` CDN URLs or extract links via browser.
2. **No PTY for sudo**: Must pipe password via `echo \\\"pass\\\" | sudo -S`.
3. **Script file for config**: Long inline bash commands via sudo-heredoc time out. Write a .sh file first.
4. **System auth**: If `AuthorizationPassword` is not enabled in server.cfg, NoMachine uses system PAM. No separate NX password DB. Just use OS credentials.
5. **Frozen sessions**: If the remote desktop appears frozen but the machine is responsive locally:
   - Check for stuck `nxnode.bin` processes: `ps aux | grep nxnode`
   - Kill the stuck node process tied to your session ID (look for `-H <session_id>`): `sudo kill -9 <PID>`
   - Restart services: `sudo /usr/NX/bin/nxserver --restart`
   - Verify ports: `ss -tlnp | grep :4000`
   - Reconnect your NoMachine client for a fresh session.
6. **Service not persisting**: If NoMachine doesn't start after reboot, verify the service is enabled with `systemctl is-enabled nxserver.service` and enable it if needed.
