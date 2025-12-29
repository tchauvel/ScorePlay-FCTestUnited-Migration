# FC Test United - Customer Handover Note
## ScorePlay Migration & Integration

**Forward Deployed Engineer**: Thomas Chauvel  
**Customer**: FC Test United  
**Date**: December 2024  
**Status**: ✅ Prototype Complete - Ready for Production Deployment

---

## Overview

We have successfully completed the migration prototype for FC Test United. The legacy NAS archive is now bridged to the ScorePlay Pulse ecosystem. Below are the operational details required for long-term account management.

---

## Custom Glue (The FDE Layer)

We developed two bespoke components to handle the club's specific technical debt:

### 1. Modular Dalet Connector

A dedicated `dalet_connector.py` module was built to parse their legacy XML sidecar files. This extracts competition details, stadium data, and event locators that standard filename parsing would miss.

**Key Features:**
- Handles Dalet XML format (`<titles><title>` structure)
- Extracts all metadata fields from XML sidecars
- Maps Dalet-specific tags to readable metadata keys
- Gracefully handles missing or malformed XML files

**Implementation:**
- Location: `dalet_connector.py`
- Reusable module for future Dalet integrations
- Extracts fields like: `Match_Competition`, `Match_OM_Stadium`, `LOGGING_TEAM`, etc.

### 2. Quiescence Ingest Heuristic

To prevent the ingestion of "growing files" from their live broadcast encoders, we implemented a custom stability check. The Agent waits for file-size stasis before triggering the upload.

**How It Works:**
- Monitors file size changes
- Waits for file to stabilize (no size changes for 2 seconds)
- Only processes files that have finished copying/writing
- Prevents partial file ingestion

**Note:** This is currently implemented in the migration script. For production watchfolder mode, this should be enhanced with configurable wait times.

---

## ScorePlay Product Features Leveraged

The deployment relies on the following core platform strengths:

### 1. Pulse Intelligent Agent

Acts as the secure, outbound-only gateway (Zero-Inbound Port policy). The migration agent connects to ScorePlay API endpoints without requiring inbound firewall rules.

**Security Benefits:**
- No open ports on customer network
- Outbound HTTPS only
- Bearer token authentication
- Secure credential management via `.env` files

### 2. Named-Capture Regex Engine

Used for Layer 1 structural metadata extraction from filenames:
- Pattern: `{match_id}_{player_id}_{timestamp}.mxf`
- Example: `M1234_P5678_20240420T153000.mxf`
- Extracts: `match_id`, `player_id`, `timestamp`

**Implementation:**
- Regex pattern: `^(?P<m>M\d+)_(?P<p>P\d+)_(?P<t>\d{8}T\d{6})$`
- Validates filename structure before processing
- Skips malformed files with clear error messages

### 3. Multi-threaded Transport

Leveraged for the Week 3-4 bulk archive transfer to maximize throughput while respecting the 200Mbps QoS cap.

**Current Implementation:**
- Sequential processing (safe for initial migration)
- Can be parallelized for bulk transfers
- Respects API rate limits
- Configurable timeout settings

---

## Residual Risks for Go-Live

### 1. NAS Performance

**Risk:** The legacy hardware showed high latency during the Pilot. We must monitor for I/O bottlenecks during the full bulk transfer.

**Mitigation:**
- Monitor API response times
- Track file processing rates
- Implement retry logic for timeout errors
- Consider batch processing during off-peak hours

**Action Items:**
- [ ] Baseline performance metrics during pilot
- [ ] Set up monitoring for I/O latency
- [ ] Define escalation thresholds

### 2. Filename Exceptions

**Risk:** Any assets not following the `M1234_P5678_20240420T153000.mxf` convention will be skipped. CS should expect a list of "orphans" for manual review.

**Current Behavior:**
- Script logs skipped files: `"Skipping malformed filename: {filename}"`
- Summary shows: `{skipped} skipped` count
- No automatic remediation

**Action Items:**
- [ ] Generate orphan file report after migration
- [ ] Review orphan files with customer
- [ ] Determine manual ingestion process for exceptions
- [ ] Consider regex pattern adjustments if needed

### 3. SRT Network Stability

**Risk:** The live stream relies on UDP Port 2000. If the club's ISP experiences significant jitter, the SRT buffer may need further tuning by the FDE team.

**Note:** This is a production streaming concern, not directly related to the migration script. However, it should be monitored during the full deployment.

**Action Items:**
- [ ] Monitor SRT stream stability during pilot
- [ ] Document network jitter incidents
- [ ] Coordinate with FDE team for buffer tuning if needed

---

## Technical Architecture

### Migration Agent Components

```
ScorePlay.py
├── Filename Parser (Layer 1)
│   └── Extracts: match_id, player_id, timestamp
├── Dalet Connector (Layer 2)
│   └── Parses XML sidecar files
├── Payload Builder
│   └── Merges filename + XML metadata
└── API Client
    └── Creates assets in ScorePlay
```

### File Structure

- `ScorePlay.py` - Main migration script
- `dalet_connector.py` - Dalet XML parser (reusable module)
- `config.py` - Configuration management
- `.env` - Environment variables (excluded from git)
- `.env.example` - Configuration template

### API Integration

**Endpoint:** `POST https://dc.scoreplay.io/api/assets`

**Payload Structure:**
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
    "stadium": "Orange Velodrome",
    ...
  }
}
```

---

## Deployment Phases

### Phase 1: Proof of Concept ✅ COMPLETE

**Status:** Successfully completed  
**Deliverables:**
- Working prototype script
- Dalet XML connector
- API integration validated
- Test platform verified

### Phase 2: Pilot Migration (Week 1-2)

**Scope:** Process sample batch (100-1000 files)  
**Objectives:**
- Validate metadata extraction accuracy
- Test API performance
- Identify edge cases
- Baseline performance metrics

**Success Criteria:**
- 95%+ successful ingestion rate
- Metadata accuracy verified
- No critical errors

### Phase 3: Bulk Archive Transfer (Week 3-4)

**Scope:** Full legacy archive migration  
**Timeline:** 1-2 days for 10,000+ files  
**Approach:**
- Multi-threaded processing
- Respect 200Mbps QoS cap
- Monitor NAS I/O performance
- Generate orphan file report

**Success Criteria:**
- All valid files processed
- Orphan files documented
- Performance within SLA

### Phase 4: Production Watchfolder (Week 5+)

**Scope:** Ongoing ingestion for new content  
**Deployment:**
- Background service (systemd/supervisor)
- Continuous monitoring
- Alerting for failures

---

## Operational Procedures

### Running the Migration

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API credentials

# Test mode (simulation)
python ScorePlay.py --simulate

# Production mode
python ScorePlay.py
```

### Monitoring

**Key Metrics:**
- Files processed per hour
- API success/failure rates
- Orphan file count
- Average processing time per file

**Logs:**
- Console output shows real-time progress
- Errors logged with file names and HTTP status codes
- Summary statistics at completion

### Troubleshooting

**Common Issues:**

1. **API Authentication Errors (401)**
   - Check `.env` file has correct `SCOREPLAY_API_KEY`
   - Verify API key hasn't expired

2. **Network Timeouts**
   - Check network connectivity
   - Increase `REQUEST_TIMEOUT` in `.env`
   - Monitor NAS I/O performance

3. **Malformed Filenames**
   - Review skipped files list
   - Determine if pattern needs adjustment
   - Document for manual processing

---

## Customer Expectations

### What This Solution Provides ✅

- ✅ Metadata extraction from filenames
- ✅ Dalet XML sidecar parsing
- ✅ Asset creation in ScorePlay
- ✅ Error handling and logging
- ✅ Simulation mode for testing

### What This Solution Does NOT Include ❌

- ❌ Actual video file upload (metadata only)
- ❌ File validation or integrity checks
- ❌ Video transcoding or transformation
- ❌ Automatic retry logic (fails fast)
- ❌ State tracking for resumability (one-time migration)

### Next Steps for Full Integration

1. **File Upload**: Separate process to upload actual MXF files to ScorePlay storage
2. **Validation**: Verify file integrity and format compliance
3. **Transcoding**: If ScorePlay requires different formats
4. **Watchfolder**: Continuous monitoring for new files (future enhancement)

---

## Support & Maintenance

### Code Repository

**GitHub:** https://github.com/tchauvel/ScorePlay

**Key Files:**
- `ScorePlay.py` - Main migration script
- `dalet_connector.py` - Dalet XML parser
- `config.py` - Configuration management
- `README.md` - Quick start guide
- `CODE_QUALITY.md` - Design decisions documentation

### Configuration

**Environment Variables** (`.env` file):
```bash
SCOREPLAY_API_BASE_URL=https://dc.scoreplay.io/api
SCOREPLAY_API_KEY=your_api_key_here
SOURCE_PATH=./videos
REQUEST_TIMEOUT=10
```

### API Documentation

- ScorePlay Developer Docs: https://developer.scoreplay.io/
- Test Platform: https://dc.scoreplay.io/

### Contact

**Forward Deployed Engineer**: Thomas Chauvel  
**Customer**: FC Test United  
**ScorePlay Support**: [Support contact information]

---

## Appendix: Technical Details

### File Naming Pattern

```
{match_id}_{player_id}_{timestamp}.mxf

Where:
- match_id: M followed by digits (e.g., M1234)
- player_id: P followed by digits (e.g., P5678)
- timestamp: YYYYMMDDTHHMMSS (e.g., 20240420T153000)
```

### Dalet XML Structure

The connector handles the standard Dalet format:
```xml
<titles>
  <title>
    <TitleId>904571</TitleId>
    <Match_Competition>Ligue 1 UberEats</Match_Competition>
    <Match_OM_Stadium>Orange Velodrome</Match_OM_Stadium>
    <LOGGING_TEAM>MARSEILLE</LOGGING_TEAM>
    ...
  </title>
</titles>
```

### Error Handling

**HTTP Status Codes:**
- `200-299`: Success (asset created)
- `400-499`: Client error (check payload/credentials)
- `500+`: Server error (retry or escalate)

**Network Errors:**
- Timeout: Increase `REQUEST_TIMEOUT` or check network
- Connection Error: Verify network connectivity
- Request Exception: Check API endpoint availability

---

**Document Version**: 2.0  
**Last Updated**: December 2024  
**Status**: Customer Handover - Production Ready
