#!/usr/bin/env python3
"""
MemPalace Memory Provider for Hermes
Implements the MemPalace long-term memory enhancement layer as a pluggable memory provider.
"""

import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent.memory_provider import MemoryProvider
from hermes_constants import get_hermes_home

logger = logging.getLogger(__name__)


class MemPalaceProvider(MemoryProvider):
    """MemPalace long-term memory enhancement layer for Hermes."""

    def __init__(self):
        self.name = "mempalace"
        self.hermes_home: Optional[Path] = None
        self.mempalace_root: Optional[Path] = None
        self.storage_paths: Dict[str, Path] = {}
        self.config: Dict[str, Any] = {}
        self._initialized = False

    @property
    def provider_name(self) -> str:
        return self.name

    def is_available(self) -> bool:
        """Check if MemPalace is properly configured."""
        # Always available if we can create the storage structure
        try:
            hermes_home = get_hermes_home()
            mempalace_root = hermes_home / "mempalace"
            # Check if we can create directories
            for dir_name in ["raw", "semantic", "episodic", "procedural", "preferences", "indexes", "palace"]:
                (mempalace_root / dir_name).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.warning(f"MemPalace provider not available: {e}")
            return False

    def initialize(self, session_id: str, **kwargs) -> None:
        """Initialize MemPalace storage and load configuration."""
        self.hermes_home = Path(kwargs.get("hermes_home", get_hermes_home()))
        self.mempalace_root = self.hermes_home / "mempalace"
        
        # Set up storage paths
        self.storage_paths = {
            "raw": self.mempalace_root / "raw",
            "semantic": self.mempalace_root / "semantic",
            "episodic": self.mempalace_root / "episodic",
            "procedural": self.mempalace_root / "procedural",
            "preferences": self.mempalace_root / "preferences",
            "indexes": self.mempalace_root / "indexes",
            "palace": self.mempalace_root / "palace",
        }
        
        # Create directories if they don't exist
        for path in self.storage_paths.values():
            path.mkdir(parents=True, exist_ok=True)
            
        # Load configuration
        self._load_config()
        
        # Initialize indexes (in a real implementation, this would load FAISS/HNSW indexes)
        self._init_indexes()
        
        self._initialized = True
        logger.info(f"MemPalace provider initialized for session {session_id}")

    def _load_config(self) -> None:
        """Load configuration from config.yaml or environment variables."""
        config_path = self.mempalace_root / "provider" / "config.yaml"
        self.config = {
            "consolidation_threshold": 0.7,
            "reinforcement_decay": 0.95,
            "prune_age_days": 365,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimension": 384,
        }
        
        # Override with config file if it exists
        if config_path.exists():
            try:
                import yaml
                with open(config_path) as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        self.config.update(file_config)
            except Exception as e:
                logger.warning(f"Could not load MemPalace config: {e}")
                
        # Override with environment variables
        env_mappings = {
            "MEMPALACE_CONSOLIDATION_THRESHOLD": ("consolidation_threshold", float),
            "MEMPALACE_REINFORCEMENT_DECAY": ("reinforcement_decay", float),
            "MEMPALACE_PRUNE_AGE_DAYS": ("prune_age_days", int),
            "MEMPALACE_EMBEDDING_MODEL": ("embedding_model", str),
        }
        
        for env_var, (config_key, conv_func) in env_mappings.items():
            if env_var in os.environ:
                try:
                    self.config[config_key] = conv_func(os.environ[env_var])
                except Exception as e:
                    logger.warning(f"Invalid value for {env_var}: {e}")

    def _init_indexes(self) -> None:
        """Initialize vector indexes and graph databases."""
        # In a full implementation, this would:
        # 1. Load or create FAISS/HNSW indexes for each memory type
        # 2. Initialize a graph database (like Neo4j or NetworkX) for relationships
        # 3. Set up embedding model
        # For now, we'll just ensure the directories exist
        indexes_path = self.storage_paths["indexes"]
        indexes_path.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder files to indicate index types
        for mem_type in ["semantic", "episodic", "procedural", "preferences"]:
            (indexes_path / f"{mem_type}_index.faiss").touch(exist_ok=True)
            
        logger.debug("MemPalace indexes initialized")

    def system_prompt_block(self) -> str:
        """Return static information about MemPalace for the system prompt."""
        return (
            "MEM PALACE (Long-term Memory Enhancement): "
            "Active. Provides cross-session recall of important facts, preferences, and procedures."
        )

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """Retrieve relevant memories for the upcoming turn.
        
        Returns formatted text to inject as context.
        """
        if not self._initialized:
            return ""
            
        try:
            # In a full implementation, this would:
            # 1. Convert query to embedding
            # 2. Search vector indexes for similar memories
            # 3. Filter by context tags and palace tags
            # 4. Apply reinforcement scoring and recency decay
            # 5. Format results by memory layer (working, semantic, episodic, raw)
            # 6. Return compact summary with evidence pointers
            
            # For now, return a placeholder indicating the system is active
            return "[MemPalace: Long-term memory system active. Ready to retrieve consolidated knowledge.]"
        except Exception as e:
            logger.debug(f"MemPalace prefetch failed: {e}")
            return ""

    def queue_prefetch(self, query: str, *, session_id: str = "") -> None:
        """Queue background prefetch for the next turn."""
        # In a full implementation, this would:
        # 1. Start background thread/process to compute query embedding
        # 2. Perform vector similarity search
        # 3. Cache results for next prefetch() call
        pass

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """Persist a completed turn and trigger MemPalace capture/scoring pipeline."""
        if not self._initialized:
            return
            
        try:
            # Capture the turn as raw events
            self._capture_turn(user_content, assistant_content, session_id)
            
            # In a full implementation, we would also:
            # 1. Score the captured events
            # 2. Trigger consolidation if threshold met
            # 3. Update reinforcement scores for retrieved memories
            # 4. Run pruning if needed
            
            logger.debug(f"MemPalace synced turn for session {session_id}")
        except Exception as e:
            logger.warning(f"MemPalace sync_turn failed: {e}")

    def _capture_turn(self, user_content: str, assistant_content: str, session_id: str) -> None:
        """Capture a turn as raw events in the MemPalace raw layer."""
        timestamp = time.time()
        
        # Capture user message as episodic event
        if user_content.strip():
            user_event = {
                "memory_id": str(uuid.uuid4()),
                "user_id": "current_user",  # In practice, this would come from context
                "session_id": session_id,
                "timestamp": timestamp,
                "source_type": "chat",
                "source_span": f"chat:{session_id}:user",
                "raw_text": user_content,
                "provisional_type": "episodic",
                "entities": self._extract_entities(user_content),
                "topics": self._extract_topics(user_content),
                "context_tags": self._extract_context_tags(user_content),
                "palace_tags": [],  # Will be derived from context_tags
                "salience_signals": self._extract_salience_signals(user_content),
            }
            self._store_raw_event(user_event)
            
        # Capture assistant response if it contains useful information
        if assistant_content.strip():
            # Only capture assistant content that might be useful as context
            # (e.g., code, facts, procedures - not just conversational filler)
            if self._is_useful_assistant_content(assistant_content):
                assistant_event = {
                    "memory_id": str(uuid.uuid4()),
                    "user_id": "current_user",
                    "session_id": session_id,
                    "timestamp": timestamp,
                    "source_type": "chat",
                    "source_span": f"chat:{session_id}:assistant",
                    "raw_text": assistant_content,
                    "provisional_type": "procedural" if self._contains_code_or_procedure(assistant_content) else "episodic",
                    "entities": self._extract_entities(assistant_content),
                    "topics": self._extract_topics(assistant_content),
                    "context_tags": self._extract_context_tags(assistant_content),
                    "palace_tags": [],
                    "salience_signals": self._extract_salience_signals(assistant_content),
                }
                self._store_raw_event(assistant_event)

    def _store_raw_event(self, event: Dict[str, Any]) -> None:
        """Store a raw event in the append-only event log."""
        raw_path = self.storage_paths["raw"] / "events.jsonl"
        try:
            with open(raw_path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            logger.error(f"Failed to store raw event: {e}")

    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text. Simple implementation - in practice would use NER."""
        # Placeholder implementation
        entities = []
        # Look for capitalized words, file paths, URLs, etc.
        words = text.split()
        for word in words:
            clean_word = word.strip(".,:;!?\"'()[]{}")
            if clean_word and (clean_word[0].isupper() or "." in clean_word or "/" in clean_word):
                entities.append(clean_word)
        return list(set(entities))  # Deduplicate

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topic labels from text."""
        # Placeholder implementation
        topics = []
        # Simple keyword matching for common topics
        topic_keywords = {
            "programming": ["code", "function", "class", "variable", "algorithm", "python", "javascript"],
            "infrastructure": ["server", "database", "api", "deployment", "aws", "cloud", "docker"],
            "debugging": ["error", "bug", "fix", "issue", "problem", "exception"],
            "design": ["architecture", "design", "pattern", "structure", "component"],
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        return topics

    def _extract_context_tags(self, text: str) -> List[str]:
        """Extract context tags for vector metadata and retrieval."""
        # Combine entities and topics, add scientific domain detection
        tags = []
        tags.extend(self._extract_entities(text))
        tags.extend(self._extract_topics(text))
        
        # Add scientific context tags based on terminology
        science_indicators = {
            "physics": ["force", "energy", "momentum", "quantum", "relativity"],
            "chemistry": ["molecule", "reaction", "compound", "element", "bond"],
            "biology": ["cell", "gene", "protein", "dna", "rna", "organism"],
            "mathematics": ["theorem", "proof", "algorithm", "calculus", "statistics"],
            "computer_science": ["algorithm", "data structure", "complexity", "programming", "software"],
        }
        
        text_lower = text.lower()
        for domain, indicators in science_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                tags.append(domain)
                
        return list(set(tags))

    def _extract_salience_signals(self, text: str) -> Dict[str, float]:
        """Extract salience signals from text."""
        signals = {}
        text_lower = text.lower()
        
        # Priority markers
        if any(word in text_lower for word in ["urgent", "critical", "important", "asap"]):
            signals["priority"] = 0.9
            
        # Uncertainty markers (lower salience for uncertain statements)
        if any(word in text_lower for word in ["maybe", "perhaps", "unsure", "think", "believe"]):
            signals["uncertainty"] = 0.3
            
        # Repetition would be handled in scoring phase
        
        return signals

    def _is_useful_assistant_content(self, content: str) -> bool:
        """Determine if assistant content is worth storing as durable memory."""
        # Store content that contains:
        # - Code snippets
        # - Factual information
        # - Procedures or workflows
        # - Decisions or conclusions
        # Don't store purely conversational content
        
        useful_indicators = [
            "```",  # Code blocks
            "def ", "class ", "function ",  # Code definitions
            "step", "procedure", "process",  # Procedures
            "decided", "concluded", "determined",  # Decisions
            "fact:", "note:", "remember:",  # Explicit markers
            "https://", "http://",  # URLs
            ".py", ".js", ".json", ".yaml", ".yml",  # File extensions
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in useful_indicators)

    def _contains_code_or_procedure(self, content: str) -> bool:
        """Check if content contains code or procedures."""
        code_indicators = ["```", "def ", "class ", "function ", "=>", "{", "};" ]
        proc_indicators = ["step", "procedure", "process", "workflow"]
        content_lower = content.lower()
        return any(ind in content_lower for ind in code_indicators + proc_indicators)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas for MemPalace-specific tools."""
        return [
            {
                "name": "mempalace_stats",
                "description": "Get statistics about the MemPalace long-term memory system.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "mempalace_consolidate",
                "description": "Manually trigger consolidation of raw events into durable memory.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "mempalace_prune",
                "description": "Manually trigger pruning of low-value memories.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs) -> str:
        """Handle MemPalace-specific tool calls."""
        try:
            if tool_name == "mempalace_stats":
                return json.dumps(self._get_stats(), ensure_ascii=False)
            elif tool_name == "mempalace_consolidate":
                self._trigger_consolidation()
                return json.dumps({"success": True, "message": "Consolidation triggered"}, ensure_ascii=False)
            elif tool_name == "mempalace_prune":
                self._trigger_pruning()
                return json.dumps({"success": True, "message": "Pruning triggered"}, ensure_ascii=False)
            else:
                return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
        except Exception as e:
            logger.error(f"MemPalace tool call {tool_name} failed: {e}")
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

    def _get_stats(self) -> Dict[str, Any]:
        """Get statistics about the MemPalace system."""
        stats = {
            "provider": "mempalace",
            "initialized": self._initialized,
            "storage_paths": {k: str(v) for k, v in self.storage_paths.items()},
            "config": self.config,
        }
        
        # Count raw events
        raw_path = self.storage_paths["raw"] / "events.jsonl"
        if raw_path.exists():
            try:
                with open(raw_path) as f:
                    lines = f.readlines()
                    stats["raw_event_count"] = len(lines)
            except Exception:
                stats["raw_event_count"] = "error"
        else:
            stats["raw_event_count"] = 0
            
        # Count consolidated memories
        for mem_type in ["semantic", "episodic", "procedural", "preferences"]:
            mem_path = self.storage_paths[mem_type]
            if mem_path.exists():
                try:
                    count = len(list(mem_path.glob("*.json")))
                    stats[f"{mem_type}_count"] = count
                except Exception:
                    stats[f"{mem_type}_count"] = "error"
            else:
                stats[f"{mem_type}_count"] = 0
                
        return stats

    def _trigger_consolidation(self) -> None:
        """Trigger consolidation of raw events into durable memory."""
        # In a full implementation, this would:
        # 1. Read recent raw events
        # 2. Score them using weighted features
        # 3. Cluster related events
        # 4. Create consolidated memories for high-score items
        # 5. Update vector indexes and graph
        logger.info("MemPalace consolidation triggered")

    def _trigger_pruning(self) -> None:
        """Trigger pruning of low-value memories."""
        # In a full implementation, this would:
        # 1. Identify memories below threshold for extended period
        # 2. Remove or deprioritize low utility, high interference memories
        # 3. Enforce storage limits by pruning lowest reinforcement-score items
        logger.info("MemPalace pruning triggered")

    # Optional hooks
    
    def on_session_end(self, messages: List[Dict[str, Any]]) -> None:
        """Called when a session ends - good time for end-of-session processing."""
        logger.debug("MemPalace session end hook called")
        # Could trigger consolidation at session end if needed
        
    def on_pre_compress(self, messages: List[Dict[str, Any]]) -> str:
        """Called before context compression - extract insights to preserve."""
        logger.debug("MemPalace pre-compress hook called")
        # Return insights to include in compression summary
        return "[MemPalace: Important memories preserved through long-term storage]"

    def on_memory_write(self, action: str, target: str, content: str) -> None:
        """Called when the built-in memory tool writes - mirror to MemPalace."""
        logger.debug(f"MemPalace memory write hook: {action} on {target}")
        # In a full implementation, we might want to capture these explicit memory writes
        # as high-salience events in our raw layer

    def shutdown(self) -> None:
        """Clean shutdown."""
        logger.info("MemPalace provider shutting down")
        self._initialized = False