---
name: ai-api-integration
description: Methodology for integrating with AI APIs and troubleshooting common issues
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [api, integration, troubleshooting, ai, methodology]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [openrouter-image-generator, image-generation-workflow]
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# AI API Integration Methodology

This skill captures the systematic approach for integrating with AI APIs and troubleshooting common issues, based on the experience of attempting to integrate black-forest-labs/flux.2-max via OpenRouter.

## When to Use This Skill

Use this methodology when:
- Integrating with a new AI API or service
- A model integration fails or behaves unexpectedly
- You need to diagnose API connectivity or compatibility issues
- You want to verify model availability before investing implementation time

## Key Principles

1. **Verify availability first** - Check if the model exists on the platform before building integration
2. **Test with simple requests** - Start with basic API calls before complex implementations
3. **Understand API scope** - Know whether the API supports chat, completions, images, or other modalities
4. **Document diagnostic steps** - Keep track of what you tried and what worked/failed
5. **Have fallback options** - Know alternative services that offer similar functionality

## Step-by-Step Integration Process

### 1. Research and Availability Check

```python
# Check if model exists on platform
import requests

# Get list of available models
response = requests.get("https://api.openrouter.ai/v1/models")
models = response.json()

# Search for your model ID
model_id = "black-forest-labs/flux.2-max"
if any(m['id'] == model_id for m in models['models']):
    print(f"Model {model_id} found!")
else:
    print(f"Model {model_id} not available on this platform")
```

**Alternative approach**: Browse the platform's website directly to confirm model availability.

### 2. API Endpoint Verification

Different model types may use different endpoints:
- **Chat models**: `/v1/chat` endpoint
- **Completion models**: `/v1/completions` endpoint
- **Image models**: May require different API structure or not be supported at all

**Test basic connectivity**:
```bash
curl -X POST "https://api.openrouter.ai/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model": "claude-3-opus", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 3. Diagnostic Steps for Integration Failures

#### A. Check Response Format
- **JSON response**: API is working correctly
- **HTML response**: Wrong endpoint or unsupported model type
- **404 Not Found**: Model ID incorrect or model doesn't exist
- **401 Unauthorized**: API key invalid or missing

#### B. Model Type Mismatch
If you get HTML when expecting JSON, you may be trying to use:
- An image generation model on a chat API
- A model that requires special parameters
- A model that uses a different API version

#### C. Authentication Issues
- Verify API key is correctly set
- Check if the key has proper permissions
- Ensure the key hasn't expired

#### D. Rate Limiting and Quotas
- Check API response for rate limit headers
- Monitor your usage in the platform dashboard
- Consider implementing retry logic with exponential backoff

### 4. Common Error Patterns and Solutions

#### Error: "Expecting value: line 1 column 1 (char 0)"
**Cause**: Empty or non-JSON response (usually HTML)
**Solution**: 
- Verify you're using the correct endpoint
- Confirm the model type supports the API you're using
- Check if the model requires a different API version

#### Error: 404 Not Found
**Cause**: Model doesn't exist or endpoint is wrong
**Solution**:
- Double-check model ID spelling
- Verify the model is available on the platform
- Try a simpler test with a known working model

#### Error: 401 Unauthorized
**Cause**: Invalid or missing API key
**Solution**:
- Verify API key in configuration
- Check environment variable is set correctly
- Regenerate key if necessary

### 5. Alternative Service Evaluation

When a model isn't available on your preferred platform, evaluate alternatives:

#### Research Alternative Providers
```python
# Example: Check Replicate for Flux.2 Max
import requests
response = requests.get("https://api.replicate.com/v1/models")
# Search for model in response
```

#### Comparison Criteria
- **API reliability** - Uptime, error rates
- **Cost** - Price per request/image/token
- **Ease of integration** - Documentation quality, SDK availability
- **Rate limits** - Requests per second/minute
- **Features** - Supported parameters, output formats

#### Common Alternative Services
- **Replicate**: `replicate.com` - Good for image models
- **Hugging Face**: `huggingface.co` - Wide model selection
- **Stability AI**: `platform.stability.ai` - Stable Diffusion models
- **RunPod**: `runpod.io` - GPU hosting with model marketplace
- **Banana.dev**: `banana.dev` - AI infrastructure platform

### 6. Documentation and Knowledge Capture

After resolving an integration issue, document:
- What the problem was
- How you diagnosed it
- What the solution was
- Alternative approaches you considered
- Lessons learned for future integrations

This prevents repeating the same troubleshooting steps in the future.

## Lessons from Flux.2 Max Integration Attempt

### What We Tried
1. Created a skill assuming Flux.2 Max was available on OpenRouter
2. Wrote Python code to call OpenRouter API
3. Got HTML response instead of JSON
4. Discovered Flux.2 Max is not available on OpenRouter for image generation
5. Identified that OpenRouter only supports chat-based models

### Key Learnings
1. **Always verify model availability** before building integration
2. **Understand API scope** - chat APIs vs. image generation APIs are fundamentally different
3. **Test with simple requests** early to catch platform limitations
4. **Have alternative services ready** when primary platform doesn't support needed models

### Best Practices for Future Integrations
1. Start with a basic connectivity test
2. Use platform browsing to confirm model availability
3. Check platform documentation for model-specific requirements
4. Consider using multiple services to access different model ecosystems

## Related Skills

- `openrouter-image-generator` - The original skill (now documented with limitations)
- `image-generation-workflow` - General image generation approaches
- `replicate-integration` - (If created) Integration with Replicate API

## Maintenance

This skill should be updated whenever:
- New diagnostic steps are discovered
- Alternative services become available
- Platform APIs change significantly
- New integration patterns emerge