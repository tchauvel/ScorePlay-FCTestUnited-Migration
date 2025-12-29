"""
ScorePlay Migration Agent

Migrates MXF video files to ScorePlay by:
1. Extracting metadata from structured filenames
2. Parsing optional Dalet XML sidecar files
3. Creating assets via ScorePlay API

Business Context:
- This is a focused migration tool for one-time archive ingestion
- Not a full product - designed to solve the specific migration need
- Minimal scope: metadata extraction + API integration
- Production-ready but purpose-built for this use case
"""
import re
import requests
import sys
from datetime import datetime
from dalet_connector import parse_dalet_xml
from config import API_URL, HEADERS, SOURCE, FILENAME_PATTERN, REQUEST_TIMEOUT

FILENAME_REGEX = re.compile(FILENAME_PATTERN)


def parse_filename(file_path):
    """
    Extract metadata from structured filename.
    
    Expected format: {match_id}_{player_id}_{timestamp}.mxf
    Example: M1234_P5678_20240420T153000.mxf
    
    Returns: dict with match_id, player_id, timestamp or None if invalid
    """
    match = FILENAME_REGEX.match(file_path.stem)
    if not match:
        return None
    
    try:
        timestamp = datetime.strptime(match.group("t"), "%Y%m%dT%H%M%S").isoformat() + "Z"
        return {
            "match_id": match.group("m"),
            "player_id": match.group("p"),
            "timestamp": timestamp
        }
    except ValueError:
        return None


def create_asset_payload(video_path, filename_metadata, xml_metadata):
    """
    Build ScorePlay API payload for asset creation.
    
    Args:
        video_path: Path to the MXF file
        filename_metadata: Dict with match_id, player_id, timestamp
        xml_metadata: Dict with additional metadata from XML sidecar
    
    Returns: API payload dict
    """
    return {
        "external_id": str(video_path.absolute()),
        "name": video_path.name,
        "date": filename_metadata["timestamp"],
        "metadata": {
            "match_id": filename_metadata["match_id"],
            "player_id": filename_metadata["player_id"],
            "fde_source": "Dalet_Connector_v1",
            **xml_metadata  # Merge XML metadata
        }
    }


def create_scoreplay_asset(payload, simulate=False):
    """
    Create asset in ScorePlay via API.
    
    Args:
        payload: Asset payload dict
        simulate: If True, show detailed output
    
    Returns: tuple (success: bool, response_data: dict or None)
    """
    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        
        # Handle successful responses (200-299)
        if 200 <= resp.status_code < 300:
            try:
                return True, resp.json() if resp.content else None
            except ValueError:
                # Response is not JSON, but status is success
                return True, None
        
        # Handle client errors (400-499)
        elif 400 <= resp.status_code < 500:
            error_msg = resp.text[:200] if resp.text else "Client error"
            return False, {"error": error_msg, "status_code": resp.status_code}
        
        # Handle server errors (500+)
        else:
            return False, {"error": f"Server error: {resp.status_code}", "status_code": resp.status_code}
            
    except requests.exceptions.Timeout:
        return False, {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "Connection error - check network"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Request failed: {str(e)}"}


def run_migration(simulate=False):
    """
    Main migration workflow.
    
    Processes all MXF files in source directory:
    1. Validates filename format
    2. Extracts metadata from filename
    3. Parses optional XML sidecar
    4. Creates asset in ScorePlay
    
    Args:
        simulate: If True, shows detailed metadata output
    """
    mode = "SIMULATION MODE" if simulate else "LIVE MODE"
    print(f"ScorePlay Agent Active | FDE Layer: Dalet-Connector | {mode}")
    
    if not SOURCE.exists():
        print(f"Error: Source directory not found: {SOURCE}")
        return
    
    processed = 0
    skipped = 0
    failed = 0
    
    for video in SOURCE.rglob("*.mxf"):
        # Step 1: Parse filename
        filename_metadata = parse_filename(video)
        if not filename_metadata:
            print(f"Skipping malformed filename: {video.name}")
            skipped += 1
            continue

        # Step 2: Parse XML sidecar (optional)
        xml_metadata = parse_dalet_xml(video.with_suffix('.xml'))

        # Step 3: Build API payload
        payload = create_asset_payload(video, filename_metadata, xml_metadata)

        # Step 4: Create asset via API
        success, response_data = create_scoreplay_asset(payload, simulate)
        
        if success:
            if simulate:
                print(f"Successfully ingested {video.name}")
                print(f"   Match: {filename_metadata['match_id']} | "
                      f"Player: {filename_metadata['player_id']} | "
                      f"Date: {filename_metadata['timestamp']}")
                if xml_metadata:
                    print(f"   XML Metadata: {len(xml_metadata)} fields extracted")
                    for key, value in list(xml_metadata.items())[:3]:
                        print(f"      {key}: {value}")
                    if len(xml_metadata) > 3:
                        print(f"      ... and {len(xml_metadata) - 3} more fields")
            else:
                print(f"Successfully ingested {video.name}")
            processed += 1
        else:
            error = response_data.get("error", "Unknown error") if response_data else "Unknown error"
            status = response_data.get("status_code", "") if response_data else ""
            status_str = f" (HTTP {status})" if status else ""
            print(f"Error: {video.name}{status_str} - {error}")
            failed += 1
    
    # Summary
    print(f"\nSummary: {processed} processed, {skipped} skipped, {failed} failed")

if __name__ == "__main__":
    simulate = "--simulate" in sys.argv or "-s" in sys.argv
    run_migration(simulate=simulate)