# DreamHost WordPress Publishing — Infrastructure Reference

## Server Access
- Host: IAD1-SHARED-B8-42.DREAMHOST.COM
- User: dh_mwpxuu
- Password: Rm2214ri#### (from ~/.hermes/.env as DREAMHOST_PASSWORD)
- Remote path: /home/dh_mwpxuu/mifeco.com/

## WordPress
- DB: mifeco_com_1 / User: ak48bme / Pass: 7jpetxEL / Host: mysql.mifeco.com
- Table prefix: wp_gryu9c_
- SPA routing blocks WP REST API — must use PHP CLI directly

## Publishing
Use wp-publish-post.php with --content-file (not --content) for HTML.
Include both wp-load.php AND wp-admin/includes/taxonomy.php.

## SCP Pattern
1. mkdir -p remote dirs FIRST via SSH
2. SCP upload files
3. SSH run publish script
4. Cleanup temp files

## Gotchas
- SCP exitstatus may be None on success — check output strings
- Remote dirs must exist before SCP
- Add -o PubkeyAuthentication=no if key auth interferes

## Gemini Image Gen
- Model: gemini-2.5-flash-image via Google AI Studio
- Script: ~/.hermes/pipeline-engine/scripts/generate-blog-image.py
- Modes: cover-inspired (books), infographic (SaaS/consulting)
