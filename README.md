# branded

An AI agent repository with API key configuration support.

## Setup

### Prerequisites
- Python 3.8 or higher
- An API key from your chosen AI provider (OpenAI, Anthropic, etc.)

### API Key Configuration

This project requires API keys to interact with AI services. Follow these steps to set up your API keys:

#### 1. Get Your API Key

**For OpenAI (recommended):**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy your API key (you won't be able to see it again!)

**For other providers:**
- **Anthropic Claude**: Visit [Anthropic Console](https://console.anthropic.com/)
- **Google AI**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Hugging Face**: Visit [Hugging Face Tokens](https://huggingface.co/settings/tokens)

#### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in your text editor and replace the placeholder values with your actual API keys:
   ```bash
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

#### 3. Verify Your Setup

You can verify your API key is configured correctly by checking if the environment variable is set:

```bash
# On Linux/Mac
echo $OPENAI_API_KEY

# On Windows (PowerShell)
$env:OPENAI_API_KEY
```

## Usage

Once your API keys are configured, you can start using the AI agent. (Usage instructions will be added as the project develops)

## Security Notes

- **Never share your API keys** publicly or commit them to version control
- **Rotate your keys** regularly for better security
- **Use environment variables** to keep keys separate from code
- **Monitor your usage** on your provider's dashboard to avoid unexpected charges

## Support

For issues or questions, please open an issue on GitHub.