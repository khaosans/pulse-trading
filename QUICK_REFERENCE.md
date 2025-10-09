# 🚀 Quick Reference Guide

## Starting the App

```bash
# Standard mode
streamlit run demo_app.py

# Debug mode (performance monitoring)
streamlit run demo_app.py -- ?debug=true

# Custom port
streamlit run demo_app.py --server.port 8501
```

## Using New Components

### Metric Cards
```python
from ui_components import render_metric_card

render_metric_card(
    label="Portfolio Value",
    value="$68,450",
    delta="+5.2%",
    delta_color="normal",  # or "inverse", "off"
    icon="💰"
)
```

### Loading States
```python
from ui_components import render_loading_state

render_loading_state("Loading market data...")
```

### Error Handling
```python
from ui_components import render_error_state
from app_enhancements import ErrorBoundary

# Method 1: Manual error display
try:
    data = fetch_data()
except Exception as e:
    render_error_state(str(e), retry_callback=fetch_data)

# Method 2: Decorator
@ErrorBoundary.wrap
def risky_operation():
    return external_api_call()
```

### Status Badges
```python
from ui_components import render_status_badge

badge = render_status_badge("CONNECTED", "success")
st.markdown(badge, unsafe_allow_html=True)
```

## Formatting Utilities

```python
from app_enhancements import (
    format_currency,
    format_percentage,
    format_large_number
)

# Currency
format_currency(68450)  # "$68,450.00"

# Percentage
format_percentage(5.23)  # "+5.23%"

# Large numbers
format_large_number(1500000)  # "1.5M"
format_large_number(2500000000)  # "2.5B"
```

## Performance Optimization

### Caching
```python
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def expensive_operation():
    return fetch_and_process_data()
```

### DataFrame Optimization
```python
from performance_config import optimize_dataframe

# Automatically sample large DataFrames
df = optimize_dataframe(large_df, max_rows=1000)
st.dataframe(df)
```

### Performance Monitoring
```python
from app_enhancements import PerformanceMonitor

monitor = PerformanceMonitor()

@monitor.track_time("data_fetch")
def fetch_data():
    return api.get_data()

# View metrics
metrics = monitor.get_metrics()
print(metrics)
```

## Accessibility

### ARIA Labels
Components automatically get ARIA labels when enhancements are enabled.

### Skip Navigation
```python
from ui_components import render_accessibility_skip_link

render_accessibility_skip_link()
```

### Keyboard Hints
```python
from app_enhancements import AccessibilityEnhancements

AccessibilityEnhancements.add_keyboard_navigation_hints()
```

## Debug Mode

Access at: `http://localhost:8501?debug=true`

### Features
- Clear all caches
- View performance metrics
- Inspect session state
- Monitor API calls

### Programmatic Access
```python
if st.session_state.get('debug_mode', False):
    st.write("Debug info:", debug_data)
```

## Configuration

### Performance Settings
```python
from performance_config import CACHE_TTL, UI_CONFIG, CHART_COLORS

# Use cache TTL constants
@st.cache_data(ttl=CACHE_TTL['live_data'])
def get_live_data():
    pass

# Use chart colors for consistency
fig.update_traces(line_color=CHART_COLORS['primary'])
```

### Breakpoints
```python
from performance_config import BREAKPOINTS

if window_width < BREAKPOINTS['tablet']:
    # Mobile layout
    pass
```

## Common Patterns

### Section Headers
```python
from ui_components import render_section_header

render_section_header(
    "Market Overview",
    subtitle="Real-time market data and analysis",
    icon="📊"
)
```

### Empty States
```python
from ui_components import render_empty_state

if len(data) == 0:
    render_empty_state(
        "No trades yet",
        icon="📭",
        action_text="Start Trading",
        action_callback=start_trading
    )
```

### Info Cards
```python
from ui_components import render_info_card

render_info_card(
    title="Trading Tip",
    content="Your calm level is optimal for trading!",
    type="success"  # or "info", "warning", "error"
)
```

## Chart Styling

```python
from ui_components import create_consistent_chart, CHART_COLORS

# Create chart with consistent styling
fig = create_consistent_chart(df, chart_type="line")

# Use consistent colors
fig.update_traces(
    line_color=CHART_COLORS['primary'],
    fillcolor=CHART_COLORS['primary_light']
)
```

## Error Checking

### No Linting Errors
```bash
# All files pass linting ✅
# Run manually if needed:
mypy live_data.py
mypy app_enhancements.py
```

## File Structure

```
Key Files:
├── demo_app.py              # Main app (enhanced)
├── app_enhancements.py      # Performance layer
├── ui_components.py         # Reusable components
├── live_data.py             # Type-safe data
├── performance_config.py    # Settings
├── optimized_styles.css     # CSS
└── OPTIMIZATION_GUIDE.md    # Full documentation
```

## Troubleshooting

### Clear Caches
```python
from app_enhancements import CacheManager

CacheManager.clear_all_caches()
```

### Check Performance
1. Enable debug mode: `?debug=true`
2. Navigate through app
3. Click "Show Performance Metrics"
4. Look for operations >1s

### Fix Styling Issues
1. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Clear browser cache
3. Restart Streamlit

## Best Practices

✅ **DO:**
- Use type hints
- Wrap risky operations with ErrorBoundary
- Use consistent components from ui_components
- Cache expensive operations
- Test keyboard navigation
- Check color contrast

❌ **DON'T:**
- Modify CSS directly in components
- Skip error handling
- Use inline styles
- Forget ARIA labels
- Ignore performance metrics
- Create duplicate components

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run demo_app.py

# Run with debug
streamlit run demo_app.py -- ?debug=true

# Type check
mypy live_data.py

# Check linting (if you have pylint)
pylint demo_app.py
```

## Support

- **Documentation**: See `OPTIMIZATION_GUIDE.md`
- **Examples**: Check `ui_components.py` docstrings
- **Performance**: Read `performance_config.py`
- **Accessibility**: Review WCAG 2.1 guidelines

---

**Last Updated**: October 9, 2025  
**Version**: 2.0.0

