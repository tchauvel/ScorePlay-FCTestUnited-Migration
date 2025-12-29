# FC Test United - ScorePlay Migration Plan
## Forward Deployed Engineer: Thomas Chauvel

---

## Executive Summary

This document outlines the migration approach for FC Test United's legacy MXF video archive to ScorePlay, including both one-time migration and ongoing watchfolder setup.

**Status**: ✅ Proof of Concept Complete

---

## Current State

### Customer Assets
- **Legacy NAS**: Thousands of MXF video files
- **File Naming Convention**: `{match_id}_{player_id}_{timestamp}.mxf`
- **Optional Metadata**: XML sidecar files with additional information
- **Example**: `M1234_P5678_20240420T153000.mxf` + `M1234_P5678_20240420T153000.xml`

### ScorePlay Integration
- **Test Platform**: https://dc.scoreplay.io/
- **API Endpoint**: `POST /api/assets`
- **Authentication**: Bearer token (API key provided)

---

## Solution Architecture

### Phase 1: Metadata Ingestion Script ✅

**Deliverable**: `ScorePlay.py`

**Capabilities**:
1. **Filename Parsing**: Extracts match_id, player_id, timestamp from structured filenames
2. **XML Sidecar Support**: Automatically detects and parses optional XML metadata files
3. **State Management**: Tracks processed files to avoid duplicates and enable resumability
4. **Dual Mode Operation**:
   - **Migration Mode**: One-time processing of existing archive
   - **Watchfolder Mode**: Continuous monitoring for new files

**Key Features**:
- ✅ Resumable migration (safe to interrupt and restart)
- ✅ Error handling and logging
- ✅ File readiness checks (for watchfolder mode)
- ✅ API error recovery
- ✅ Malformed filename detection and skipping

---

## Migration Approach

### Step 1: Proof of Concept ✅ COMPLETE

**Objective**: Validate approach with sample files

**Actions Taken**:
- ✅ Developed working prototype script
- ✅ Tested filename parsing logic
- ✅ Tested XML sidecar parsing
- ✅ Validated API integration
- ✅ Confirmed state tracking works

**Results**:
- Script successfully processes files
- XML metadata extraction working
- API calls successful
- Error handling robust

### Step 2: Pre-Migration Assessment

**Recommended Actions**:

1. **File Inventory**
   ```bash
   # Count total MXF files
   find /path/to/nas -name "*.mxf" | wc -l
   
   # Count files with XML sidecars
   find /path/to/nas -name "*.mxf" -exec sh -c 'test -f "${1%.mxf}.xml" && echo "$1"' _ {} \; | wc -l
   
   # Identify malformed filenames
   find /path/to/nas -name "*.mxf" | grep -vE "M\d+_P\d+_\d{8}T\d{6}\.mxf"
   ```

2. **Sample Processing**
   - Process 100-1000 files as a test batch
   - Verify metadata accuracy in ScorePlay
   - Check API response times and error rates
   - Validate XML sidecar extraction

3. **Network & Performance Testing**
   - Measure API call latency
   - Test with various file sizes
   - Identify any rate limiting issues

### Step 3: Full Migration Execution

**Timeline Estimate**:
- **Small Archive (< 1,000 files)**: 1-2 hours
- **Medium Archive (1,000 - 10,000 files)**: 4-8 hours  
- **Large Archive (10,000+ files)**: 1-2 days

**Execution Plan**:

1. **Preparation**
   - Update `SOURCE_PATH` in script to point to NAS mount
   - Verify API credentials are correct
   - Create backup of state file location
   - Schedule during off-peak hours (if applicable)

2. **Migration Run**
   ```bash
   # Run migration mode
   python ScorePlay.py
   ```

3. **Monitoring**
   - Watch console output for errors
   - Monitor `.scoreplay_processed.json` file growth
   - Track API success/failure rates
   - Log any malformed filenames for review

4. **Validation**
   - Spot-check assets in ScorePlay portal
   - Verify metadata completeness
   - Confirm XML sidecar data is present where expected
   - Review error logs for patterns

5. **Completion**
   - Final count: Compare processed files vs. total files
   - Document any skipped files and reasons
   - Generate migration report

### Step 4: Watchfolder Deployment

**Objective**: Automatically process new files as they arrive

**Deployment Options**:

**Option A: Background Service (Recommended)**
```bash
# Create systemd service (see README.md)
sudo systemctl enable scoreplay-watchfolder
sudo systemctl start scoreplay-watchfolder
```

**Option B: Cron Job (Alternative)**
```bash
# Run every 5 minutes
*/5 * * * * /path/to/venv/bin/python /path/to/ScorePlay.py --watch
```

**Option C: Manual Monitoring**
- Run script in screen/tmux session
- Monitor logs periodically

**Monitoring & Maintenance**:
- Set up log rotation
- Monitor disk space for state file
- Alert on API failure rates > 5%
- Regular spot-checks of processed files

---

## Customer Expectations Management

### What This Solution Provides ✅

1. **Metadata Migration**
   - All filename-based metadata extracted and registered
   - XML sidecar metadata included where available
   - Assets created in ScorePlay with complete metadata

2. **Resumability**
   - Safe to interrupt and restart
   - No duplicate processing
   - Progress tracking via state file

3. **Error Handling**
   - Malformed filenames skipped with warnings
   - API errors logged but don't block processing
   - Network issues handled gracefully

4. **Ongoing Automation**
   - Watchfolder mode for new content
   - Automatic processing as files arrive
   - No manual intervention required

### What This Solution Does NOT Include ❌

1. **File Upload**
   - This script only registers metadata
   - Actual MXF file upload requires separate process
   - ScorePlay may need files uploaded to cloud storage

2. **File Validation**
   - Does not verify MXF file integrity
   - Does not check file format compliance
   - Does not validate video content

3. **File Transformation**
   - No transcoding or format conversion
   - No thumbnail generation
   - No preview creation

4. **File Management**
   - Does not delete source files
   - Does not move files after processing
   - Does not archive processed files

### Next Steps for Complete Integration

**Phase 2: File Upload** (Future)
- Implement actual file upload to ScorePlay storage
- Handle large file transfers
- Resume interrupted uploads
- Verify upload completion

**Phase 3: Validation** (Future)
- Validate MXF file integrity
- Check format compliance
- Verify video content accessibility

**Phase 4: Transformation** (Future, if needed)
- Transcode to ScorePlay-required formats
- Generate thumbnails/previews
- Extract additional metadata from video content

---

## Risk Assessment & Mitigation

### Identified Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API rate limiting | Medium | Low | Sequential processing; can add delays if needed |
| Network interruptions | Medium | Medium | Resumable state tracking; retry logic |
| Malformed filenames | Low | Medium | Skip with warning; log for review |
| XML parsing errors | Low | Low | Optional metadata; graceful degradation |
| Large archive size | Medium | High | Batch processing; progress tracking |

### Contingency Plans

1. **API Rate Limiting**
   - Add exponential backoff
   - Implement request queuing
   - Parallelize with rate limiting

2. **Network Issues**
   - State file ensures no data loss
   - Can resume from last processed file
   - Retry failed API calls

3. **Large Archive**
   - Process in batches
   - Monitor progress regularly
   - Can split across multiple runs

---

## Success Criteria

### Phase 1: Proof of Concept ✅
- [x] Script successfully processes sample files
- [x] API integration working
- [x] XML parsing functional
- [x] Error handling robust

### Phase 2: Migration (Pending)
- [ ] All valid files processed
- [ ] Metadata accuracy verified
- [ ] Error rate < 1%
- [ ] Migration completed within timeline

### Phase 3: Watchfolder (Pending)
- [ ] Service deployed and running
- [ ] New files processed automatically
- [ ] Monitoring and alerting in place
- [ ] Zero manual intervention required

---

## Timeline & Milestones

### Completed ✅
- **Week 1**: Proof of concept development
- **Week 1**: Script testing and validation

### Upcoming
- **Week 2**: Pre-migration assessment
- **Week 2**: Sample batch processing
- **Week 3**: Full migration execution
- **Week 3**: Watchfolder deployment
- **Week 4**: Validation and handoff

---

## Support & Documentation

### Documentation Provided
- ✅ `ScorePlay.py` - Main migration script
- ✅ `README.md` - User guide and technical documentation
- ✅ `MIGRATION_PLAN.md` - This document
- ✅ `requirements.txt` - Python dependencies

### API Documentation
- ScorePlay Developer Docs: https://developer.scoreplay.io/
- Test Platform: https://dc.scoreplay.io/

### Contact
- **FDE**: Thomas Chauvel
- **Customer**: FC Test United

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

### XML Sidecar Structure
```xml
<metadata>
    <match>
        <venue>...</venue>
        <competition>...</competition>
    </match>
    <player>
        <name>...</name>
        <position>...</position>
    </player>
    <recording>
        <camera>...</camera>
        <quality>...</quality>
        <duration>...</duration>
    </recording>
</metadata>
```

### API Payload Example
```json
{
  "external_id": "/absolute/path/to/file.mxf",
  "name": "M1234_P5678_20240420T153000.mxf",
  "date": "2024-04-20T15:30:00Z",
  "metadata": {
    "match_id": "M1234",
    "player_id": "P5678",
    "customer": "FC Test United",
    "match_venue": "Test Stadium",
    "player_name": "John Doe",
    ...
  }
}
```

---

**Document Version**: 1.0  
**Last Updated**: 2024-12-28  
**Status**: Proof of Concept Complete

