# gui/app.py

import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ==============================
# Add project root to sys.path
# ==============================
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.logger import get_logger
from gui.model.fetch_data import DataService
from gui.model.preprocess import PreprocessService

logger = get_logger(__name__)

# ==============================
# Initialize services
# ==============================
data_service = DataService()
data_service.load_all()
data_service.run_analysis()

st.set_page_config(
    page_title="JEE 2026 Shift Performance Dashboard",
    layout="wide"
)
st.title("📊 JEE 2026 Shiftwise Performance Dashboard")

# ==============================
# Sidebar controls
# ==============================
# difficulty_levels = ["Easy", "Moderate", "Tough", "Toughest"]
# selected_difficulty = st.sidebar.multiselect(
#    "Select Difficulty Level(s)", difficulty_levels, default=difficulty_levels
# )
# subject_options = ["Overall", "Maths", "Physics", "Chemistry"]
# selected_subject = st.sidebar.selectbox("Select Subject for Prediction", subject_options)


# ==============================
# Preprocess tables
# ==============================
rank_df_ui = PreprocessService.prepare_shift_table(data_service.rank_df)
shift_avg_ui = PreprocessService.subject_summary_table(data_service.shift_avg_df)
volatility_ui = PreprocessService.volatility_table(data_service.shift_volatility())
# filtered_rank_df = rank_df_ui[rank_df_ui["Difficulty_Level"].isin(selected_difficulty)]

# ==============================
# Styling for Top-3 Gold/Silver/Bronze
# ==============================
def style_top3(df):
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
    
    def highlight_top3(row):
        return [f'background-color: {colors[i]}' if i < 3 else '' for i in range(len(row))]
    
    return (
        df.style
          .apply(highlight_top3, axis=0)
          .set_properties(**{
              "font-size": "12px",
              "text-align": "center",
              "padding": "3px 6px"
          })
    )

# ==============================
# 1️⃣ Top-3 Overall Shifts
# ==============================
st.subheader("🏆 Top-3 Shifts (Overall Difficulty)")
top3_total = rank_df_ui.sort_values("Total_Avg").head(3)
st.dataframe(style_top3(top3_total[["Shift", "Total_Avg", "Difficulty_Level"]]), height=160)

# ==============================
# 2️⃣ Top-3 Shifts per Subject (Little Granular)
# ==============================
subjects = ["Maths", "Physics", "Chemistry"]
cols = st.columns(3)
for col, subj in zip(cols, subjects):
    col.subheader(f"🥇 Top-3 {subj} Shifts")
    top3_subj = shift_avg_ui.sort_values(subj).head(3)
    col.dataframe(style_top3(top3_subj[["Shift", subj]]), height=140)

# ==============================
# 3️⃣ Top-3 Chapters per Subject (More Granular)
# ==============================
chapter_top3 = {}  # For highlights and bar graph
cols = st.columns(3)
for col, subj in zip(cols, subjects):
    col.subheader(f"📚 Top-3 {subj} Chapters (High Probability)")
    subj_df = data_service.chapter_summary_df[data_service.chapter_summary_df["Subject"] == subj].copy()
    shift_pct_cols = [c for c in subj_df.columns if "_Pct" in c]
    subj_df["Total_Percent"] = subj_df[shift_pct_cols].sum(axis=1)
    top3_chapters = subj_df.sort_values("Total_Percent", ascending=False).head(3)
    chapter_top3[subj] = top3_chapters
    col.dataframe(style_top3(top3_chapters[["Chapter Name", "Total_Percent"]]), height=140)


# ==============================
# Dashboard Summary / Highlights
# ==============================
st.markdown("---")
st.subheader("💡 Key Insights / Highlights")
st.markdown(
    f"""
    - 🥇 Top-3 Overall Shifts: {', '.join(top3_total['Shift'].tolist())}  
    - 📌 Most Challenging Subject Shifts: {', '.join([shift_avg_ui.sort_values(s).head(1)['Shift'].values[0] for s in subjects])}  
    - 📚 Focus on Top Chapters:  
        - Maths: {', '.join(chapter_top3['Maths']['Chapter Name'].tolist())}  
        - Physics: {', '.join(chapter_top3['Physics']['Chapter Name'].tolist())}  
        - Chemistry: {', '.join(chapter_top3['Chemistry']['Chapter Name'].tolist())}  
    """
)
st.markdown("💡 Gold / Silver / Bronze highlights indicate top-3 priority for study.")