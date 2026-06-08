#!/usr/bin/env python3
"""
Example integration hook showing how Hermes memory tool would be extended
to also capture memories to MemPalace raw layer.
"""
import json
import os
import sys
import subprocess
from datetime import datetime

def hermes_memory_hook(action, key=None, value=None, metadata=None):
    """
    Hook that extends Hermes memory tool to also store in MemPalace.
    
    This would be integrated into the Hermes memory tool implementation.
    """
    # Only handle 'set' operations for durable memories
    if action != 'set':
        # For other actions, just proceed normally (this is a simplified example)
        return {"status": "skipped", "reason": f"Only 'set' action triggers MemPalace capture"}
    
    # Extract information for MemPalace capture
    user_id = metadata.get('user_id', 'default') if metadata else 'default'
    session_id = metadata.get('session_id', 'default') if metadata else 'default'
    
    # Determine provisional type based on metadata or key patterns
    provisional_type = 'semantic'  # Default
    if metadata:
        if metadata.get('type') == 'preference':
            provisional_type = 'preference'
        elif metadata.get('type') == 'procedure' or 'how' in str(key).lower():
            provisional_type = 'procedural'
        elif metadata.get('type') == 'episodic' or 'event' in str(key).lower():
            provisional_type = 'episodic'
    
    # Prepare raw text for capture
    if isinstance(value, dict):
        raw_text = json.dumps(value)
    else:
        raw_text = str(value)
    
    # Add key context if available
    if key and key not in ['value', 'data']:
        raw_text = f"{key}: {raw_text}"
    
    # Determine salience based on metadata
    salience = metadata.get('salience', 0.7) if metadata else 0.7
    reliability = metadata.get('reliability', 0.8) if metadata else 0.8  # Hermes memories are generally reliable
    
    # Extract entities and topics (simplified)
    entities = []
    topics = []
    if metadata:
        entities = metadata.get('entities', [])
        topics = metadata.get('topics', [])
    
    # If not provided, try to extract from key/value
    if not entities and not topics:
        text_to_analyze = f"{key} {raw_text}".lower()
        # Simple entity extraction (would be more sophisticated in practice)
        if 'aws' in text_to_analyze or 'amazon web services' in text_to_analyze:
            entities.append('AWS')
            topics.append('cloud')
        if 'deployment' in text_to_analyze or 'deploy' in text_to_analyze:
            entities.append('deployment')
            topics.append('deployment')
        if 'staging' in text_to_analyze:
            entities.append('staging')
            topics.append('environment')
    
    # Capture to MemPalace raw layer
    try:
        # Use the capture script we created
        capture_cmd = [
            sys.executable,
            os.path.expanduser("~/.hermes/mempalace/bin/capture.py"),
            raw_text
        ]
        
        # We could pass additional parameters via environment or modify the script
        # For simplicity, we'll just call it with the text and enhance the JSON afterward
        result = subprocess.run(capture_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            memory_id = result.stdout.strip().split(': ')[-1]  # Extract memory ID from output
            
            # Enhance the captured memory with additional metadata
            raw_dir = os.path.expanduser("~/.hermes/mempalace/raw")
            memory_file = os.path.join(raw_dir, f"{memory_id}.json")
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory_event = json.load(f)
                
                # Update with our metadata
                memory_event.update({
                    "user_id": user_id,
                    "session_id": session_id,
                    "provisional_type": provisional_type,
                    "salience": salience,
                    "reliability": reliability,
                    "entities": entities,
                    "topics": topics,
                    "evidence_ref": f"hermes:{session_id}:{key or 'unknown'}"
                })
                
                with open(memory_file, 'w') as f:
                    json.dump(memory_event, f, indent=2)
                
                print(f"✓ Captured to MemPalace: {memory_id}")
                return {
                    "status": "success", 
                    "mempalace_id": memory_id,
                    "action": "captured_to_raw_layer"
                }
            else:
                return {"status": "error", "reason": "Failed to locate captured memory file"}
        else:
            return {"status": "error", "reason": f"Capture script failed: {result.stderr}"}
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "reason": "Capture script timed out"}
    except Exception as e:
        return {"status": "error", "reason": f"Capture error: {str(e)}"}

def example_usage():
    """
    Demonstrate example usage of the hook.
    """
    print("=== Hermes Memory Tool Integration Hook Demo ===\n")
    
    # Example 1: Storing a user preference
    print("Example 1: Storing user preference")
    result = hermes_memory_hook(
        action='set',
        key='ui.theme',
        value='dark',
        metadata={
            'user_id': 'u123',
            'session_id': 's456',
            'type': 'preference',
            'salience': 0.9,
            'reliability': 0.95,
            'entities': ['ui', 'theme'],
            'topics': ['interface', 'preferences']
        }
    )
    print(json.dumps(result, indent=2))
    print()
    
    # Example 2: Storing a procedural memory
    print("Example 2: Storing procedural knowledge")
    result = hermes_memory_hook(
        action='set',
        key='deployment.procedure',
        value={
            'steps': ['build', 'test', 'staging-deploy', 'production-deploy'],
            'environment': 'AWS',
            'rollback_enabled': True
        },
        metadata={
            'user_id': 'u123',
            'session_id': 's456',
            'type': 'procedure',
            'salience': 0.85,
            'reliability': 0.9,
            'entities': ['deployment', 'AWS'],
            'topics': ['devops', 'procedures']
        }
    )
    print(json.dumps(result, indent=2))
    print()
    
    # Example 3: Storing an episodic memory
    print("Example 3: Storing episodic memory")
    result = hermes_memory_hook(
        action='set',
        key='incident.report',
        value='Database connection pool exhaustion caused 5xx errors at 14:30 UTC. Resolved by increasing pool size and adding monitoring.',
        metadata={
            'user_id': 'u123',
            'session_id': 's456',
            'type': 'episodic',
            'salience': 0.9,
            'reliability': 0.95,  # Post-mortem is reliable
            'entities': ['database', 'connection-pool'],
            'topics': ['incident', 'post-mortem', 'database']
        }
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    example_usage()
EOF