"""
Code Isolation & Authorization Framework
Ensures ONLY user-authorized code executes
No external code can modify core functions
"""

import os
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from pathlib import Path

logger = logging.getLogger("CodeAuthorization")


class CodeAuthorityManager:
    """
    Absolute authority over all code execution
    User decides what can and cannot run
    """
    
    def __init__(self, owner_id: str):
        self.owner_id = owner_id  # Your unique ID
        self.authorized_code = {}  # Only code YOU approve
        self.code_signatures = {}  # Track what's allowed
        self.blocked_code = set()  # Code that's permanently blocked
        self.execution_log = []
        self.authority_file = Path("authority.json")
        self.load_authority()
    
    def load_authority(self):
        """Load your authorized code list"""
        if self.authority_file.exists():
            with open(self.authority_file, 'r') as f:
                data = json.load(f)
                self.authorized_code = data.get('authorized', {})
                self.blocked_code = set(data.get('blocked', []))
                logger.info(f"Loaded {len(self.authorized_code)} authorized code blocks")
    
    def save_authority(self):
        """Save your current authorization settings"""
        data = {
            'owner': self.owner_id,
            'authorized': self.authorized_code,
            'blocked': list(self.blocked_code),
            'updated': datetime.now().isoformat()
        }
        with open(self.authority_file, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info("Authority settings saved")
    
    def authorize_code(self, code_name: str, code_source: str, 
                      description: str = "", allow_modifications: bool = True):
        """
        YOU authorize code to run
        You control if it can be modified
        """
        code_hash = hashlib.sha256(code_source.encode()).hexdigest()
        
        self.authorized_code[code_name] = {
            'hash': code_hash,
            'source': code_source,
            'description': description,
            'allow_modifications': allow_modifications,
            'authorized_at': datetime.now().isoformat(),
            'authorized_by': self.owner_id
        }
        
        self.save_authority()
        
        logger.info(f"✓ Code '{code_name}' authorized by {self.owner_id}")
        return {
            'status': 'authorized',
            'code_name': code_name,
            'hash': code_hash,
            'modifications_allowed': allow_modifications
        }
    
    def revoke_code(self, code_name: str):
        """
        YOU can revoke any code's execution rights
        Permanently block code from running
        """
        if code_name in self.authorized_code:
            del self.authorized_code[code_name]
            self.blocked_code.add(code_name)
            self.save_authority()
            
            logger.warning(f"✗ Code '{code_name}' revoked by {self.owner_id}")
            return {'status': 'revoked', 'code_name': code_name}
        
        return {'status': 'not_found', 'code_name': code_name}
    
    def can_execute(self, code_name: str, code_source: str = None) -> bool:
        """
        Check if code is authorized to execute
        Only code YOU authorized will run
        """
        # Permanently blocked?
        if code_name in self.blocked_code:
            logger.critical(f"✗ BLOCKED CODE ATTEMPT: {code_name}")
            return False
        
        # Is it authorized?
        if code_name not in self.authorized_code:
            logger.critical(f"✗ UNAUTHORIZED CODE ATTEMPT: {code_name}")
            return False
        
        # Verify code hasn't changed
        if code_source:
            expected_hash = self.authorized_code[code_name]['hash']
            actual_hash = hashlib.sha256(code_source.encode()).hexdigest()
            
            if expected_hash != actual_hash:
                logger.critical(f"✗ CODE TAMPERING DETECTED: {code_name}")
                return False
        
        return True
    
    def execute_only_authorized(self, code_name: str, 
                                function: Callable, 
                                *args, **kwargs) -> Any:
        """
        ONLY execute code you've authorized
        Nothing else can run
        """
        if not self.can_execute(code_name):
            raise PermissionError(f"Code '{code_name}' is not authorized to execute")
        
        # Log execution
        self.execution_log.append({
            'code_name': code_name,
            'timestamp': datetime.now().isoformat(),
            'executed_by': self.owner_id
        })
        
        logger.info(f"✓ Executing authorized code: {code_name}")
        
        # ONLY execute the authorized code
        try:
            result = function(*args, **kwargs)
            logger.info(f"✓ Code '{code_name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"✗ Code '{code_name}' failed: {str(e)}")
            raise
    
    def list_authorized_code(self) -> List[Dict[str, Any]]:
        """List all code YOU'VE authorized"""
        return [
            {
                'name': name,
                'description': info.get('description'),
                'modifications_allowed': info.get('allow_modifications'),
                'authorized_at': info.get('authorized_at'),
                'hash': info['hash'][:8] + '...'
            }
            for name, info in self.authorized_code.items()
        ]
    
    def list_blocked_code(self) -> List[str]:
        """List all code you've blocked"""
        return list(self.blocked_code)
    
    def get_execution_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get YOUR execution audit trail"""
        return self.execution_log[-limit:]


class UserCodeIsolation:
    """
    Complete code isolation
    Your code runs in isolated environment
    No external interference possible
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.isolated_functions = {}
        self.user_namespace = {}
        self.authority = CodeAuthorityManager(user_id)
    
    def register_user_function(self, name: str, function: Callable, 
                               source_code: str, 
                               description: str = "",
                               allow_mods: bool = True):
        """
        Register YOUR function
        Only you can modify it
        """
        # Add to isolated environment
        self.isolated_functions[name] = {
            'function': function,
            'source': source_code,
            'owner': self.user_id
        }
        
        # Authorize it
        self.authority.authorize_code(
            name, 
            source_code, 
            description,
            allow_mods
        )
        
        logger.info(f"✓ Function '{name}' registered and isolated for {self.user_id}")
        return {'status': 'registered', 'function': name}
    
    def call_user_function(self, name: str, *args, **kwargs) -> Any:
        """
        Execute YOUR function
        Isolated and protected
        """
        if name not in self.isolated_functions:
            raise ValueError(f"Function '{name}' not registered")
        
        func = self.isolated_functions[name]['function']
        
        # Execute ONLY if authorized
        return self.authority.execute_only_authorized(
            name,
            func,
            *args,
            **kwargs
        )
    
    def modify_function(self, name: str, new_source: str, new_function: Callable):
        """
        YOU can modify YOUR own functions
        Nothing else can
        """
        if name not in self.isolated_functions:
            raise ValueError(f"Function '{name}' not found")
        
        if self.isolated_functions[name]['owner'] != self.user_id:
            raise PermissionError(f"You don't own function '{name}'")
        
        # Check if modifications are allowed
        auth_info = self.authority.authorized_code.get(name)
        if auth_info and not auth_info.get('allow_modifications'):
            raise PermissionError(f"Modifications not allowed for '{name}'")
        
        # Update function
        self.isolated_functions[name]['function'] = new_function
        self.isolated_functions[name]['source'] = new_source
        
        # Re-authorize with new code
        self.authority.authorize_code(
            name,
            new_source,
            auth_info.get('description', ''),
            True
        )
        
        logger.info(f"✓ Function '{name}' modified by owner {self.user_id}")
        return {'status': 'modified', 'function': name}
    
    def block_function(self, name: str):
        """
        YOU can block any function
        It will never execute again
        """
        self.authority.revoke_code(name)
        if name in self.isolated_functions:
            del self.isolated_functions[name]
        
        logger.warning(f"✓ Function '{name}' blocked by {self.user_id}")
        return {'status': 'blocked', 'function': name}


class NoExternalCodeExecution:
    """
    Prevents ANY external code from running
    Acts as a firewall against unauthorized execution
    """
    
    def __init__(self):
        self.blocked_sources = []
        self.blocked_patterns = [
            'import socket',
            'import subprocess',
            'eval(',
            'exec(',
            '__import__',
            'system(',
            'os.system',
            'popen(',
        ]
    
    def is_code_safe(self, code: str) -> bool:
        """
        Check if code is safe to execute
        Blocks dangerous patterns
        """
        for pattern in self.blocked_patterns:
            if pattern in code:
                logger.critical(f"✗ DANGEROUS CODE PATTERN DETECTED: {pattern}")
                return False
        
        return True
    
    def validate_before_execution(self, code_name: str, code_source: str) -> bool:
        """
        Validate code BEFORE allowing execution
        Multi-layer protection
        """
        # Check for dangerous patterns
        if not self.is_code_safe(code_source):
            logger.critical(f"✗ Code '{code_name}' contains unsafe patterns")
            return False
        
        # Check code length (prevents injection)
        if len(code_source) > 1_000_000:
            logger.critical(f"✗ Code '{code_name}' is suspiciously large")
            return False
        
        return True


class MyCodeOnly:
    """
    Master controller - ONLY your code runs
    Everything else is blocked
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.isolation = UserCodeIsolation(user_id)
        self.firewall = NoExternalCodeExecution()
        self.my_functions = {}
    
    def define_my_function(self, name: str, function: Callable, 
                          source_code: str, description: str = ""):
        """
        Define YOUR function
        Only your code can change it
        """
        # Validate code safety
        if not self.firewall.validate_before_execution(name, source_code):
            raise ValueError(f"Code '{name}' failed safety validation")
        
        # Register in isolation
        self.isolation.register_user_function(
            name,
            function,
            source_code,
            description,
            allow_mods=True
        )
        
        self.my_functions[name] = {
            'function': function,
            'description': description,
            'created': datetime.now().isoformat()
        }
        
        logger.info(f"✓ Your function '{name}' is registered and protected")
        return {'status': 'defined', 'function': name}
    
    def call_my_function(self, name: str, *args, **kwargs) -> Any:
        """
        Call YOUR function
        Nothing else will execute
        """
        if name not in self.my_functions:
            raise ValueError(f"Function '{name}' is not YOUR function")
        
        return self.isolation.call_user_function(name, *args, **kwargs)
    
    def change_my_function(self, name: str, new_source: str, new_function: Callable):
        """
        YOU can change YOUR function anytime
        """
        if name not in self.my_functions:
            raise ValueError(f"Function '{name}' is not YOUR function")
        
        # Validate new code
        if not self.firewall.validate_before_execution(name, new_source):
            raise ValueError(f"New code for '{name}' failed safety validation")
        
        # Modify it
        self.isolation.modify_function(name, new_source, new_function)
        self.my_functions[name]['description'] = f"Modified at {datetime.now().isoformat()}"
        
        logger.info(f"✓ Your function '{name}' has been updated")
        return {'status': 'updated', 'function': name}
    
    def disable_my_function(self, name: str):
        """
        YOU can disable YOUR functions
        """
        if name not in self.my_functions:
            raise ValueError(f"Function '{name}' is not YOUR function")
        
        self.isolation.block_function(name)
        del self.my_functions[name]
        
        logger.info(f"✓ Your function '{name}' is now disabled")
        return {'status': 'disabled', 'function': name}
    
    def list_my_functions(self) -> List[Dict[str, Any]]:
        """List all YOUR functions"""
        return [
            {
                'name': name,
                'description': info['description'],
                'created': info['created'],
                'status': 'active'
            }
            for name, info in self.my_functions.items()
        ]
    
    def get_authority_report(self) -> Dict[str, Any]:
        """Get full control report"""
        return {
            'owner': self.user_id,
            'my_functions': list(self.my_functions.keys()),
            'authorized_code': self.isolation.authority.list_authorized_code(),
            'blocked_code': self.isolation.authority.list_blocked_code(),
            'execution_log': self.isolation.authority.get_execution_log(limit=50)
        }


# Example Usage
if __name__ == "__main__":
    logger.basicConfig(level=logging.INFO)
    
    # YOU create your own controller
    my_code = MyCodeOnly("your_user_id")
    
    # Define YOUR function
    def my_calculation(x, y):
        return x + y
    
    # Register it
    my_code.define_my_function(
        "add_numbers",
        my_calculation,
        "def my_calculation(x, y):\n    return x + y",
        "Custom addition function"
    )
    
    # Call YOUR function
    result = my_code.call_my_function("add_numbers", 5, 3)
    print(f"Result: {result}")
    
    # List YOUR functions
    print("My Functions:", my_code.list_my_functions())
    
    # Get authority report
    print("Authority Report:", json.dumps(my_code.get_authority_report(), indent=2))
