# ScorePlay Migration Agent
## FC Test United - Forward Deployed Engineer Solution

Python migration agent for ingesting MXF video files into ScorePlay with metadata extraction from filenames and optional XML sidecar files.

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
- `docs/Documentation.md` - Complete technical and usage documentation

### Part 3: Customer Handover Note
📄 **`docs/Handover.md`**  
Complete customer handover documentation including:
- Custom Glue components (Dalet Connector, Quiescence Heuristic)
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
    ├── Documentation.md                    # Part 2: Code & usage docs
    ├── Handover.md                        # Part 3: Handover
    └── AI-Ideas.md                        # Part 4: Enhancements
```

---

## Getting Started

See **[docs/Documentation.md](docs/Documentation.md)** for:
- Installation and configuration
- Usage examples
- Code reference
- Troubleshooting guide

---

## Support

**FDE**: Thomas Chauvel  
**API Docs**: https://developer.scoreplay.io/
