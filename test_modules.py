# test_modules.py

from src.data_loader import load_percentile_data, load_question_data
from src.analysis import calculate_shift_averages, rank_shift_difficulty, chapter_question_summary

DATA_FOLDER = "data/"

# -------------------------------
# 1. Test Data Loader
# -------------------------------
print("Loading percentile data...")
df_percentiles = load_percentile_data(DATA_FOLDER)
for subj, df in df_percentiles.items():
    print(f"\n{subj} Percentile Data (first 5 rows):")
    print(df.head())

print("\nLoading question data...")
df_questions = load_question_data(DATA_FOLDER)
print(df_questions.head())

# -------------------------------
# 2. Test Analysis Functions
# -------------------------------
print("\nCalculating shift averages...")
avg_df = calculate_shift_averages(df_percentiles)
print(avg_df)

print("\nRanking shift difficulty...")
difficulty_df = rank_shift_difficulty(avg_df)
print(difficulty_df)

print("\nChapter-level question summary...")
chap_summary = chapter_question_summary(df_questions)
print(chap_summary.head())