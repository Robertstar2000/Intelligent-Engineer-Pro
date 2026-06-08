#!/bin/bash
# Sync subscriber data from DreamHost to local machine
# This ensures subscriber data is included in Hermes backups

REMOTE_USER="dh_mwpxuu"
REMOTE_HOST="IAD1-SHARED-B8-42.DREAMHOST.COM"
REMOTE_PATH="/home/dh_mwpxuu/mifeco.com/books/api/subscribers.json"
LOCAL_PATH="/mnt/usb_4tb/books/books-section/api/subscribers.json"
SSH_PASS="Rm2214ri####"

# Sync using SSH
if command -v sshpass &>/dev/null; then
    sshpass -p "$SSH_PASS" rsync -avz "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}" "$LOCAL_PATH" --timeout=15
elif command -v python3 &>/dev/null; then
    python3 -c "
import paramiko, os
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('$REMOTE_HOST', username='$REMOTE_USER', password='$SSH_PASS', timeout=15)
sftp = client.open_sftp()
os.makedirs(os.path.dirname('$LOCAL_PATH'), exist_ok=True)
sftp.get('$REMOTE_PATH', '$LOCAL_PATH')
sftp.close()
client.close()
print('Subscriber DB synced: ' + str(os.path.getsize('$LOCAL_PATH')) + ' bytes')
"
fi

echo "Sync complete: $(date)"