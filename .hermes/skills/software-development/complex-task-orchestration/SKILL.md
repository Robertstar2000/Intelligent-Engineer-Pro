---
name: complex-task-orchestration
description: Orchestrate large-scale, multi-component tasks in Hermes that require systematic execution across different domains (writing, coding, configuration, automation).
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Complex Task Orchestration in Hermes

Use this skill to orchestrate large-scale, multi-component tasks in Hermes that require systematic execution across different domains (writing, coding, configuration, automation). This skill provides a framework for breaking down complex objectives into manageable components, tracking progress, and ensuring consistency across implementations.

## Outcome

Build a reusable approach for:
1. Decomposing complex tasks into sequential and parallel components
2. Maintaining consistency across multiple implementations (agents, skills, configs)
3. Managing system constraints (memory limits, file formats)
4. Setting up automated maintenance and verification
5. Documenting lessons learned for future reuse

## Core Principles

- **Modular Decomposition**: Break large objectives into independent, testable components
- **Consistency Patterns**: Use templates and reference implementations to ensure uniformity
- **Constraint Awareness**: Monitor and adapt to system limitations (memory, API rates, etc.)
- **Verification Loops**: Build in checkpoints to validate progress before proceeding
- **Documentation as You Go**: Save insights and approaches as skills/memory for future reuse

## Functional Components

### 1) Task Analysis & Decomposition
- Identify core objectives and required deliverables
- Determine dependencies between components
- Classify tasks as sequential vs parallelizable
- Estimate effort and identify potential bottlenecks
- Define clear completion criteria for each component

### 2) Component Implementation Framework
- Create reference implementations for common patterns
- Use templates to ensure consistency across similar components
- Implement validation checks for each component type
- Document assumptions and prerequisites
- Plan for error handling and recovery paths

### 3) Progress Tracking & Validation
- Establish clear metrics for completion (file counts, skill updates, etc.)
- Implement regular check-ins to verify progress
- Use automated validation where possible (scripts, linting, tests)
- Maintain a visible progress indicator (dashboard, log, report)
- Define exit criteria for each phase

### 4) Consistency Management
- Create reference implementations for repeated patterns
- Use search/replace with context for bulk updates
- Implement versioning for templates and reference files
- Validate consistency after bulk operations
- Document deviations and justify exceptions

### 5) Automation & Maintenance Setup
- Identify repetitive tasks suitable for automation
- Configure cron jobs, hooks, or scheduled tasks
- Implement self-healing or self-correcting mechanisms
- Set up monitoring and alerting for critical components
- Plan for regular review and update cycles

### 6) Knowledge Capture & Transfer
- Save effective approaches as skills immediately after use
- Document pitfalls and solutions encountered
- Create reference implementations for future teams
- Transfer knowledge through clear documentation
- Update related skills and memory with lessons learned

## Hermes-Specific Patterns

### Writing Projects
- Chapter templates with required elements (dialogue, transitions, etc.)
- Consistent formatting and style guidelines
- Progress tracking by chapter count/completion
- Automated compilation and verification scripts
- Character and lore consistency checks

### Skill Deployment
- Reference skill templates with standard sections
- Consistent metadata and categorization
- Automated validation of skill structure
- Reference implementations for common patterns
- Dependency tracking and conflict resolution

### Configuration Management
- Template configurations with variable substitution
- Validation scripts for config correctness
- Change tracking and rollback procedures
- Environment-specific overrides
- Secret management and secure distribution

### Automation Configuration
- Cron job templates with standard formatting
- Skill dependency management
- Delivery target configuration
- Error handling and logging setup
- Monitoring and health check integration

## Implementation Workflow

### Phase 1: Foundation
1. Clear objective definition and success criteria
2. Resource assessment and constraint identification
3. Reference implementation creation for core patterns
4. Tool and skill preparation
5. Initial progress tracking setup

### Phase 2: Component Execution
1. Sequential components: Execute in dependency order
2. Parallel components: Batch similar tasks for efficiency
3. Regular validation checkpoints
4. Adaptive replanning based on learned constraints
5. Intermediate knowledge capture as skills

### Phase 3: Integration & Consistency
1. Cross-component consistency verification
2. Reference implementation application
3. Bulk update execution with validation
4. Conflict resolution and exception handling
5. Final integration testing

### Phase 4: Automation & Handoff
1. Maintenance automation setup (cron, hooks)
2. Documentation completion and knowledge transfer
3. Final verification and sign-off
4. Knowledge capture as reusable skills
5. Retrospective and improvement planning

## Risk Management

### Common Risks
- Scope creep from undefined requirements
- Inconsistency across similar implementations
- Constraint exhaustion (memory, time, API limits)
- Integration failures between components
- Knowledge loss during execution

### Mitigation Strategies
- Rigorous objective definition and change control
- Reference implementations and templates
- Regular constraint monitoring and adaptive planning
- Interface contracts and integration testing
- Continuous knowledge capture and skill creation

## Verification Checklist

Before considering a component complete:
- [ ] Meets all defined acceptance criteria
- [ ] Has been validated through testing or inspection
- [ ] Consistent with reference implementations
- [ ] Documented with lessons learned and pitfalls
- [ ] Integrated with related components as required
- [ ] Has associated knowledge captured (skill/memory update)
- [ ] Includes any necessary automation or maintenance setup

## Knowledge Capture Guidelines

Save immediately when:
- You discover a non-obvious solution to a problem
- You develop a reference implementation worth reusing
- You identify a pattern that applies to multiple similar tasks
- You learn important constraints or limitations of the system
- You develop an effective verification or validation approach
- You create a template that eliminates repetitive work

Format knowledge as:
- Skills for reusable procedures and approaches
- Memory for factual information and preferences
- Reference implementations in appropriate locations
- Updated documentation for existing skills and configs

## Example Application: Writing a Novel Series

Applied this approach to write 64 chapters of "Second Generation":
1. Decomposed into: chapter writing, consistency maintenance, compilation
2. Used chapter template with required Mission AI dialogue and transitions
3. Tracked progress by chapter count and content verification
4. Created reference chapters for consistency checking
5. Set up automated compilation and verification
6. Captured approach as this skill for future writing projects

## Example Application: System-Wide Skill Deployment

Applied this approach to deploy MemPalace Integration:
1. Decomposed into: skill creation, agent updates, cron setup, memory configuration
2. Used reference SKILL.md template with standard sections
3. Implemented consistent MEM PALACE INTEGRATION sections across all agents
4. Set up daily cron job for maintenance
5. Configured memory system for knowledge persistence
6. Created this skill to capture the orchestration approach

## Example Application: Automated Daily Workflows Setup

Applied this approach to configure automated daily workflows with Telegram delivery:
1. Decomposed into: memory maintenance job, daily briefing job, business analysis job
2. Created mempalace-integration skill for long-term memory enhancement
3. Set up three cron jobs with specific schedules (3 AM, 7 AM, 8 AM daily)
4. Configured delivery targets to send insights to Telegram chat
5. Combined appropriate skills for each job's purpose:
   - mempalace-integration for memory maintenance
   - hermes-agent + novel-writing-workflow for daily briefing
   - hermes-agent + research-paper-writing for business analysis
6. Updated all 15 OpenClaw agent skills with consistent MEM PALACE INTEGRATION sections
7. Added memory entry to ensure future agents/skills include the reference
8. Verified all configurations and next run times