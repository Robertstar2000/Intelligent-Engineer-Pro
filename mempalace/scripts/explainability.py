#!/usr/bin/env python3
"""
MemPalace Explainability Metadata Script
Maintains explainability traces for all memories.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Storage paths
HOME = os.path.expanduser("~")
SEMANTIC_DIR = os.path.join(HOME, ".hermes/mempalace/semantic")
EPISODIC_DIR = os.path.join(HOME, ".hermes/mempalace/episodic")
PROCEDURAL_DIR = os.path.join(HOME, ".hermes/mempalace/procedural")
PREFERENCES_DIR = os.path.join(HOME, ".hermes/mempalace/preferences")
EXPLAINABILITY_DIR = os.path.join(HOME, ".hermes/mempalace/indexes/explainability")

def ensure_dirs():
    """Ensure storage directories exist."""
    for dir_path in [SEMANTIC_DIR, EPISODIC_DIR, PROCEDURAL_DIR, PREFERENCES_DIR, EXPLAINABILITY_DIR]:
        os.makedirs(dir_path, exist_ok=True)

def add_explainability_metadata(memory: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add explainability metadata to a memory.
    
    Args:
        memory: Memory dictionary to enhance
    
    Returns:
        Enhanced memory with explainability metadata
    """
    memory_id = memory.get("memory_id")
    if not memory_id:
        return memory
    
    # Initialize explainability if not present
    if "explainability" not in memory:
        memory["explainability"] = {}
    
    expl = memory["explainability"]
    
    # Add origin information if not present
    if "origin" not in expl:
        expl["origin"] = {
            "capture_events": [],  # Would be populated from raw events
            "consolidation_event": f"consolidated_at:{datetime.now(timezone.utc).isoformat()}",
            "source_type": memory.get("source_type", "unknown"),
            "session_id": memory.get("session_id", "unknown")
        }
    
    # Add confidence if not present
    if "confidence" not in expl:
        expl["confidence"] = memory.get("confidence", 0.5)
    
    # Add context if not present
    if "context" not in expl:
        expl["context"] = {
            "tags": memory.get("context_tags", []),
            "palace_location": memory.get("palace_tags", []),
            "temporal_validity": memory.get("validity_window", "unknown"),
            "entities": memory.get("entities", []),
            "relations": memory.get("relations", [])
        }
    
    # Add contradictions if not present
    if "contradictions" not in expl:
        expl["contradictions"] = {
            "pointers": memory.get("contradicted_by", []),
            "resolution_status": "unknown" if not memory.get("contradicted_by") else "unresolved"
        }
    
    # Add reinforcement history if not present
    if "reinforcement_history" not in expl:
        expl["reinforcement_history"] = {
            "retrieval_count": memory.get("reinforcement_count", 0),
            "application_count": 0,  # Would be tracked separately
            "last_retrieved": None,
            "last_applied": None,
            "decay_curve": {
                "initial_salience": memory.get("score", 0.5),
                "current_salience": memory.get("score", 0.5),
                "projected_salience_30d": memory.get("score", 0.5) * 0.8,  # Simplified decay
                "projected_salience_90d": memory.get("score", 0.5) * 0.6
            }
        }
    
    # Add metadata about when explainability was last updated
    expl["last_updated"] = datetime.now(timezone.utc).isoformat()
    expl["version"] = "1.0"
    
    return memory

def update_explainability_on_retrieval(memory_id: str):
    """Update explainability metadata when a memory is retrieved."""
    # This would be called from the retrieval script
    memory_types = ["semantic", "episodic", "procedural", "preference"]
    
    for mem_type in memory_types:
        dir_path = {
            "semantic": SEMANTIC_DIR,
            "episodic": EPISODIC_DIR,
            "procedural": PROCEDURAL_DIR,
            "preference": PREFERENCES_DIR
        }[mem_type]
        
        if not os.path.exists(dir_path):
            continue
            
        filename = os.path.join(dir_path, f"{memory_id}.json")
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    memory = json.load(f)
                
                # Update reinforcement history
                if "explainability" in memory and "reinforcement_history" in memory["explainability"]:
                    memory["explainability"]["reinforcement_history"]["retrieval_count"] += 1
                    memory["explainability"]["reinforcement_history"]["last_retrieved"] = datetime.now(timezone.utc).isoformat()
                
                # Update last updated timestamp
                if "explainability" in memory:
                    memory["explainability"]["last_updated"] = datetime.now(timezone.utc).isoformat()
                
                # Save updated memory
                with open(filename, "w") as f:
                    json.dump(memory, f, indent=2)
                
                return True
            except:
                continue
    
    return False

def update_explainability_on_application(memory_id: str):
    """Update explainability metadata when a memory is successfully applied."""
    # Similar to retrieval but for application
    memory_types = ["semantic", "episodic", "procedural", "preference"]
    
    for mem_type in memory_types:
        dir_path = {
            "semantic": SEMANTIC_DIR,
            "episodic": EPISODIC_DIR,
            "procedural": PROCEDURAL_DIR,
            "preference": PREFERENCES_DIR
        }[mem_type]
        
        if not os.path.exists(dir_path):
            continue
            
        filename = os.path.join(dir_path, f"{memory_id}.json")
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    memory = json.load(f)
                
                # Update reinforcement history
                if "explainability" in memory and "reinforcement_history" in memory["explainability"]:
                    memory["explainability"]["reinforcement_history"]["application_count"] += 1
                    memory["explainability"]["reinforcement_history"]["last_applied"] = datetime.now(timezone.utc).isoformat()
                
                # Update last updated timestamp
                if "explainability" in memory:
                    memory["explainability"]["last_updated"] = datetime.now(timezone.utc).isoformat()
                
                # Save updated memory
                with open(filename, "w") as f:
                    json.dump(memory, f, indent=2)
                
                return True
            except:
                continue
    
    return False

def get_explainability_summary(memory_id: str) -> Optional[Dict[str, Any]]:
    """Get explainability summary for a memory."""
    memory_types = ["semantic", "episodic", "procedural", "preference"]
    
    for mem_type in memory_types:
        dir_path = {
            "semantic": SEMANTIC_DIR,
            "episodic": EPISODIC_DIR,
            "procedural": PROCEDURAL_DIR,
            "preference": PREFERENCES_DIR
        }[mem_type]
        
        if not os.path.exists(dir_path):
            continue
            
        filename = os.path.join(dir_path, f"{memory_id}.json")
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    memory = json.load(f)
                
                return memory.get("explainability", {})
            except:
                continue
    
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python explainability.py <memory_id> [retrieve|apply]")
        sys.exit(1)
    
    memory_id = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "none"
    
    if action == "retrieve":
        success = update_explainability_on_retrieval(memory_id)
        print(f"Updated explainability for retrieval: {success}")
    elif action == "apply":
        success = update_explainability_on_application(memory_id)
        print(f"Updated explainability for application: {success}")
    else:
        summary = get_explainability_summary(memory_id)
        if summary:
            print(json.dumps(summary, indent=2))
        else:
            print(f"No explainability found for memory {memory_id}")