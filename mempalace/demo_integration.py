#!/usr/bin/env python3
"""
Demo script showing how to use the MemPalace long-term memory enhancement layer.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mempalace import (
    init_mempalace,
    capture_memory,
    retrieve_memory,
    reinforce_memory
)

def main():
    print("=== MemPalace Demo ===")
    
    # Initialize the MemPalace system
    init_mempalace()
    
    # Capture some sample memories
    print("\n--- Capturing memories ---")
    
    memory1 = capture_memory({
        'type': 'user_interaction',
        'content': 'User asked about the progress on the MIFECO book writing project',
        'context': 'MIFECO dashboard, book writing, chapter 3',
        'timestamp': '2026-05-01T02:30:00Z'
    })
    print(f"Captured memory 1: {memory1}")
    
    memory2 = capture_memory({
        'type': 'book_writing',
        'content': 'Completed chapter 3 of the MIFECO book, focusing on AI agent architectures',
        'context': 'Book writing, MIFECO, chapter 3 completed',
        'timestamp': '2026-05-01T01:15:00Z'
    })
    print(f"Captured memory 2: {memory2}")
    
    memory3 = capture_memory({
        'type': 'research',
        'content': 'Researching different memory augmentation techniques for AI agents',
        'context': 'AI research, memory systems, long-term memory',
        'timestamp': '2026-04-30T14:20:00Z'
    })
    print(f"Captured memory 3: {memory3}")
    
    # Retrieve memories related to book progress
    print("\n--- Retrieving memories for 'book progress' ---")
    memories = retrieve_memory('book progress', k=5)
    
    for i, mem in enumerate(memories, 1):
        print(f"\n{i}. [{mem['type']}] {mem['content']}")
        print(f"   Timestamp: {mem['timestamp']}")
        print(f"   Score: {mem.get('score', 'N/A')}")
        print(f"   Layer: {mem['explainability']['layer']}")
        print(f"   Explanation: {mem['explainability']['explanation_text']}")
    
    # Demonstrate reinforcement
    print("\n--- Reinforcing a memory ---")
    if memories:
        reinforce_memory(memories[0]['id'], success=True, context='User found this information helpful')
        print(f"Reinforced memory {memories[0]['id']}")
    
    print("\n=== Demo Complete ===")

if __name__ == '__main__':
    main()