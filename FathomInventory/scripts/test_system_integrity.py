#!/usr/bin/env python3
"""
Fast-running system integrity tests to catch breakage from file moves and reorganization.
Focuses on import paths, file existence, permissions, and configuration integrity.
"""

import os
import sys
import subprocess
import sqlite3
import json
import importlib.util
from pathlib import Path

class SystemIntegrityTester:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
    def log_error(self, test_name, message):
        self.errors.append(f"❌ {test_name}: {message}")
        
    def log_warning(self, test_name, message):
        self.warnings.append(f"⚠️  {test_name}: {message}")
        
    def log_success(self, test_name, message="OK"):
        print(f"✅ {test_name}: {message}")

    def test_critical_files_exist(self):
        """Test that all critical files exist and are accessible."""
        critical_files = [
            'run_all.sh',
            'download_emails.py', 
            'run_daily_share.py',
            'share_fathom_call2.py',
            'fathom_cookies.json',
            'credentials.json',
            'token.json',
            'all_fathom_calls.tsv',
            'fathom_emails.db'
        ]
        
        for file_path in critical_files:
            full_path = self.script_dir / file_path
            if not full_path.exists():
                self.log_error("Critical Files", f"Missing: {file_path}")
            else:
                self.log_success("Critical Files", f"Found: {file_path}")

    def test_script_permissions(self):
        """Test that executable scripts have proper permissions."""
        executable_scripts = ['run_all.sh', 'refresh_fathom_auth.sh']
        
        for script in executable_scripts:
            script_path = self.script_dir / script
            if script_path.exists():
                if os.access(script_path, os.X_OK):
                    self.log_success("Permissions", f"{script} is executable")
                else:
                    self.log_error("Permissions", f"{script} is not executable")
            else:
                self.log_error("Permissions", f"{script} not found")

    def test_bash_syntax(self):
        """Test bash scripts for syntax errors."""
        bash_scripts = ['run_all.sh', 'refresh_fathom_auth.sh']
        
        for script in bash_scripts:
            script_path = self.script_dir / script
            if script_path.exists():
                try:
                    result = subprocess.run(['bash', '-n', str(script_path)], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_success("Bash Syntax", f"{script} syntax OK")
                    else:
                        self.log_error("Bash Syntax", f"{script}: {result.stderr.strip()}")
                except Exception as e:
                    self.log_error("Bash Syntax", f"{script}: {e}")

    def test_python_imports(self):
        """Test that Python scripts can import their dependencies."""
        python_scripts = {
            'download_emails.py': ['email_conversion.fathom_email_2_md'],
            'run_daily_share.py': ['share_fathom_call2'],
            'analysis/batch_analyze_calls.py': [],
            'analysis/ask_fathom_ai.py': []
        }
        
        # Add current directory to Python path for testing
        original_path = sys.path.copy()
        sys.path.insert(0, str(self.script_dir))
        
        try:
            for script, expected_imports in python_scripts.items():
                script_path = self.script_dir / script
                if script_path.exists():
                    # Test script syntax
                    try:
                        with open(script_path, 'r') as f:
                            compile(f.read(), script_path, 'exec')
                        self.log_success("Python Syntax", f"{script} compiles OK")
                    except SyntaxError as e:
                        self.log_error("Python Syntax", f"{script}: {e}")
                    
                    # Test expected imports
                    for import_module in expected_imports:
                        try:
                            importlib.import_module(import_module)
                            self.log_success("Python Imports", f"{script} can import {import_module}")
                        except ImportError as e:
                            self.log_error("Python Imports", f"{script} cannot import {import_module}: {e}")
        finally:
            sys.path = original_path

    def test_database_connectivity(self):
        """Test that database file is accessible and has expected structure."""
        db_path = self.script_dir / 'fathom_emails.db'
        
        if not db_path.exists():
            self.log_error("Database", "fathom_emails.db not found")
            return
            
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check if emails table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails'")
            if cursor.fetchone():
                self.log_success("Database", "emails table exists")
                
                # Check table structure
                cursor.execute("PRAGMA table_info(emails)")
                columns = [row[1] for row in cursor.fetchall()]
                expected_columns = ['message_id', 'thread_id', 'date', 'subject', 'body_html', 'body_md']
                
                missing_columns = set(expected_columns) - set(columns)
                if missing_columns:
                    self.log_error("Database", f"Missing columns: {missing_columns}")
                else:
                    self.log_success("Database", "Table structure OK")
            else:
                self.log_error("Database", "emails table not found")
                
            conn.close()
            
        except sqlite3.Error as e:
            self.log_error("Database", f"SQLite error: {e}")

    def test_json_files_validity(self):
        """Test that JSON configuration files are valid."""
        json_files = ['fathom_cookies.json', 'credentials.json', 'token.json']
        
        for json_file in json_files:
            file_path = self.script_dir / json_file
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        json.load(f)
                    self.log_success("JSON Validity", f"{json_file} is valid JSON")
                except json.JSONDecodeError as e:
                    self.log_error("JSON Validity", f"{json_file}: {e}")
            else:
                self.log_warning("JSON Validity", f"{json_file} not found")

    def test_virtual_environment_path(self):
        """Test that virtual environment path is accessible."""
        venv_path = self.script_dir.parent / 'ERA_Admin_venv' / 'bin' / 'activate'
        
        if venv_path.exists():
            self.log_success("Virtual Environment", f"Found at {venv_path}")
        else:
            self.log_error("Virtual Environment", f"Not found at {venv_path}")

    def test_launchd_configuration(self):
        """Test launchd job configuration and status."""
        plist_path = self.script_dir / 'com.fathominventory.run.plist'
        
        if plist_path.exists():
            self.log_success("launchd Config", "plist file exists")
            
            # Check if job is loaded
            try:
                result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
                if 'com.era.admin.fathom' in result.stdout:
                    self.log_success("launchd Status", "Job is loaded")
                else:
                    self.log_warning("launchd Status", "Job not found in launchctl list")
            except Exception as e:
                self.log_warning("launchd Status", f"Could not check status: {e}")
        else:
            self.log_error("launchd Config", "plist file not found")

    def test_dual_output_functionality(self):
        """Test that log_and_echo function works in run_all.sh."""
        script_path = self.script_dir / 'run_all.sh'
        
        if script_path.exists():
            try:
                with open(script_path, 'r') as f:
                    content = f.read()
                
                if 'log_and_echo()' in content and 'tee -a' in content:
                    self.log_success("Dual Output", "log_and_echo function found")
                else:
                    self.log_error("Dual Output", "log_and_echo function not found or incomplete")
                    
            except Exception as e:
                self.log_error("Dual Output", f"Could not read run_all.sh: {e}")

    def test_authentication_health(self):
        """Test authentication system health."""
        health_script = self.script_dir / 'check_auth_health.py'
        
        if health_script.exists():
            try:
                # Run the health check script
                result = subprocess.run([sys.executable, str(health_script)], 
                                      capture_output=True, text=True, 
                                      cwd=str(self.script_dir))
                
                if result.returncode == 0:
                    self.log_success("Auth Health", "Authentication system healthy")
                else:
                    self.log_warning("Auth Health", "Authentication needs attention")
                    
            except Exception as e:
                self.log_error("Auth Health", f"Could not run health check: {e}")
        else:
            self.log_error("Auth Health", "check_auth_health.py not found")

    def run_all_tests(self):
        """Run all integrity tests."""
        print("🔍 SYSTEM INTEGRITY TEST SUITE")
        print("=" * 50)
        print("Testing for breakage from file moves and reorganization...")
        print("")
        
        # Run all tests
        self.test_critical_files_exist()
        self.test_script_permissions()
        self.test_bash_syntax()
        self.test_python_imports()
        self.test_database_connectivity()
        self.test_json_files_validity()
        self.test_virtual_environment_path()
        self.test_launchd_configuration()
        self.test_dual_output_functionality()
        self.test_authentication_health()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        if not self.errors and not self.warnings:
            print("🎉 ALL TESTS PASSED - System integrity verified!")
            return 0
        elif not self.errors:
            print("✅ No critical errors found (warnings can be addressed)")
            return 0
        else:
            print("❌ Critical errors found - system may be broken")
            return 1

if __name__ == "__main__":
    tester = SystemIntegrityTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
