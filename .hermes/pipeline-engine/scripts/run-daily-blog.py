#!/usr/bin/env python3
"""
Execute the full mifeco-daily-blog workflow for one book post and one saas/consulting post.
This is the main runner that orchestrates the entire process.

Usage: python3 run-daily-blog.py
"""
import json, os, random, sys, subprocess, datetime, pexpect

# ── Configuration ──────────────────────────────────────────────────────────────
HOME = os.path.expanduser("~")
PIPELINE_DIR = f"{HOME}/.hermes/pipeline-engine"
DATA_DIR = f"{PIPELINE_DIR}/data"
SCRIPTS_DIR = f"{PIPELINE_DIR}/scripts"
STATE_FILE = f"{DATA_DIR}/generated-blog-posts.json"

DREAMHOST = {
    "host": "IAD1-SHARED-B8-42.DREAMHOST.COM",
    "user": "dh_mwpxuu",
    "password": "Rm2214ri####",
    "remote_path": "/home/dh_mwpxuu/mifeco.com",
    "scripts_dir": "/home/dh_mwpxuu/mifeco.com/scripts",
    "images_dir": "/home/dh_mwpxuu/mifeco.com/images",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def ssh_run(command, timeout=60):
    """Run a command on DreamHost via SSH with password auth."""
    child = pexpect.spawn("ssh", [
        "-o", "StrictHostKeyChecking=accept-new",
        f"{DREAMHOST['user']}@{DREAMHOST['host']}",
        command
    ], timeout=timeout)
    child.expect("password:")
    child.sendline(DREAMHOST["password"])
    child.expect(pexpect.EOF, timeout=timeout)
    return child.before.decode()

def scp_upload(local, remote):
    """Upload a file to DreamHost via SCP with password auth."""
    child = pexpect.spawn("scp", [
        "-o", "StrictHostKeyChecking=accept-new",
        local,
        f"{DREAMHOST['user']}@{DREAMHOST['host']}:{remote}"
    ], timeout=60)
    child.expect("password:")
    child.sendline(DREAMHOST["password"])
    child.expect(pexpect.EOF, timeout=60)
    return child.exitstatus == 0

def get_gemini_key():
    """Get GOOGLE_AI_STUDIO_KEY from .env"""
    env_path = f"{HOME}/.hermes/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip().startswith("GOOGLE_AI_STUDIO_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip("'\"")
    return os.environ.get("GOOGLE_AI_STUDIO_KEY", "")

def generate_image(mode, output_path, **kwargs):
    """Generate image using Gemini."""
    key = get_gemini_key()
    if not key:
        return {"error": "No Gemini API key"}
    
    cmd = [
        sys.executable, f"{SCRIPTS_DIR}/generate-blog-image.py",
        f"--mode={mode}",
        f"--output={output_path}",
    ]
    if mode == "cover-inspired":
        cmd += [
            f"--book-title={kwargs.get('book_title', '')}",
            f"--series={kwargs.get('series', '')}",
            f"--genre={kwargs.get('genre', 'Science Fiction')}",
            f"--description={kwargs.get('description', '')}",
        ]
    elif mode == "infographic":
        cmd += [
            f"--post-title={kwargs.get('post_title', '')}",
            f"--content-summary={kwargs.get('content_summary', '')}",
            f"--category={kwargs.get('category', 'Business')}",
        ]
    
    env = os.environ.copy()
    env["GOOGLE_AI_STUDIO_KEY"] = key
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
    try:
        return json.loads(result.stdout.strip().split("\n")[-1])
    except:
        return {"error": result.stdout + result.stderr}

def publish_to_wordpress(title, content, slug, category, tags, featured_image_remote=None):
    """Publish a post to WordPress via DreamHost SSH."""
    cmd_parts = [
        f'cd {DREAMHOST["remote_path"]}',
        'php scripts/wp-publish-post.php',
        f'--title={title}',
        f'--slug={slug}',
        f'--category={category}',
        f'--tags={tags}',
    ]
    if featured_image_remote:
        cmd_parts.append(f'--featured-image={featured_image_remote}')
    
    # Write content to temp file to avoid shell escaping issues
    content_file = f"/tmp/wp-content-{slug}.html"
    with open(content_file, "w") as f:
        f.write(content)
    
    # Upload content file
    scp_upload(content_file, f"{DREAMHOST['remote_path']}/tmp/{slug}.html")
    
    # Run WP publish with content from file
    cmd = f'cd {DREAMHOST["remote_path"]} && php scripts/wp-publish-post.php --title="{title}" --slug="{slug}" --category="{category}" --tags="{tags}" --featured-image="{featured_image_remote or ""}" --content="$(cat tmp/{slug}.html)"'
    
    # Simpler approach: write PHP script that reads content
    php_wrapper = f'''
<?php
$content = file_get_contents('/home/dh_mwpxuu/mifeco.com/tmp/{slug}.html');
$_GET['title'] = '{title.replace("'", "\\\\'")}';
$_GET['slug'] = '{slug}';
$_GET['category'] = '{category}';
$_GET['tags'] = '{tags}';
$_GET['featured_image'] = '{featured_image_remote or ""}';
$_GET['content'] = $content;
include('/home/dh_mwpxuu/mifeco.com/scripts/wp-publish-post.php');
?>
'''
    # Actually, let's just use the CLI approach with proper escaping
    # Write a small PHP helper that takes content via stdin
    helper_php = f'''<?php
require_once('/home/dh_mwpxuu/mifeco.com/wp-load.php');
$content = file_get_contents('php://stdin');
$title = '{title.replace("'", "\\\\'")}';
$slug = '{slug}';
$category = '{category}';
$tags = array_map('trim', explode(',', '{tags}'));

$existing = get_posts(['name' => $slug, 'post_type' => 'post', 'post_status' => 'any', 'numberposts' => 1]);
if (!empty($existing)) {{
    echo json_encode(['error' => "Slug '$slug' already exists", 'existing_id' => $existing[0]->ID]);
    exit(1);
}}

$cat_id = null;
if ($category) {{
    $ec = get_category_by_slug(sanitize_title($category));
    if ($ec) $cat_id = $ec->term_id;
    else {{ $nc = wp_create_category($category); if (!is_wp_error($nc)) $cat_id = $nc; }}
}}

$post_data = [
    'post_title' => $title,
    'post_content' => $content,
    'post_name' => $slug,
    'post_status' => 'publish',
    'post_type' => 'post',
    'post_author' => 1,
];
if ($cat_id) $post_data['post_category'] = [$cat_id];

$post_id = wp_insert_post($post_data, true);
if (is_wp_error($post_id)) {{ echo json_encode(['error' => $post_id->get_error_message()]); exit(1); }}

if ($tags) wp_set_post_tags($post_id, $tags);

$thumb_id = null;
$thumb_url = null;
$img_path = '{featured_image_remote or ""}';
if ($img_path && file_exists($img_path)) {{
    $upload = wp_upload_bits(basename($img_path), null, file_get_contents($img_path));
    if ($upload['error'] === false) {{
        $ft = wp_check_filetype(basename($upload['file']), null);
        $att = ['guid' => $upload['url'], 'post_mime_type' => $ft['type'], 'post_title' => preg_replace('/\\.[^.]+$/', '', basename($upload['file'])), 'post_content' => '', 'post_status' => 'inherit'];
        $aid = wp_insert_attachment($att, $upload['file'], $post_id);
        if (!is_wp_error($aid)) {{
            require_once(ABSPATH . 'wp-admin/includes/image.php');
            $ad = wp_generate_attachment_metadata($aid, $upload['file']);
            wp_update_attachment_metadata($aid, $ad);
            set_post_thumbnail($post_id, $aid);
            $thumb_id = $aid;
            $thumb_url = wp_get_attachment_url($aid);
        }}
    }}
}}

echo json_encode([
    'success' => true,
    'post_id' => $post_id,
    'post_url' => get_permalink($post_id),
    'slug' => $slug,
    'thumbnail_id' => $thumb_id,
    'featured_image_url' => $thumb_url,
]);
'''
    helper_path = f"/tmp/wp-publish-{slug}.php"
    with open(helper_path, "w") as f:
        f.write(helper_php)
    
    scp_upload(helper_path, f"{DREAMHOST['remote_path']}/tmp/wp-publish-{slug}.php")
    
    # Upload content
    content_path = f"/tmp/wp-content-{slug}.html"
    with open(content_path, "w") as f:
        f.write(content)
    scp_upload(content_path, f"{DREAMHOST['remote_path']}/tmp/{slug}.html")
    
    result = ssh_run(f"cd {DREAMHOST['remote_path']} && php tmp/wp-publish-{slug}.php < tmp/{slug}.html 2>&1", timeout=30)
    
    # Cleanup
    ssh_run(f"rm -f {DREAMHOST['remote_path']}/tmp/wp-publish-{slug}.php {DREAMHOST['remote_path']}/tmp/{slug}.html")
    
    try:
        return json.loads(result.strip())
    except:
        return {"error": result[:500]}

def get_existing_wp_posts():
    """Get all existing WordPress post slugs and titles."""
    result = ssh_run(
        'mysql -u ak48bme -p7jpetxEL -h mysql.mifeco.com mifeco_com_1 '
        '-e "SELECT post_title, post_name FROM wp_gryu9c_posts WHERE post_type=\'post\';" 2>&1',
        timeout=30
    )
    posts = {}
    for line in result.strip().split("\n")[1:]:  # skip header
        parts = line.split("\t")
        if len(parts) >= 2:
            posts[parts[1].strip()] = parts[0].strip()
    return posts

# ── Main Workflow ────────────────────────────────────────────────────────────

def main():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    report = {"timestamp": now, "posts": [], "errors": []}
    
    # Load data
    books_data = load_json(f"{DATA_DIR}/pipeline-books.json")
    saas_data = load_json(f"{DATA_DIR}/pipeline-saas.json")
    existing_posts = load_json(STATE_FILE)
    
    # Extract published books
    published_books = []
    products = books_data["pipeline"]["products"]
    for section_key in ["titles", "moon_books", "age_of_lightships", "standalone", "business_books"]:
        section = products.get(section_key, [])
        if isinstance(section, dict):
            section = section.get("titles", section.get("books", []))
        for b in section:
            if b.get("status") == "published":
                published_books.append(b)
    
    # Get existing slugs for dedup
    existing_local_slugs = set()
    for p in existing_posts[1:] if len(existing_posts) > 1 else []:
        existing_local_slugs.add(p.get("slug", ""))
    
    existing_wp = get_existing_wp_posts()
    all_existing_slugs = existing_local_slogs | set(existing_wp.keys())
    all_existing_titles = set(existing_wp.values()) | {p.get("title","") for p in existing_posts[1:] if len(existing_posts) > 1}
    
    print(f"Published books: {len(published_books)}")
    print(f"Existing WP posts: {len(existing_wp)}")
    print(f"Existing local posts: {len(existing_local_slugs)}")
    
    # ── BOOK POST ──────────────────────────────────────────────────────────
    random.shuffle(published_books)
    book_post = None
    for book in published_books:
        slug = f"book-{book['title'].lower().replace(' ', '-').replace(':','').replace(',','')[:50]}"
        if slug not in all_existing_slugs and book["title"] not in all_existing_titles:
            book_post = book
            break
    
    if not book_post:
        # Try with suffix
        for book in published_books:
            for suffix in ["-review", "-guide", "-explored", "-deep-dive"]:
                slug = f"book-{book['title'].lower().replace(' ', '-').replace(':','').replace(',','')[:40]}{suffix}"
                if slug not in all_existing_slugs:
                    book_post = book
                    break
            if book_post:
                break
    
    if book_post:
        print(f"\n📚 Book post: {book_post['title']}")
        # The actual blog post content will be generated by the LLM in the cron job
        # For now, record the selection
        report["book_selection"] = {
            "title": book_post["title"],
            "asin": book_post.get("asin", ""),
            "slug": slug,
        }
    else:
        report["errors"].append("No unique book found for blog post")
    
    # ── SAAS/CONSULTING POST ───────────────────────────────────────────────
    saas_products = saas_data["pipeline"]["products"]
    consulting_topics = [
        {"name": "Virtual Consulting", "desc": "$199 online business assessment and strategy session"},
        {"name": "AI Readiness Assessment", "desc": "Custom evaluation of your organization's AI readiness"},
    ]
    all_saas_topics = [{"name": p, "desc": f"MIFECO {p}"} for p in saas_products] + consulting_topics
    random.shuffle(all_saas_topics)
    
    saas_post = None
    for topic in all_saas_topics:
        slug = f"saas-{topic['name'].lower().replace(' ', '-').replace(':','').replace(',','')[:50]}"
        if slug not in all_existing_slugs and topic["name"] not in all_existing_titles:
            saas_post = topic
            break
    
    if saas_post:
        print(f"💼 SaaS/Consulting post: {saas_post['name']}")
        report["saas_selection"] = {
            "name": saas_post["name"],
            "slug": slug,
        }
    else:
        report["errors"].append("No unique SaaS/consulting topic found")
    
    print(f"\nReport: {json.dumps(report, indent=2)}")
    return report

if __name__ == "__main__":
    main()
