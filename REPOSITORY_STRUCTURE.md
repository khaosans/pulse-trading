# 📁 PulseTrade Repository Structure

## Best Practices Organization

```
pulse-trading/
├── README.md                    # Main entry point with demo link
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # How to contribute
├── CHANGELOG.md                 # Version history
├── .gitignore                   # Git exclusions
│
├── demo_app.py                  # Main Streamlit application ⭐
├── requirements.txt             # Python dependencies (for deployment)
├── run_demo.sh                  # Quick launch script
│
├── docs/                        # All documentation
│   ├── README.md               # Documentation index
│   ├── DEPLOYMENT.md           # How to deploy live
│   ├── PROJECT_OVERVIEW.md     # Project summary
│   │
│   ├── demo/                   # Demo-specific guides
│   │   ├── QUICK_START.md
│   │   ├── EMOTION_TRACKER_GUIDE.md
│   │   ├── QA_REPORT.md
│   │   └── ...
│   │
│   ├── marketing/              # Marketing materials
│   │   ├── presentations/
│   │   ├── surveys/
│   │   └── financial/
│   │
│   └── archive/                # Old/deprecated files
│
├── assets/                     # Static assets
│   ├── images/
│   │   └── logo.svg
│   └── icons/
│
├── presentation/               # Original HTML presentation
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── .streamlit/                 # Streamlit configuration
    └── config.toml
```

## File Purposes

### Root Level (Only Essential Files)
- `README.md` - First thing people see
- `demo_app.py` - Main application
- `requirements.txt` - For Streamlit Cloud deployment
- `run_demo.sh` - Easy local launch
- Configuration files (`.gitignore`, `package.json`)

### docs/
- All documentation organized by category
- `demo/` - Demo usage guides
- `marketing/` - Marketing plan and materials
- `archive/` - Old files (not deleted for history)

### assets/
- Images, logos, icons
- No code, only static files

### presentation/
- Original HTML presentation
- Separated from main demo

## Why This Structure?

✅ **Clear Entry Point**: README.md tells you everything
✅ **Separation of Concerns**: Code, docs, assets separated
✅ **Easy Navigation**: Logical folder hierarchy
✅ **Deployment Ready**: Root files optimized for Streamlit Cloud
✅ **Professional**: Follows industry standards
✅ **Maintainable**: Easy to find and update files

## For Developers

### To Run Demo:
```bash
./run_demo.sh
# or
streamlit run demo_app.py
```

### To Deploy:
See `docs/DEPLOYMENT.md`

### To Contribute:
See `CONTRIBUTING.md`

---

**Maintained by**: PulseTrade Team (BADM 520 Fall 2025)
