import json
import os
from datetime import datetime, timezone

def reinforce_memory(memory_id, storage_path=None, reinforcement_type='successful_retrieval'):
    """
    Reinforce a memory by increasing its rehearsal count or updating metadata.
    
    Args:
        memory_id (str): The ID of the memory to reinforce.
        storage_path (str, optional): Path to the mempalace storage directory.
        reinforcement_type (str): Type of reinforcement ('successful_retrieval', 'application', etc.).
    
    Returns:
        bool: True if reinforcement was successful, False otherwise.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Find the memory in any store (prefer semantic/episodic over raw)
    memory_event = None
    store_type = None
    
    for store in ['semantic', 'episodic', 'raw']:
        store_dir = os.path.join(storage_path, store)
        filepath = os.path.join(store_dir, f"{memory_id}.jsonl")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        data = json.loads(line)
                        if isinstance(data, dict):
                            memory_event = data
                            store_type = store
                            break
            except Exception:
                continue
    
    if memory_event is None:
        print(f"Memory {memory_id} not found for reinforcement")
        return False
    
    # Update reinforcement metadata
    if 'reinforcement_history' not in memory_event:
        memory_event['reinforcement_history'] = []
    
    reinforcement_event = {
        'type': reinforcement_type,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'count': 1
    }
    
    memory_event['reinforcement_history'].append(reinforcement_event)
    
    # Update rehearsal count (simple increment)
    if 'rehearsal_count' not in memory_event:
        memory_event['rehearsal_count'] = 0
    memory_event['rehearsal_count'] += 1
    
    # Update the memory in its store
    try:
        # Rewrite the file with updated memory
        store_dir = os.path.join(storage_path, store_type)
        filepath = os.path.join(store_dir, f"{memory_id}.jsonl")
        
        # Read all lines, replace the first line (assuming one memory per file for simplicity)
        lines = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        if lines:
            lines[0] = json.dumps(memory_event) + '\n'
            with open(filepath, 'w') as f:
                f.writelines(lines)
        
        print(f"Reinforced memory {memory_id} with {reinforcement_type}")
        return True
    except Exception as e:
        print(f"Error reinforcing memory {memory_id}: {e}")
        return False

def reinforce_by_query(query, storage_path=None, reinforcement_type='successful_retrieval'):
    """
    Reinforce memories that match a query (e.g., after successful retrieval).
    
    Args:
        query (str): The query that was successfully used.
        storage_path (str, optional): Path to the mempalace storage directory.
        reinforcement_type (str): Type of reinforcement.
    
    Returns:
        int: Number of memories reinforced.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Import retrieve function to find matching memories
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from retrieve import retrieve_memory
    
    # Get matching memories
    memories = retrieve_memory(query, storage_path=storage_path)
    
    reinforced_count = 0
    for memory in memories:
        memory_id = memory.get('id')
        if memory_id and reinforce_memory(memory_id, storage_path, reinforcement_type):
            reinforced_count += 1
    
    return reinforced_count

def get_reinforcement_stats(memory_id, storage_path=None):
    """
    Get reinforcement statistics for a memory.
    
    Args:
        memory_id (str): The ID of the memory.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: Reinforcement statistics.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Find the memory
    memory_event = None
    for store in ['semantic', 'episodic', 'raw']:
        store_dir = os.path.join(storage_path, store)
        filepath = os.path.join(store_dir, f"{memory_id}.jsonl")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        data = json.loads(line)
                        if isinstance(data, dict):
                            memory_event = data
                            break
            except Exception:
                continue
    
    if memory_event is None:
        return {}
    
    reinforcement_history = memory_event.get('reinforcement_history', [])
    rehearsal_count = memory_event.get('rehearsal_count', 0)
    
    # Count by type
    type_counts = {}
    for event in reinforcement_history:
        event_type = event.get('type', 'unknown')
        type_counts[event_type] = type_counts.get(event_type, 0) + 1
    
    return {
        'memory_id': memory_id,
        'rehearsal_count': rehearsal_count,
        'total_reinforcements': len(reinforcement_history),
        'reinforcement_by_type': type_counts,
        'latest_reinforcement': reinforcement_history[-1] if reinforcement_history else None
    }