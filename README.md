# ScorePlay Migration Agent
## FC Test United - Forward Deployed Engineer Solution

Simple Python script to migrate MXF video files to ScorePlay with metadata extraction from filenames and optional XML sidecar files.

---

## Repository Structure

This repository is organized according to the assessment deliverables:

### Part 1: Migration & Deployment Proposal
📄 **`docs/FC-Test-United-Technical-doc.pdf`**  
Customer technical proposal and deployment strategy.

### Part 2: Code Implementation & Documentation
**Source Code:**
- `ScorePlay.py` - Main migration script
- `dalet_connector.py` - Dalet XML parser module
- `config.py` - Configuration management

**Code Documentation:**
- `docs/CODE_QUALITY.md` - Design decisions and code quality documentation

### Part 3: Customer Handover Note
📄 **`docs/MIGRATION_PLAN.md`**  
Complete customer handover documentation including:
- Custom Glue components (Dalet Connector, ...)
- ScorePlay product features leveraged
- Residual risks for go-live
- Operational procedures

### Part 4: Future Enhancements
📄 **`docs/AI-Ideas.md`**  
AI-driven optimization opportunities:
- Neural compression for storage optimization
- Vision-based metadata extraction
- Probabilistic validation layer

---

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

## Project Structure

```
ScorePlay/
├── ScorePlay.py              # Main migration script
├── dalet_connector.py        # Dalet XML parser
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # This file
└── docs/                     # Documentation
    ├── FC-Test-United-Technical-doc.pdf  # Part 1: Proposal
    ├── CODE_QUALITY.md                    # Part 2: Code docs
    ├── MIGRATION_PLAN.md                  # Part 3: Handover
    └── AI-Ideas.md                        # Part 4: Enhancements
```

## Support

**FDE**: Thomas Chauvel  
**API Docs**: https://developer.scoreplay.io/
