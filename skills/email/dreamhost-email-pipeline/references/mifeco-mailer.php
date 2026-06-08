<?php
/**
 * Plugin Name: MIFECO Mailer
 * Description: Email sending endpoint for MIFECO content command center.
 * Creates REST endpoint at /wp-json/mifeco/v1/send-email
 * Requires subject to contain [SaaS], [Books], or [Consulting] identifier.
 * CAN-SPAM compliant: physical address, List-Unsubscribe header, suppression list.
 * Uses shared Gmail account MIFECOinc@gmail.com for all sending.
 * Version: 1.2.0
 * Author: MIFECO
 */

if (!defined('ABSPATH')) exit;

class MIFECO_Mailer {
    private $secret_key = 'JY2pcWpfu1*JeubsVBpm';

    // Shared Gmail account — the ONLY email account available on DreamHost
    // Used by all applications. DO NOT change password without coordinating.
    private $from_email = 'MIFECOinc@gmail.com';
    private $from_name = 'MIFECO';

    // CAN-SPAM physical postal address
    private $physical_address = '147 Bathclub Cir, N. Redington Beach, FL 33708';

    // Abuse contact — shared Gmail account. Recipients reply with "ABUSE" in subject line.
    private $abuse_email = 'MIFECOinc@gmail.com';
    private $abuse_subject_keyword = 'ABUSE';

    // Suppression list file path (relative to WP_CONTENT_DIR)
    private $suppression_file = '/mifeco-suppression-list.txt';

    // Subject tag for shared-account identification
    private $subject_tag = '[MIFECO]';

    public function __construct() {
        add_action('rest_api_init', [$this, 'register_routes']);
    }

    public function register_routes() {
        register_rest_route('mifeco/v1', '/send-email', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_send_email'],
            'permission_callback' => [$this, 'verify_request'],
        ]);
        register_rest_route('mifeco/v1', '/unsubscribe', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_unsubscribe'],
            'permission_callback' => '__return_true',
        ]);
        register_rest_route('mifeco/v1', '/suppress', [
            'methods' => 'POST',
            'callback' => [$this, 'handle_suppress_check'],
            'permission_callback' => [$this, 'verify_request'],
        ]);
    }

    public function verify_request($request) {
        return $request->get_param('secret') === $this->secret_key;
    }

    /**
     * Check if an email address is on the suppression list.
     */
    private function is_suppressed($email) {
        $file = WP_CONTENT_DIR . $this->suppression_file;
        if (!file_exists($file)) return false;
        $list = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if ($list === false) return false;
        $normalized = strtolower(trim($email));
        foreach ($list as $entry) {
            if (strtolower(trim($entry)) === $normalized) return true;
        }
        return false;
    }

    /**
     * Add an address to the suppression list.
     */
    private function add_suppression($email) {
        $file = WP_CONTENT_DIR . $this->suppression_file;
        $dir = dirname($file);
        if (!is_dir($dir)) wp_mkdir_p($dir);
        file_put_contents($file, strtolower(trim($email)) . "\n", FILE_APPEND | LOCK_EX);
    }

    /**
     * Handle unsubscribe request from email link.
     * POST /wp-json/mifeco/v1/unsubscribe
     * Body: { "email": "user@example.com" }
     */
    public function handle_unsubscribe($request) {
        $email = sanitize_email($request->get_param('email'));
        if (!$email || !is_email($email)) {
            return new WP_REST_Response(['success' => false, 'error' => 'Valid email required'], 400);
        }
        if ($this->is_suppressed($email)) {
            return new WP_REST_Response(['success' => true, 'message' => 'Already unsubscribed'], 200);
        }
        $this->add_suppression($email);
        if (function_exists('error_log')) {
            error_log('[MIFECO Mailer] Unsubscribed: ' . $email);
        }
        return new WP_REST_Response([
            'success' => true,
            'message' => 'You have been unsubscribed. You will no longer receive emails from MIFECO.',
        ], 200);
    }

    /**
     * Check suppression status (for outbound pre-send check).
     * POST /wp-json/mifeco/v1/suppress
     * Body: { "secret": "...", "email": "user@example.com" }
     */
    public function handle_suppress_check($request) {
        $email = sanitize_email($request->get_param('email'));
        if (!$email) {
            return new WP_REST_Response(['success' => false, 'error' => 'Email required'], 400);
        }
        return new WP_REST_Response([
            'success' => true,
            'email' => $email,
            'suppressed' => $this->is_suppressed($email),
        ], 200);
    }

    /**
     * Build CAN-SPAM compliant email footer.
     */
    private function build_footer($unsubscribe_url = '') {
        $footer = "\n\n---\n";
        $footer .= "MIFECO — " . $this->physical_address . "\n";
        if ($unsubscribe_url) {
            $footer .= "To unsubscribe from future emails, click here: " . $unsubscribe_url . "\n";
        } else {
            $footer .= "To unsubscribe, reply with \"UNSUBSCRIBE\" in the subject or body.\n";
        }
        $footer .= "For abuse/violation reports, reply to " . $this->abuse_email . " with the word \"" . $this->abuse_subject_keyword . "\" in the subject line.\n";
        return $footer;
    }

    /**
     * Build List-Unsubscribe header value.
     */
    private function build_list_unsubscribe_header($email) {
        $unsubscribe_url = site_url('/wp-json/mifeco/v1/unsubscribe');
        return '<' . $unsubscribe_url . '>, <mailto:' . $this->abuse_email . '?subject=Unsubscribe+' . urlencode($email) . '>';
    }

    /**
     * Apply subject tag for shared-account identification.
     * All outbound emails through the shared MIFECOinc@gmail.com account
     * are tagged so replies can be identified and routed.
     */
    private function apply_subject_tag($subject) {
        if (strpos($subject, $this->subject_tag) !== 0) {
            $subject = $this->subject_tag . ' ' . $subject;
        }
        return $subject;
    }

    public function handle_send_email($request) {
        $email_data = $request->get_param('email');
        if (!$email_data || !isset($email_data['subject']) || !isset($email_data['body'])) {
            return new WP_REST_Response(['success' => false, 'error' => 'Missing required fields'], 400);
        }

        $subject = sanitize_text_field($email_data['subject']);
        $body = wp_kses_post($email_data['body']);
        $to = isset($email_data['to']) ? sanitize_email($email_data['to']) : $this->from_email;
        $pipeline = isset($email_data['pipeline']) ? sanitize_text_field($email_data['pipeline']) : '';

        // Check suppression list before sending
        if ($to && $this->is_suppressed($to)) {
            return new WP_REST_Response([
                'success' => false,
                'error' => 'Suppressed',
                'message' => 'Recipient has unsubscribed and is on the suppression list',
            ], 403);
        }

        // Ensure subject has pipeline identifier
        $identifiers = ['SaaS', 'Books', 'Consulting'];
        $found_identifier = '';
        foreach ($identifiers as $id) {
            if (stripos($subject, "[$id]") !== false) {
                $found_identifier = $id;
                break;
            }
        }
        if (!$found_identifier && $pipeline && in_array(ucfirst(strtolower($pipeline)), $identifiers)) {
            $found_identifier = ucfirst(strtolower($pipeline));
            $subject = '[' . $found_identifier . '] ' . $subject;
        }

        // Prepend AD: to commercial/sales pipeline subjects
        $commercial_pipelines = ['SaaS', 'Consulting'];
        if ($found_identifier && in_array($found_identifier, $commercial_pipelines)) {
            if (stripos($subject, 'AD:') !== 0) {
                $subject = 'AD: ' . $subject;
            }
        }

        // Apply shared-account subject tag
        $subject = $this->apply_subject_tag($subject);

        // Build CAN-SPAM footer
        $unsubscribe_url = site_url('/wp-json/mifeco/v1/unsubscribe');
        $footer = $this->build_footer($unsubscribe_url);
        $full_body = $body . $footer;

        // Build headers
        $headers = [
            'From: ' . $this->from_name . ' <' . $this->from_email . '>',
            'Reply-To: ' . $this->from_email,
            'Content-Type: text/html; charset=UTF-8',
            'X-MIFECO-Pipeline: ' . $found_identifier,
            'List-Unsubscribe: ' . $this->build_list_unsubscribe_header($to),
        ];

        $sent = wp_mail($to, $subject, nl2br($full_body), $headers);
        return new WP_REST_Response([
            'success' => $sent,
            'to' => $to,
            'subject' => $subject,
            'pipeline' => $found_identifier,
            'suppression_checked' => true,
        ], $sent ? 200 : 500);
    }
}

new MIFECO_Mailer();
