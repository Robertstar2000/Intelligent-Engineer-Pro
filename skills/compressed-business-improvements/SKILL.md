---
name: compressed-business-improvements
description: ""
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

{"name":"business-improvements","goal":"Run daily system checks and optimizations","steps":[{"action":"inter_agent_communication","substeps":[{"action":"create_delivery_queue","dirs":["processed","archive"]},{"action":"create_delivery_queue_processor"},{"action":"create_agent_heartbeat_enhancer"},{"action":"create_soul_tracker"}]},{"action":"skill_utilization_analytics","substeps":[{"action":"create_skill_usage_logger"},{"action":"create_skill_recommender"}]},{"action":"memory_persistence_optimization","substeps":[{"action":"create_memory_optimizer"},{"action":"create_memory_compressor"}]},{"action":"tool_discovery_automation","substeps":[{"action":"create_tool_assessor"},{"action":"create_tool_recommender"}]},{"action":"run_daily_checks"}]}