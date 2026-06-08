#!/usr/bin/env python3
"""Test suite for content-generator.py"""
import sys
import os
import json
import tempfile
import unittest

# Add the script's dir to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# We'll test by running the script as subprocess
import subprocess

class TestContentGenerator(unittest.TestCase):
    """Test the content generation engine."""
    
    def setUp(self):
        self.script_path = os.path.join(SCRIPT_DIR, "content-generator.py")
        self.data_dir = os.path.join(os.path.dirname(SCRIPT_DIR), "data")
        self.seq_dir = os.path.join(os.path.dirname(SCRIPT_DIR), "sequences")
    
    def test_report_mode(self):
        """Test --report mode runs without errors."""
        result = subprocess.run(
            [sys.executable, self.script_path, "--report"],
            capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        print("STDOUT:", result.stdout[:500])
        print("STDERR:", result.stderr[:500])
        self.assertEqual(result.returncode, 0)
        self.assertIn("GENERATION REPORT", result.stdout)
    
    def test_social_only(self):
        """Test --social only mode."""
        result = subprocess.run(
            [sys.executable, self.script_path, "--social", "only"],
            capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        self.assertEqual(result.returncode, 0)
        # Check output file exists
        social_output = os.path.join(self.data_dir, "generated-social-content.json")
        self.assertTrue(os.path.exists(social_output))
        with open(social_output) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 1)  # header + posts
    
    def test_blog_only(self):
        """Test --blog only mode."""
        result = subprocess.run(
            [sys.executable, self.script_path, "--blog", "only"],
            capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        self.assertEqual(result.returncode, 0)
        blog_output = os.path.join(self.data_dir, "generated-blog-posts.json")
        self.assertTrue(os.path.exists(blog_output))
        with open(blog_output) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 1)
    
    def test_full_generation(self):
        """Test full generation (social + blog)."""
        result = subprocess.run(
            [sys.executable, self.script_path],
            capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Generation Complete", result.stdout)
    
    def test_pipeline_filter_books(self):
        """Test --pipeline books filter."""
        result = subprocess.run(
            [sys.executable, self.script_path, "--pipeline", "books", "--social", "only"],
            capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        self.assertEqual(result.returncode, 0)
        social_output = os.path.join(self.data_dir, "generated-social-content.json")
        with open(social_output) as f:
            data = json.load(f)
        # First item is header
        posts = [p for p in data[1:] if isinstance(p, dict) and "platform" in p]
        for post in posts:
            self.assertIn("linked_lead_id", post)
    
    def test_output_schema(self):
        """Verify generated content follows required schema."""
        # Generate first
        subprocess.run(
            [sys.executable, self.script_path, "--social", "only"],
            capture_output=True, cwd=os.path.dirname(SCRIPT_DIR)
        )
        
        with open(os.path.join(self.data_dir, "generated-social-content.json")) as f:
            data = json.load(f)
        
        # Check header
        self.assertIn("generated_at", data[0])
        self.assertIn("stats", data[0])
        
        # Check posts
        posts = [p for p in data[1:] if isinstance(p, dict) and "platform" in p]
        for post in posts:
            self.assertIn("platform", post)
            self.assertIn(post["platform"], ["linkedin", "x"])
            self.assertIn("target_audience", post)
            self.assertIn("copy", post)
            self.assertIn("hashtags", post)
            self.assertIn("graphic_prompt", post)
            self.assertIn("linked_lead_id", post)
            self.assertIn("generated_at", post)
            
            # Type checks
            self.assertIsInstance(post["copy"], str)
            self.assertIsInstance(post["hashtags"], list)
            self.assertIsInstance(post["graphic_prompt"], str)
            
            # X posts should be <= 280 chars
            if post["platform"] == "x":
                self.assertLessEqual(len(post["copy"]), 280,
                    f"X post too long: {len(post['copy'])} chars")

if __name__ == "__main__":
    unittest.main(verbosity=2)
