---
name: news-gathering-workflow
description: A systematic approach for collecting local news, events, and sports information from multiple web sources while navigating access restrictions and bot detection.
version: 1.0.0
author: Hermes Agent + Teknium
license: MIT
metadata:
  hermes:
    tags: [research, news, events, sports, web-scraping, bot-detection]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [hermes-agent, creative-writing, research]
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# News Gathering Workflow for Hermes Agent

A systematic approach for collecting local news, events, and sports information from multiple web sources while navigating access restrictions and bot detection.

## Overview
This workflow provides a structured methodology for gathering comprehensive local information from news websites, event platforms, and sports sites. It's particularly useful when facing access restrictions, bot detection, or when needing to extract structured data from unstructured web pages.

## When to Use
- Daily news briefings requiring local coverage
- Event discovery for specific geographic areas
- Sports schedule and score tracking
- Any task requiring information from multiple web sources with varying access controls

## Workflow Steps

### 1. Source Identification and Prioritization
**Primary Local News Sources:**
- Identify local newspapers and news websites (e.g., Grand Haven Tribune, Tampa Bay Times)
- Check for local TV station websites
- Look for community news portals

**Event Platforms:**
- Eventbrite (search by location)
- Facebook Events (if accessible)
- Local community center websites
- Library event calendars

**Sports Sources:**
- Official university athletic sites (msuspartans.com, mgoblue.com)
- Professional team sites (rowdiessoccer.com)
- ESPN team pages
- Conference websites

### 2. Access Strategy and Bot Detection Handling
**When facing bot detection or access restrictions:**

**A. Try different navigation patterns:**
- Start with main news/event pages rather than direct article links
- Use search functions on the site
- Navigate through category pages (news/local, events/)

**B. Use console scraping when page content is accessible but structured data is hidden:**
```javascript
// Example: Extract article headlines and summaries
const articles = Array.from(document.querySelectorAll('article'));
const headlines = articles.map(article => {
    const title = article.querySelector('h2 a')?.textContent.trim();
    const summary = article.querySelector('p')?.textContent.trim();
    return {title, summary};
});
console.log(JSON.stringify(headlines, null, 2));
```

**C. Use browser_vision for visual analysis when text extraction fails:**
- Take screenshots of relevant sections
- Ask specific questions about content
- Use annotate mode to identify interactive elements

**D. Try different user-agents or timing:**
- Add delays between actions
- Use browser tools with stealth features
- Try accessing different sections of the site

### 3. Data Extraction Patterns

**For News Sites:**
- Look for article lists in `<main>` or news sections
- Extract: headline, summary, URL, timestamp
- Prioritize recent articles (last 24-48 hours)

**For Eventbrite:**
- Navigate to location-specific event pages
- Extract: event name, date/time, venue, city, ticket info
- Filter for next 48 hours

**For Sports Sites:**
- Find schedule/roster pages
- Extract: team names, dates, times, venues, scores
- Check multiple sections (baseball, basketball, etc.)

### 4. Fallback and Alternative Approaches

**If primary source fails:**
1. Try secondary local news source
2. Use search engines with location-specific queries
3. Check social media (Twitter, Facebook) for local updates
4. Use official government or tourism sites for events

**For sports information:**
- Try ESPN teams pages
- Check conference websites
- Use sports API alternatives if available
- Search for "team schedule 2026" directly

### 5. Data Organization and Validation

**Structure extracted data consistently:**
```json
{
  "source": "Grand Haven Tribune",
  "category": "local_news",
  "items": [
    {
      "headline": "Planning Commission considers zoning changes",
      "summary": "The commission is reviewing several zoning amendments...",
      "url": "https://www.grandhaventribune.com/news/local/...",
      "timestamp": "2026-04-22T10:00:00-04:00"
    }
  ]
}
```

**Validate completeness:**
- Cross-check multiple sources for major events
- Verify event times and dates
- Confirm sports scores with multiple outlets when possible

### 6. Error Handling and Troubleshooting

**Common Issues and Solutions:**

**Bot Detection:**
- Use browser with stealth features enabled
- Add human-like delays (2-5 seconds between actions)
- Start with less sensitive pages (contact, about) to establish session
- Use different browser profiles or sessions

**Access Restrictions:**
- Try textise dot iitty (textise dot iitty.org for Wikipedia)
- Use textise dot iitty for news sites when available
- Check if site has RSS feeds as alternative

**Incomplete Data:**
- Document what's missing and why
- Provide alternative sources if available
- Note limitations in the final report

### 7. Quality Standards

**News Items:**
- Prioritize recent, relevant local content
- Include source attribution
- Keep summaries concise (1-2 sentences)
- Verify local relevance (within specified radius)

**Events:**
- Include date, time, venue, and location
- Filter for upcoming 48 hours
- Include both recurring and one-time events
- Note ticket availability when relevant

**Sports:**
- Include team names, dates, times, venues
- Note scores and recent performance
- Cover specified teams only

### 8. Automation Considerations

**When to use delegate_task vs. direct browser navigation:**
- Use `delegate_task` for complex, multi-source research
- Use direct browser navigation for quick, single-source checks
- Consider cron jobs for regular briefings

**Performance optimization:**
- Cache results when possible
- Use session persistence for multi-step extractions
- Parallelize independent source queries

## Example Implementation

```python
# Sample function for gathering local news
def gather_local_news(location, radius_miles=25, days_back=2):
    """
    Gather local news for a specific location within a radius.
    Returns structured data with headlines, summaries, and sources.
    """
    sources = {
        'newspaper': f'https://www.{location.replace(" ", "").lower()}.com',
        'eventbrite': f'https://www.eventbrite.com/d/{location.replace(" ", "-")}/events/',
        'sports': {
            'msu': 'https://msuspartans.com/sports',
            'um': 'https://mgoblue.com',
            'rowdies': 'https://rowdiessoccer.com'
        }
    }
    
    results = {}
    
    # News extraction
    news_url = sources['newspaper']
    browser_navigate(url=news_url)
    snapshot = browser_snapshot(full=True)
    # Extract articles using patterns...
    
    return results
```

## Customization Points
- Adjust location radius based on population density
- Modify time windows for events (48 hours vs. weekly)
- Add/remove source types based on availability
- Customize sports coverage based on user preferences

## Related Skills
- hermes-agent: General Hermes usage and configuration
- creative-writing: For narrative content creation
- research: For academic and technical research

## Benefits
- Provides comprehensive local coverage
- Handles access restrictions systematically
- Produces structured, consistent output
- Reduces manual effort for regular briefings