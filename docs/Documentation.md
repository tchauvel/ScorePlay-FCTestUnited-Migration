# ScorePlay Migration Agent - Documentation

Complete technical and usage documentation for the ScorePlay Migration Agent.

---

## Quick Start

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
SCOREPLAY_API_BASE_URL=https://dc.scoreplay.io/api
SCOREPLAY_API_KEY=your_api_key_here
SOURCE_PATH=./videos
REQUEST_TIMEOUT=10
```

### Usage

**Simulation Mode (Test):**
```bash
python ScorePlay.py --simulate
# or
python ScorePlay.py -s
```
Shows detailed metadata extraction for each file.

**Live Mode (Production):**
```bash
python ScorePlay.py
```
Processes all MXF files and creates assets in ScorePlay.

---

## File Format

Files must follow this naming pattern:

```
{match_id}_{player_id}_{timestamp}.mxf
```

**Example:** `M1234_P5678_20240420T153000.mxf`

**Components:**
- `match_id`: M followed by digits (e.g., M1234)
- `player_id`: P followed by digits (e.g., P5678)
- `timestamp`: YYYYMMDDTHHMMSS format (e.g., 20240420T153000)

**Optional XML Sidecar:**
If an XML file exists with the same base name (e.g., `M1234_P5678_20240420T153000.xml`), additional metadata is automatically extracted.

---

## Code Reference

### Modules

**ScorePlay.py** - Main migration workflow  
**dalet_connector.py** - Dalet XML sidecar parser  
**config.py** - Configuration management

### Functions

#### `parse_filename(file_path) -> dict | None`

Extracts metadata from MXF filename: `{match_id}_{player_id}_{timestamp}.mxf`

**Returns:** `{"match_id": "M1234", "player_id": "P5678", "timestamp": "2024-04-20T15:30:00Z"}` or `None`

#### `create_asset_payload(video_path, filename_metadata, xml_metadata) -> dict`

Builds ScorePlay API payload. Merges filename and XML metadata.

#### `create_scoreplay_asset(payload, simulate=False) -> tuple[bool, dict|None]`

Creates asset via ScorePlay API.

**Returns:** `(True, response_data)` on success, `(False, error_dict)` on failure

**API:** `POST https://dc.scoreplay.io/api/assets`  
**Auth:** Bearer token  
**Status Codes:** 200-299 success, 400-499 client error, 500+ server error

#### `run_migration(simulate=False) -> None`

Main workflow: processes all `.mxf` files in source directory.

1. Parse filename
2. Parse XML sidecar (optional)
3. Create asset via API
4. Report summary

#### `parse_dalet_xml(xml_path: Path) -> dict`

Parses Dalet XML sidecar file. Extracts all fields from `<titles><title>` structure.

**Returns:** Metadata dict (empty if file missing or parse fails)

### Configuration

**Environment Variables** (`.env` file):
- `SCOREPLAY_API_KEY` (required)
- `SCOREPLAY_API_BASE_URL` (default: `https://dc.scoreplay.io/api`)
- `SOURCE_PATH` (default: `./videos`)
- `REQUEST_TIMEOUT` (default: `10`)

**Exported Constants:**
- `API_URL` - Full API endpoint
- `HEADERS` - HTTP headers with auth
- `SOURCE` - Source directory Path
- `FILENAME_PATTERN` - Regex pattern
- `REQUEST_TIMEOUT` - Timeout in seconds

### API Payload

```json
{
  "external_id": "/absolute/path/to/file.mxf",
  "name": "M1234_P5678_20240420T153000.mxf",
  "date": "2024-04-20T15:30:00Z",
  "metadata": {
    "match_id": "M1234",
    "player_id": "P5678",
    "fde_source": "Dalet_Connector_v1",
    "competition": "Ligue 1 UberEats",
    ...
  }
}
```

---

## Error Handling

- **Invalid filenames:** Skipped with warning
- **Missing XML:** Returns empty dict (optional)
- **API errors:** Categorized by HTTP status code
- **Network errors:** Timeout, ConnectionError caught and logged

---

## Troubleshooting

**API Authentication Error:**
- Check `.env` file has correct `SCOREPLAY_API_KEY`
- Verify API key hasn't expired

**Files Not Processing:**
- Check filename matches pattern: `M\d+_P\d+_\d{8}T\d{6}\.mxf`
- Verify source directory path in `.env`
- Check file permissions

**Network Errors:**
- Verify network connectivity
- Increase `REQUEST_TIMEOUT` in `.env` if needed

---

## Features

- ✅ Extracts metadata from filenames (match_id, player_id, timestamp)
- ✅ Parses Dalet XML sidecar files automatically
- ✅ Creates assets in ScorePlay via API
- ✅ Simulation mode for testing
- ✅ Error handling and logging

