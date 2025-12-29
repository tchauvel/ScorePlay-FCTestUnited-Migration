"""
Dalet XML Connector

Parses Dalet XML sidecar files to extract metadata.
Handles the standard Dalet <titles><title> structure.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

# Map Dalet XML tags to readable metadata keys
DALET_MAPPING = {
    'Match_Competition': 'competition',
    'Match_OM_Stadium': 'stadium',
    'Match_OM_Season': 'season',
    'Duration': 'duration_ms',
    'Match_OM_Score': 'match_score',
    'Match_OM_Category': 'category',
    'LOGGING_TEAM': 'team',
    'LOGGING_SECOND_TEAM': 'opponent_team',
    'LOGGING_EVENT': 'event',
    'LOGGING_LEAGUE': 'league',
    'TitleId': 'title_id',
    'Title': 'title'
}


def parse_dalet_xml(xml_path: Path) -> dict:
    """
    Parse Dalet XML sidecar file and extract metadata.
    
    Handles the standard Dalet format: <titles><title>...</title></titles>
    Extracts all fields from the title element and applies field mappings.
    
    Args:
        xml_path: Path to XML sidecar file
    
    Returns:
        Dictionary of metadata (empty dict if file doesn't exist or parsing fails)
    """
    if not xml_path.exists():
        return {}

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        metadata = {}
        
        # Handle Dalet XML format (titles/title structure)
        if root.tag == 'titles':
            title_elem = root.find('title')
            if title_elem is not None:
                # Extract all fields from title element
                for child in title_elem:
                    text = (child.text or "").strip()
                    if text:
                        # Use mapped name if available, otherwise use original tag
                        key = DALET_MAPPING.get(child.tag, child.tag)
                        metadata[key] = text
        else:
            # For other XML structures, extract mapped fields globally
            for node in root.iter():
                if node.tag in DALET_MAPPING and (node.text or "").strip():
                    metadata[DALET_MAPPING[node.tag]] = (node.text or "").strip()
        
        return metadata
    except ET.ParseError as e:
        # XML parsing error - file exists but is malformed
        return {}
    except Exception as e:
        # Other errors (permissions, etc.) - fail silently for optional file
        return {}