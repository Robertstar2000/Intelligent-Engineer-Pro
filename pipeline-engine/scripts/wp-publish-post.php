#!/usr/bin/env php
<?php
/**
 * WordPress Blog Post Publisher — v2
 * 
 * Creates a blog post on mifeco.com WordPress via CLI.
 * Content is read from a file to avoid shell escaping issues.
 *
 * Usage:
 *   php wp-publish-post.php --title="Title" --content-file="/path/to/content.html" --slug="slug" --category="Cat" --tags="tag1,tag2" --featured-image="/path/to/image.jpg"
 *
 * All arguments are required except --featured-image and --tags.
 */

require_once('/home/dh_mwpxuu/mifeco.com/wp-load.php');
// Needed for wp_create_category()
require_once('/home/dh_mwpxuu/mifeco.com/wp-admin/includes/taxonomy.php');

$options = getopt('', [
    'title:', 'content-file:', 'slug:', 'category::', 'tags::', 'featured-image::', 'status::'
]);

$title = $options['title'] ?? '';
$content_file = $options['content-file'] ?? '';
$slug = $options['slug'] ?? sanitize_title($title);
$category = $options['category'] ?? '';
$tags = isset($options['tags']) ? array_map('trim', explode(',', $options['tags'])) : [];
$featured_image = $options['featured-image'] ?? '';
$status = $options['status'] ?? 'publish';

if (empty($title) || empty($content_file)) {
    echo json_encode(['error' => 'Title and content-file are required', 'usage' => 'wp-publish-post.php --title="..." --content-file="/path/to/file.html" [--slug="..."] [--category="..."] [--tags="..."] [--featured-image="/path"] [--status=publish]']);
    exit(1);
}

if (!file_exists($content_file)) {
    echo json_encode(['error' => "Content file not found: $content_file"]);
    exit(1);
}

$content = file_get_contents($content_file);
if (empty($content)) {
    echo json_encode(['error' => 'Content file is empty']);
    exit(1);
}

// Check for duplicate slug
$existing = get_posts(['name' => $slug, 'post_type' => 'post', 'post_status' => 'any', 'numberposts' => 1]);
if (!empty($existing)) {
    echo json_encode(['error' => "Post with slug '$slug' already exists (ID: {$existing[0]->ID})", 'existing_id' => $existing[0]->ID]);
    exit(1);
}

// Resolve or create category
$category_id = null;
if (!empty($category)) {
    $existing_cat = get_category_by_slug(sanitize_title($category));
    if ($existing_cat) {
        $category_id = $existing_cat->term_id;
    } else {
        $new_cat = wp_create_category($category);
        if (!is_wp_error($new_cat)) {
            $category_id = $new_cat;
        }
    }
}

// Build post data
$post_data = [
    'post_title'   => $title,
    'post_content' => $content,
    'post_name'    => $slug,
    'post_status'  => $status,
    'post_type'    => 'post',
    'post_author'  => 1, // admin
    'comment_status' => 'open',
];

if ($category_id) {
    $post_data['post_category'] = [$category_id];
}

// Create the post
$post_id = wp_insert_post($post_data, true);

if (is_wp_error($post_id)) {
    echo json_encode(['error' => $post_id->get_error_message()]);
    exit(1);
}

// Set tags
if (!empty($tags)) {
    wp_set_post_tags($post_id, $tags);
}

// Upload and set featured image
$thumbnail_id = null;
$thumbnail_url = null;
if (!empty($featured_image) && file_exists($featured_image)) {
    $upload = wp_upload_bits(basename($featured_image), null, file_get_contents($featured_image));
    if ($upload['error'] === false) {
        $filetype = wp_check_filetype(basename($upload['file']), null);
        $attachment = [
            'guid'           => $upload['url'],
            'post_mime_type' => $filetype['type'],
            'post_title'     => preg_replace('/\.[^.]+$/', '', basename($upload['file'])),
            'post_content'   => '',
            'post_status'    => 'inherit',
        ];
        $attach_id = wp_insert_attachment($attachment, $upload['file'], $post_id);
        if (!is_wp_error($attach_id)) {
            require_once(ABSPATH . 'wp-admin/includes/image.php');
            $attach_data = wp_generate_attachment_metadata($attach_id, $upload['file']);
            wp_update_attachment_metadata($attach_id, $attach_data);
            set_post_thumbnail($post_id, $attach_id);
            $thumbnail_id = $attach_id;
            $thumbnail_url = wp_get_attachment_url($attach_id);
        }
    }
}

// Return success
echo json_encode([
    'success' => true,
    'post_id' => $post_id,
    'post_url' => get_permalink($post_id),
    'slug' => $slug,
    'thumbnail_id' => $thumbnail_id,
    'featured_image_url' => $thumbnail_url,
    'category_id' => $category_id,
    'tags' => $tags,
], JSON_PRETTY_PRINT);
exit(0);
