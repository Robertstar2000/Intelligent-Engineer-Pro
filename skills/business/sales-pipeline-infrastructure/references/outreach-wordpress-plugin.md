# MIFECO Outreach Dashboard — WordPress Admin Plugin

## File

`/home/bob/.hermes/pipeline-engine/mifeco-outreach-admin.php` (canonical source)
Deployed to: `/home/dh_mwpxuu/mifeco.com/wp-content/plugins/mifeco-outreach/mifeco-outreach-admin.php`

## Purpose

Adds an "📤 Outreach" menu item in the WordPress admin sidebar at `admin.php?page=mifeco-outreach`. The admin page contains an iframe pointing to `https://192.168.1.77:5543/outreach-dashboard.html`.

## Deployment

### Via SCP + SSH:
```bash
mkdir -p /tmp/mifeco-outreach
cp /home/bob/.hermes/pipeline-engine/mifeco-outreach-admin.php /tmp/mifeco-outreach/
cd /tmp && zip -r mifeco-outreach.zip mifeco-outreach/
scp /tmp/mifeco-outreach.zip dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/wp-content/plugins/

ssh dh_mwpxuu@iad1-shared-b8-42.dreamhost.com
cd /home/dh_mwpxuu/mifeco.com
unzip -o wp-content/plugins/mifeco-outreach.zip -d wp-content/plugins/
/usr/bin/wp plugin activate mifeco-outreach/mifeco-outreach-admin --path=/home/dh_mwpxuu/mifeco.com
```

### Key Access:
- **Host:** iad1-shared-b8-42.dreamhost.com
- **User:** dh_mwpxuu
- **Password:** Rm2214ri#### (4 # symbols, NOT %%%%)
- **WordPress path:** /home/dh_mwpxuu/mifeco.com
- **wp-cli:** /usr/bin/wp plugin activate --path=&lt;webroot&gt;
