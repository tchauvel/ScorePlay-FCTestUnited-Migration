# Configuration Setup

## Environment Variables

Create a `.env` file in the project root with the following:

```bash
# ScorePlay API Configuration
SCOREPLAY_API_BASE_URL=https://dc.scoreplay.io/api
SCOREPLAY_API_KEY=your_api_key_here

# Source directory for MXF files
SOURCE_PATH=./videos

# Request timeout in seconds
REQUEST_TIMEOUT=10
```

## Security Notes

- The `.env` file is excluded from git (see `.gitignore`)
- Never commit API keys to version control
- Use different `.env` files for different environments (dev, staging, prod)
- The `.env.example` file shows the required structure without sensitive data

## Usage

The configuration is automatically loaded from:
1. `.env` file (if present)
2. Environment variables (takes precedence)
3. Default values (for non-sensitive settings)

