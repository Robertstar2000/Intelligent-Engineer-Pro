<?php
/**
 * Plugin Name: MIFECO Outreach Dashboard
 * Description: Adds the Outreach Engine dashboard to the WordPress admin panel
 * Version: 1.0.0
 * Author: MIFECO
 */

// Prevent direct access
if (!defined('ABSPATH')) exit;

// Add admin menu
add_action('admin_menu', 'mifeco_outreach_add_admin_page');

function mifeco_outreach_add_admin_page() {
    add_menu_page(
        'Outreach Dashboard',      // Page title
        '📤 Outreach',             // Menu title
        'manage_options',          // Capability
        'mifeco-outreach',         // Menu slug
        'mifeco_outreach_render_page', // Callback
        'dashicons-email-alt',     // Icon
        25                         // Position (above Settings)
    );
}

function mifeco_outreach_render_page() {
    // The local dashboard URL
    $dashboard_url = 'https://192.168.1.77:5543/outreach-dashboard.html';
    ?>
    <div class="wrap mifeco-outreach-wrap">
        <style>
            .mifeco-outreach-wrap { margin: 0; padding: 0; }
            .mifeco-outreach-wrap iframe {
                width: 100%;
                height: calc(100vh - 32px);
                border: none;
                background: #0f172a;
            }
            .mifeco-outreach-notice {
                background: #1e293b;
                border: 1px solid #334155;
                border-left: 4px solid #00ffcc;
                padding: 12px 16px;
                margin: 16px 0;
                border-radius: 4px;
                color: #e2e8f0;
                font-size: 13px;
            }
            .mifeco-outreach-notice code {
                background: #334155;
                color: #00ffcc;
                padding: 2px 6px;
                border-radius: 3px;
            }
            #wpcontent { padding-left: 0; }
            #wpbody-content { padding-bottom: 0; }
            #wpfooter { display: none; }
        </style>
        <div class="mifeco-outreach-notice">
            🔗 Connected to local Outreach Engine at <code><?php echo esc_html($dashboard_url); ?></code>
            &middot; <strong>Test mode</strong> uses mock inbox &middot; <strong>Production mode</strong> sends live emails
        </div>
        <iframe src="<?php echo esc_url($dashboard_url); ?>" 
                title="MIFECO Outreach Dashboard"
                allow="clipboard-read; clipboard-write"
                loading="lazy">
        </iframe>
    </div>
    <?php
}
