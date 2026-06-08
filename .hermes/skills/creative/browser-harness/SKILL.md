---
name: browser-harness
version: 1.0.0
category: creative
description: Browser automation harness for web interaction, scraping, and task automation.
overview: >
  The browser harness is a powerful tool for autonomous web interaction. It
  combines a Chromium browser with an AI language model to perform tasks like
  web scraping, form filling, navigation, and content extraction. The system
  uses a feedback loop where the AI examines the page, decides on an action,
  executes it, and repeats until the task is complete.

  This skill covers installation, configuration, and usage patterns for the
  browser-use library, including support for multiple LLM providers (Google,
  OpenAI, Anthropic, and BrowserUse Cloud).
features:
  - Autonomous web browsing and interaction
  - Multi-provider LLM support (Google, OpenAI, Anthropic, BrowserUse Cloud)
  - Browser automation with real-time decision making
  - Form filling, navigation, and content extraction
  - Production-ready with cookie synchronization and proxy support
setup: |
  1. Install the package and Chromium:
     ```
     pip install browser-use
     uvx browser-use install
     ```

  2. Create a .env file with API keys:
     ```
     BROWSER_USE_API_KEY=your_browseruse_key
     GOOGLE_API_KEY=your_google_key
     ```

  3. Test the installation with a simple script.
usage: |
  Basic usage pattern:
  ```
  from browser_use import Agent, ChatGoogle
  from dotenv import load_dotenv
  import asyncio

  load_dotenv()

  async def main():
      llm = ChatGoogle(model="gemini-flash-latest")
      task = "Your task description here"
      agent = Agent(task=task, llm=llm)
      await agent.run()

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  For more control, you can customize the Browser instance:
  ```
  from browser_use import Browser, ChatGoogle

  browser = Browser(
      headless=False,  # Show browser window
      use_cloud=True,  # Use BrowserUse Cloud for better performance
      extensions=[...] # Load extensions
  )
  ```
providers: 
  - Google (Gemini) - requires GOOGLE_API_KEY
  - OpenAI - requires OPENAI_API_KEY
  - Anthropic - requires ANTHROPIC_API_KEY
  - BrowserUse Cloud - requires BROWSER_USE_API_KEY (optimized for browser use)
examples:
  - Web scraping: "Extract all product prices from this e-commerce site"
  - Form automation: "Fill out this form with the following data"
  - Research: "Find the top 5 news articles about AI today"
  - Testing: "Test the login flow of this web application"
best_practices: |
  - Start with simple tasks and gradually increase complexity
  - Use clear, specific task descriptions
  - Monitor the agent's progress and intervene if needed
  - Use the `use_cloud=True` option for better performance and captcha solving
  - Store API keys securely in environment variables
troubleshooting: |
  - API request failed: Free tier accounts may have limits. Consider upgrading.
  - Navigation issues: Ensure URLs are correct and accessible.
  - Captcha detection: Use BrowserUse Cloud with proxies for better results.
  - Browser crashes: Check system resources and update Chromium.
dependencies:
  - browser-use package
  - Python 3.10+
  - Chromium or Chrome browser
  - LLM provider API access
related_skills:
  - web-scraping
  - form-automation
  - research-aggregation
  - web-testing
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## CAPTCHA Handling Patterns

Canvas-based CAPTCHAs (Amazon-style) are hardened against automation. They render images on a single `<canvas>` element and validate `event.isTrusted` — programmatically dispatched events are always `isTrusted=false` and will be rejected regardless of the event type (PointerEvent, MouseEvent, TouchEvent, click).

### Strategies in order of reliability

**1. USER-ASSISTED (most reliable)** — Navigate to the login form, fill in credentials, then pause for the user to solve the CAPTCHA manually. Resume automation after authentication succeeds. Use `browser_vision` with a screenshot so the user can see the puzzle.

**2. SESSION COOKIE REUSE** — If a valid authenticated session exists (browser profile cookies), inject them before the login page loads. This skips the CAPTCHA entirely. Works for repeat visits.

**3. AUDIO CAPTCHA + STT** — Amazon's audio CAPTCHA plays a spoken number sequence. Extract the base64 audio data from the `<audio>` element's `src`, decode it, and transcribe with whisper/STT. The audio is typically 8-10 seconds of AAC data (~70K base64). Caveat: extraction and decoding is impractical within a single tool call due to data size.

**4. THIRD-PARTY SOLVING** — Services like BrowserUse Cloud, 2Captcha, or Anti-Captcha can solve image CAPTCHAs via API. Requires API key and internet access.

### What does NOT work
- PointerEvent / MouseEvent / TouchEvent dispatch (isTrusted=false)
- Canvas pixel manipulation
- Keyboard navigation (Amazon captcha grid has no keyboard-accessible cells)
- Hidden button overlay elements (Amazon uses pure canvas, no overlays)
