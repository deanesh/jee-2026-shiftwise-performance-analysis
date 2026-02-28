# src/analysis.py

import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_shift_averages(df_dict: dict) -> pd.DataFrame:
    """
    Compute average marks per shift for each subject.
    """
    logger.info("Calculating shift-wise subject averages.")

    try:
        subject_avgs = {}

        for subject in ["Maths", "Physics", "Chemistry"]:
            logger.debug(f"Computing averages for {subject}")
            subject_avgs[subject] = (
                df_dict[subject]
                .groupby('Shift')['Marks']
                .mean()
            )

        avg_df = pd.DataFrame(subject_avgs).sort_index()

        logger.info("Shift averages calculated successfully.")
        logger.debug(f"Average DataFrame shape: {avg_df.shape}")

        return avg_df

    except Exception as e:
        logger.exception(f"Error while calculating shift averages: {e}")
        raise


def rank_shift_difficulty(avg_df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank shifts by difficulty (lower average marks = harder shift).
    """
    logger.info("Ranking shifts by difficulty.")

    try:
        avg_df = avg_df.copy()
        avg_df['Total_Avg'] = avg_df.sum(axis=1)

        # Lower total average = higher difficulty
        avg_df['Difficulty_Rank'] = (
            avg_df['Total_Avg']
            .rank(method='min', ascending=True)
            .astype(int)
        )

        logger.info("Shift difficulty ranking completed.")
        logger.debug(f"Ranked DataFrame shape: {avg_df.shape}")

        return avg_df[['Total_Avg', 'Difficulty_Rank']]

    except Exception as e:
        logger.exception(f"Error while ranking shift difficulty: {e}")
        raise


def chapter_question_summary(df_questions: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize chapter-wise question frequency across all shifts.
    """
    logger.info("Generating chapter-wise question summary.")

    try:
        df = df_questions.copy()
        shift_cols = [col for col in df.columns if 'Shift' in col]

        for col in shift_cols:
            df[col + "_Pct"] = (
                df[col] / df['Total-Questions-Per-Shift'] * 100
            )

        logger.info("Chapter question summary generated successfully.")
        logger.debug(f"Chapter summary shape: {df.shape}")

        return df

    except Exception as e:
        logger.exception(f"Error while generating chapter summary: {e}")
        raise


def predict_marks_for_percentile(df: pd.DataFrame, target_percentile: float) -> dict:
    """
    Simple prediction: return min, max, mean marks for a target percentile.
    """
    logger.info(f"Predicting marks for percentile: {target_percentile}")

    try:
        df_sub = df[df['Percentile'] == target_percentile]

        if df_sub.empty:
            logger.warning(f"No data found for percentile {target_percentile}")
            return {"min": None, "max": None, "mean": None}

        marks_min = df_sub['Marks'].min()
        marks_max = df_sub['Marks'].max()
        marks_mean = df_sub['Marks'].mean()

        logger.info(f"Prediction complete for percentile {target_percentile}")
        logger.debug(
            f"Prediction values -> Min: {marks_min}, Max: {marks_max}, Mean: {marks_mean}"
        )

        return {
            "min": marks_min,
            "max": marks_max,
            "mean": marks_mean
        }

    except Exception as e:
        logger.exception(f"Error while predicting marks: {e}")
        raise