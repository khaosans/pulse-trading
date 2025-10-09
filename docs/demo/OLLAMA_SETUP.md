# 🤖 Ollama AI Assistant Setup Guide

## What is Ollama?

Ollama allows you to run large language models locally on your machine. For PulseTrade, we use it to power an AI trading assistant that provides personalized advice based on your emotional state and market conditions.

## Installation

### Step 1: Install Ollama

**macOS:**
```bash
brew install ollama
```

**Or download from:** https://ollama.ai/download

### Step 2: Start Ollama Service

```bash
ollama serve
```

This starts the Ollama API server on `http://localhost:11434`

### Step 3: Pull a Model

**Recommended Models:**

```bash
# Llama 2 (7B) - Good balance of speed and quality
ollama pull llama2

# Mistral (7B) - Faster, great for quick responses
ollama pull mistral

# Llama 3.2 (3B) - Lighter, faster
ollama pull llama3.2
```

### Step 4: Test It

```bash
ollama run llama2 "What is a stop-loss order?"
```

## Using with PulseTrade

### Auto Mode (Ollama Running)
When Ollama is running, the AI Assistant will use the local model to provide real-time, context-aware trading advice.

### Demo Mode (Ollama Not Running)
If Ollama isn't running, the assistant automatically falls back to demo mode with helpful tips.

## How It Works

### Context-Aware Advice
The AI receives your:
- Current emotional state (e.g., "Calm 72%")
- Portfolio value and P/L
- Recent emotion alerts
- Historical performance data

### Example Queries:
- "Should I trade when I'm feeling anxious?"
- "How to set stop losses effectively?"
- "What's the best time to buy stocks?"
- "Explain the RSI indicator"
- "How can I manage risk better?"

## Performance Tips

### Choose the Right Model:
- **llama2** - Best for detailed, thoughtful responses
- **mistral** - Faster, concise answers
- **llama3.2** - Quickest, lighter responses

### Optimize Settings:
```bash
# Set custom parameters
ollama run llama2 --temperature 0.7 --max-tokens 500
```

## Troubleshooting

### Ollama Not Responding

**Check if running:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello",
  "stream": false
}'
```

**Restart Ollama:**
```bash
pkill ollama
ollama serve
```

### Model Not Found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama2
```

### Slow Responses
- Use a smaller model (llama3.2 instead of llama2)
- Reduce max tokens
- Upgrade RAM (8GB minimum recommended)

## Demo Mode

If you don't want to install Ollama, the demo works perfectly fine! The AI Assistant will provide helpful trading tips and guidance without requiring local AI.

### Demo Mode Features:
✅ Still provides trading guidance  
✅ Shows emotion-aware tips  
✅ Demonstrates the UX  
✅ Perfect for presentations  

## Advanced: Custom Trading Model

### Fine-tune for Trading:
```bash
# Create a Modelfile
cat > Modelfile <<EOF
FROM llama2
SYSTEM You are a professional trading advisor specializing in emotional trading psychology and technical analysis.
EOF

# Create custom model
ollama create trading-advisor -f Modelfile
```

### Use Custom Model:
Update `demo_app.py`:
```python
ai_response = query_ollama(context, model="trading-advisor")
```

## API Reference

### Ollama API Endpoint:
```
POST http://localhost:11434/api/generate
```

### Request Format:
```json
{
  "model": "llama2",
  "prompt": "Your question here",
  "stream": false
}
```

### Response Format:
```json
{
  "response": "AI generated response here"
}
```

## Resources

- **Ollama Docs:** https://github.com/ollama/ollama
- **Model Library:** https://ollama.ai/library
- **API Docs:** https://github.com/ollama/ollama/blob/main/docs/api.md

## Quick Commands

```bash
# Start Ollama
ollama serve

# List models
ollama list

# Pull model
ollama pull llama2

# Run model
ollama run llama2

# Stop Ollama
pkill ollama
```

---

**Note:** Ollama is optional! The demo works great without it in demo mode.


