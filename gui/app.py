# gui/app.py
import sys
from pathlib import Path
import pandas as pd
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
# Preprocess tables
# ==============================
rank_df_ui = PreprocessService.prepare_shift_table(data_service.rank_df)
shift_avg_ui = PreprocessService.subject_summary_table(data_service.shift_avg_df)
volatility_ui = PreprocessService.volatility_table(data_service.shift_volatility())

classified_df = data_service.classify_shifts()
overall_table = classified_df[["Total_Avg", "Difficulty_Level"]].round(2).reset_index()
overall_table.rename(columns={"index": "Shift"}, inplace=True)
overall_table = overall_table[["Shift", "Total_Avg", "Difficulty_Level"]]

chapter_top3 = {}
for subj in ["Maths", "Physics", "Chemistry"]:
    subj_df = data_service.chapter_summary_df[data_service.chapter_summary_df["Subject"] == subj].copy()
    shift_pct_cols = [c for c in subj_df.columns if "_Pct" in c]
    subj_df["Total_Percent"] = subj_df[shift_pct_cols].sum(axis=1)
    chapter_top3[subj] = subj_df.sort_values("Total_Percent", ascending=False).head(3).reset_index(drop=True)

# ==============================
# Sidebar navigation
# ==============================
st.sidebar.markdown("## 📂 Navigation")
tab = st.sidebar.radio(
    "Select a view",
    options=["📊 Overall", "🔢 Maths", "⚛️ Physics", "🧪 Chemistry"],
    index=0,
)
selected_tab = tab.split(" ")[1] if " " in tab else tab
st.markdown("---")

# ==============================
# Helper: style dataframe with colored headers
# ==============================
def style_dataframe(df):
    return df.style.set_table_styles([
        {'selector': 'thead th',
         'props': 'background-color: #4CAF50; color: white; font-weight: bold;'}
    ]).hide(axis="index")

# ==============================
# Display top-3 chapters (Lesson + Percent)
# ==============================
def display_top3_chapters(subj):
    df_top3 = chapter_top3[subj][["Chapter Name", "Total_Percent"]].copy()
    df_top3["Total_Percent"] = df_top3["Total_Percent"].map(lambda x: f"{x:.2f}%")
    # Use styled dataframe for green headers
    st.dataframe(style_dataframe(df_top3), use_container_width=True)

# ==============================
# Tab content
# ==============================
if selected_tab == "Overall":
    df = overall_table.sort_values("Total_Avg").reset_index(drop=True)
    df.index = df.index + 1
    st.dataframe(style_dataframe(df), use_container_width=True)

elif selected_tab in ["Maths", "Physics", "Chemistry"]:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader(f"📉 {selected_tab} Shift Difficulty")
        df_diff = shift_avg_ui[["Shift", selected_tab]].sort_values(selected_tab).reset_index(drop=True)
        df_diff.rename(columns={selected_tab: "Marks"}, inplace=True)
        df_diff.index = df_diff.index + 1
        st.dataframe(style_dataframe(df_diff), use_container_width=True)
    with col2:
        st.subheader(f"🏆 Top 3 {selected_tab} Chapters")
        display_top3_chapters(selected_tab)