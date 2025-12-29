# ScorePlay Migration Agent

Simple Python script to migrate MXF video files to ScorePlay with metadata extraction from filenames and optional XML sidecar files.

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure (create .env file)
cp .env.example .env
# Edit .env with your API key

# Run
python ScorePlay.py --simulate  # Test mode
python ScorePlay.py             # Live mode
```

## File Format

Files must follow this naming pattern:
```
{match_id}_{player_id}_{timestamp}.mxf
```

Example: `M1234_P5678_20240420T153000.mxf`

Optional XML sidecar files (same name with `.xml` extension) are automatically parsed for additional metadata.

## Configuration

Create a `.env` file:
```bash
SCOREPLAY_API_BASE_URL=https://dc.scoreplay.io/api
SCOREPLAY_API_KEY=your_api_key_here
SOURCE_PATH=./videos
REQUEST_TIMEOUT=10
```

## Features

- ✅ Extracts metadata from filenames (match_id, player_id, timestamp)
- ✅ Parses Dalet XML sidecar files automatically
- ✅ Creates assets in ScorePlay via API
- ✅ Simulation mode for testing (`--simulate` or `-s`)

## Architecture

- `ScorePlay.py` - Main migration script
- `dalet_connector.py` - Dalet XML parser
- `config.py` - Configuration management

## Support

**FDE**: Thomas Chauvel  
**API Docs**: https://developer.scoreplay.io/
