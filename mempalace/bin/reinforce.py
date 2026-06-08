#!/usr/bin/env python3
"""
Reinforce memories based on successful retrieval and usage.
"""
import json
import os
import sys
from datetime import datetime, timezone

def reinforce_memory(memory_id, reinforcement_type="used_in_successful_answer", 
                    boost_amount=0.1):
    """
    Reinforce a memory by increasing its reinforcement count and adjusting score.
    """
    # Search across all stores for the memory
    base_dir = os.path.expanduser("~/.hermes/mempalace")
    store_types = ['semantic', 'episodic', 'procedural', 'preferences', 'raw']
    
    memory_found = False
    memory_data = None
    store_type = None
    
    for store in store_types:
        store_dir = os.path.join(base_dir, store)
        if not os.path.exists(store_dir):
            continue
            
        for filename in os.listdir(store_dir):
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(store_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if data.get('memory_id') == memory_id:
                    memory_found = True
                    memory_data = data
                    store_type = store
                    break
            except Exception as e:
                print(f"Error reading {filepath}: {e}", file=sys.stderr)
        
        if memory_found:
            break
    
    if not memory_found:
        print(f"Memory {memory_id} not found in any store", file=sys.stderr)
        return False
    
    # Update reinforcement count
    current_count = memory_data.get('reinforcement_count', 0)
    memory_data['reinforcement_count'] = current_count + 1
    
    # Add reinforcement event to history
    if 'reinforcement_history' not in memory_data:
        memory_data['reinforcement_history'] = []
    
    reinforcement_event = {
        "type": reinforcement_type,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "boost_amount": boost_amount
    }
    memory_data['reinforcement_history'].append(reinforcement_event)
    
    # Optionally adjust confidence based on reinforcement
    # More reinforcement = slightly higher confidence (up to a point)
    current_confidence = memory_data.get('confidence', 0.5)
    new_confidence = min(0.95, current_confidence + (boost_amount * 0.5))
    memory_data['confidence'] = new_confidence
    
    # Write back the updated memory
    try:
        with open(filepath, 'w') as f:
            json.dump(memory_data, f, indent=2)
        print(f"Reinforced memory {memory_id} with {reinforcement_type}")
        print(f"  Reinforcement count: {current_count} -> {memory_data['reinforcement_count']}")
        print(f"  Confidence: {current_confidence:.3f} -> {new_confidence:.3f}")
        return True
    except Exception as e:
        print(f"Error writing reinforced memory: {e}", file=sys.stderr)
        return False

def contradict_memory(memory_id, contradiction_source="user_feedback"):
    """
    Contradict a memory, reducing confidence and marking for re-evaluation.
    """
    base_dir = os.path.expanduser("~/.hermes/mempalace")
    store_types = ['semantic', 'episodic', 'procedural', 'preferences', 'raw']
    
    memory_found = False
    memory_data = None
    store_type = None
    filepath = None
    
    for store in store_types:
        store_dir = os.path.join(base_dir, store)
        if not os.path.exists(store_dir):
            continue
            
        for filename in os.listdir(store_dir):
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(store_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if data.get('memory_id') == memory_id:
                    memory_found = True
                    memory_data = data
                    store_type = store
                    break
            except Exception as e:
                print(f"Error reading {filepath}: {e}", file=sys.stderr)
        
        if memory_found:
            break
    
    if not memory_found:
        print(f"Memory {memory_id} not found in any store", file=sys.stderr)
        return False
    
    # Add contradiction to the memory
    if 'contradicted_by' not in memory_data:
        memory_data['contradicted_by'] = []
    
    contradiction_event = {
        "source": contradiction_source,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    memory_data['contradicted_by'].append(contradiction_event)
    
    # Reduce confidence
    current_confidence = memory_data.get('confidence', 0.5)
    new_confidence = max(0.1, current_confidence * 0.8)  # Reduce by 20%
    memory_data['confidence'] = new_confidence
    
    # Write back
    try:
        with open(filepath, 'w') as f:
            json.dump(memory_data, f, indent=2)
        print(f"Contradicted memory {memory_id} from {contradiction_source}")
        print(f"  Confidence: {current_confidence:.3f} -> {new_confidence:.3f}")
        print(f"  Contradictions: {len(memory_data['contradicted_by'])}")
        return True
    except Exception as e:
        print(f"Error writing contradicted memory: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: reinforce.py <memory_id> [reinforcement_type]", file=sys.stderr)
        print("Reinforcement types: used_in_successful_answer, confirmed_by_user, frequently_retrieved")
        print("Use contradict.py for contradictions")
        sys.exit(1)
    
    memory_id = sys.argv[1]
    reinforcement_type = sys.argv[2] if len(sys.argv) > 2 else "used_in_successful_answer"
    
    success = reinforce_memory(memory_id, reinforcement_type)
    sys.exit(0 if success else 1)
EOF