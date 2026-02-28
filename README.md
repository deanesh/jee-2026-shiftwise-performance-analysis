````markdown
# JEE 2026 Shiftwise Performance Dashboard

A clean Streamlit dashboard for visualizing JEE Mains 2026 shift performance and key insights.

## Features

- **Top-3 Shifts**  
  Overall & per subject (Maths, Physics, Chemistry) with Gold/Silver/Bronze highlights.  

- **Top-3 Chapters**  
  High-probability chapters per subject for focused preparation.  

- **Percentile Predictions**  
  Predict min, max, and mean marks for percentiles 90–100.  

- **Compact Layout**  
  Tables are minimized, readable, and actionable.

## Installation

```bash
git clone <repo-url>
cd jee-2026-shiftwise-performance-analysis
pip install -r requirements.txt
````

## Run Dashboard

```bash
streamlit run gui/app.py
```

Use the sidebar to select difficulty levels, subject, and percentile.

## Notes

* Gold / Silver / Bronze highlights indicate **priority ranking**.
* Percentile slider matches historical data (90–100).
* Tables are compact for clean, actionable visualization.


