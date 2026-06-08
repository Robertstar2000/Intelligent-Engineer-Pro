---
name: daily-briefing-workflow
description: Systematic approach for generating daily briefings from multiple sources with progressive fallback strategies when primary sources fail
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [productivity, news, events, fallback, workflow]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Daily Briefing Workflow

A systematic approach for gathering comprehensive daily briefings from multiple sources, including fallback strategies when primary sources are inaccessible.

## Overview
This workflow provides a structured methodology for collecting daily briefing information (news, events, status updates) from multiple sources, with progressive fallback strategies when primary sources fail or return incomplete data.

## When to Use
- Generating daily status reports or briefings
- Aggregating information from multiple news sources
- Collecting local events and sports schedules
- Situations where primary data sources may be unreliable
- When you need to provide value despite incomplete information

## Workflow Steps

### 1. System Status Check (Primary)
Start with direct system queries to establish baseline status:
```
- Check process status (ps, systemctl)
- Verify service health (hermes status, doctor)
- Confirm tool availability
- Document current configuration
```

### 2. Primary Source Collection
Attempt to gather information from preferred sources in priority order:
```
- Use browser automation for news sites
- Access RSS feeds when available
- Query official APIs when accessible
- Follow platform-specific endpoints
```

### 3. Progressive Fallback Strategy
When primary sources fail, implement tiered fallback approaches:

**Tier 1: Alternative Access Methods**
```
- Try different URL patterns (homepage vs section pages)
- Use mobile vs desktop versions
- Access archived or cached content
- Try different user agents or headers
```

**Tier 2: Search-Based Collection**
```
- Use search engines with location-specific queries
- Query news aggregators
- Use social media monitoring
- Check multiple platforms for same information
```

**Tier 3: API-Based Collection**
```
- Use news APIs (NewsAPI, Google News)
- Access event APIs (Eventbrite, Meetup)
- Query sports APIs
- Use weather APIs for local conditions
```

**Tier 4: Synthetic Content Generation**
When real-time data is completely unavailable:
```
- Generate representative examples
- Provide historical context
- Create templates with placeholders
- Document information gaps transparently
```

### 4. Error Handling & Recovery
```python
def handle_collection_error(source, error, fallback_level):
    """Systematic error handling for data collection"""
    error_log.append({
        'source': source,
        'error': str(error),
        'timestamp': datetime.now(),
        'fallback': fallback_level
    })
    
    if fallback_level < MAX_FALLBACKS:
        return attempt_fallback(fallback_level + 1)
    else:
        return generate_placeholder_content(source)
```

### 5. Data Validation & Cross-Checking
- Verify information across multiple independent sources
- Check for consistency in dates, times, and details
- Flag contradictory information
- Document confidence levels for each data point

### 6. Progressive Reporting
Structure the final report to:
```
1. Present confirmed information first
2. Document what couldn't be obtained
3. Explain fallback methods used
4. Provide recommendations for next time
5. Include quality metrics (data freshness, source reliability)
```

## Common Issues & Solutions

### Issue: News Sites Return 404 Errors
**Solution:** 
- Try root domain instead of specific paths
- Use search queries instead of direct access
- Access via RSS feeds
- Use alternative local news sources

### Issue: Event Data Incomplete
**Solution:**
- Query multiple event platforms
- Use Facebook Events as fallback
- Generate representative event templates
- Document date ranges covered

### Issue: Sports Schedules Inconsistent
**Solution:**
- Cross-reference multiple sports sites
- Use official team APIs
- Provide date ranges instead of specific games
- Flag data quality issues

### Issue: System Access Denied
**Solution:**
- Use different authentication methods
- Query via API instead of web interface
- Use cached or historical data
- Document access limitations

## Quality Standards
- Always disclose when information is estimated or placeholder
- Provide source attribution for all data points
- Include timestamps for all collected information
- Flag contradictory or uncertain information
- Maintain consistent formatting across reports

## Customization Points
- Adjust fallback thresholds based on urgency
- Prioritize sources by reliability for each category
- Modify reporting format for different audiences
- Configure error notification preferences

## Example Implementation
```python
def generate_daily_briefing(location_preferences):
    """Main briefing generation function with fallback layers"""
    briefing = {
        'status': 'partial',
        'sources': {},
        'fallback_applied': [],
        'confidence': {}
    }
    
    # Collect each section with fallback
    briefing['local_news'] = collect_with_fallback(
        primary_sources=location_preferences['news_sources'],
        fallback_strategies=NEWS_FALLBACK_STRATEGIES
    )
    
    briefing['events'] = collect_with_fallback(
        primary_sources=location_preferences['event_sources'],
        fallback_strategies=EVENT_FALLBACK_STRATEGIES
    )
    
    # Continue for other sections...
    
    return format_briefing(briefing)
```

## Benefits
- Provides value even when primary sources fail
- Creates systematic approach to information gathering
- Reduces panic when sources are temporarily unavailable
- Builds institutional knowledge about source reliability
- Enables continuous improvement of source strategies

## Related Skills
- web-research: General web information gathering
- data-collection: Systematic data aggregation
- error-handling: Robust error management
- browser-automation: Web interaction techniques

## MEM PALACE INTEGRATION
When performing daily briefing tasks, also utilize the MemPalace Integration skill to enhance long-term memory retention and retrieval. This ensures that successful source strategies, fallback approaches, and reliability patterns are preserved across sessions for continuous improvement.