#!/usr/bin/env python3
"""
Security policy for MCP Python servers
Restricts dangerous operations and monitors system calls
"""

import os
import sys
import subprocess
import socket
import tempfile
from pathlib import Path

# Restricted operations
BLOCKED_MODULES = {
    'subprocess', 'os.system', 'eval', 'exec', 
    'compile', '__import__', 'open'
}

ALLOWED_NETWORK_HOSTS = {
    'localhost', '127.0.0.1', '::1'
}

ALLOWED_FILE_PATHS = {
    str(Path.home() / 'GithubProjects'),
    tempfile.gettempdir()
}

class SecurityMonitor:
    def __init__(self):
        self.violations = []
    
    def check_network_access(self, host, port):
        """Monitor network connections"""
        if host not in ALLOWED_NETWORK_HOSTS:
            violation = f"BLOCKED: Network access to {host}:{port}"
            self.violations.append(violation)
            print(f"🚨 SECURITY: {violation}")
            return False
        return True
    
    def check_file_access(self, filepath):
        """Monitor file system access"""
        path = Path(filepath).resolve()
        allowed = any(str(path).startswith(allowed_path) 
                     for allowed_path in ALLOWED_FILE_PATHS)
        
        if not allowed:
            violation = f"BLOCKED: File access to {filepath}"
            self.violations.append(violation)
            print(f"🚨 SECURITY: {violation}")
            return False
        return True
    
    def check_subprocess(self, command):
        """Monitor subprocess execution"""
        dangerous_commands = ['curl', 'wget', 'nc', 'netcat', 'ssh', 'scp']
        
        if any(cmd in str(command) for cmd in dangerous_commands):
            violation = f"BLOCKED: Dangerous subprocess: {command}"
            self.violations.append(violation)
            print(f"🚨 SECURITY: {violation}")
            return False
        return True

# Global security monitor
security_monitor = SecurityMonitor()

# Monkey patch dangerous functions
original_socket_connect = socket.socket.connect
def secure_socket_connect(self, address):
    host, port = address
    if security_monitor.check_network_access(host, port):
        return original_socket_connect(self, address)
    else:
        raise PermissionError(f"Network access blocked: {host}:{port}")

socket.socket.connect = secure_socket_connect

# Export security monitor for use in MCP servers
__all__ = ['security_monitor', 'SecurityMonitor']
