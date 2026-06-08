---
name: compressed-business-improvements
description: ""
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("business improvements automation monitoring optimization", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

{"name":"business-improvements","goal":"Run daily system checks and optimizations","steps":[{"action":"inter_agent_communication","substeps":[{"action":"create_delivery_queue","dirs":["processed","archive"]},{"action":"create_delivery_queue_processor"},{"action":"create_agent_heartbeat_enhancer"},{"action":"create_soul_tracker"}]},{"action":"skill_utilization_analytics","substeps":[{"action":"create_skill_usage_logger"},{"action":"create_skill_recommender"}]},{"action":"memory_persistence_optimization","substeps":[{"action":"create_memory_optimizer"},{"action":"create_memory_compressor"}]},{"action":"tool_discovery_automation","substeps":[{"action":"create_tool_assessor"},{"action":"create_tool_recommender"}]},{"action":"run_daily_checks"}]}