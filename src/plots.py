# src/plots.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

sns.set(style="whitegrid")


def plot_shift_averages(
    avg_df: pd.DataFrame,
    save_path: str = None,
    show: bool = True
) -> None:
    """
    Plot subject-wise average marks per shift.

    Parameters:
    -----------
    avg_df : pd.DataFrame
        Output from calculate_shift_averages()
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot
    """
    logger.info("Starting plot: Shift-wise subject averages")

    try:
        plt.figure(figsize=(10, 6))

        for subject in avg_df.columns:
            logger.debug(f"Plotting line for subject: {subject}")
            plt.plot(avg_df.index, avg_df[subject], marker='o', label=subject)

        plt.title("Shift-wise Average Marks (Subject-wise)")
        plt.xlabel("Shift")
        plt.ylabel("Average Marks")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300)
            logger.info(f"Shift averages plot saved to {save_path}")

        if show:
            plt.show()

        plt.close()
        logger.info("Shift-wise subject averages plot completed successfully.")

    except Exception as e:
        logger.exception(f"Error while plotting shift averages: {e}")
        raise


def plot_shift_difficulty(
    ranked_df: pd.DataFrame,
    save_path: str = None,
    show: bool = True
) -> None:
    """
    Plot total average marks per shift (difficulty visualization).
    """
    logger.info("Starting plot: Shift difficulty ranking")

    try:
        plt.figure(figsize=(10, 6))

        ranked_df = ranked_df.sort_values("Difficulty_Rank")

        sns.barplot(
            x=ranked_df.index,
            y=ranked_df["Total_Avg"],
        )

        plt.title("Shift Difficulty Ranking (Lower = Harder)")
        plt.xlabel("Shift")
        plt.ylabel("Total Average Marks")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300)
            logger.info(f"Shift difficulty plot saved to {save_path}")

        if show:
            plt.show()

        plt.close()
        logger.info("Shift difficulty plot completed successfully.")

    except Exception as e:
        logger.exception(f"Error while plotting shift difficulty: {e}")
        raise


def plot_chapter_distribution(
    df: pd.DataFrame,
    subject: str,
    shift_column: str,
    top_n: int = 10,
    save_path: str = None,
    show: bool = True
) -> None:
    """
    Plot top N chapters by question count for a given subject and shift.
    """
    logger.info(
        f"Starting chapter distribution plot | Subject: {subject} | Shift: {shift_column}"
    )

    try:
        df_sub = df[df["Subject"] == subject]

        if df_sub.empty:
            logger.warning(f"No data found for subject: {subject}")
            return

        df_top = (
            df_sub.sort_values(shift_column, ascending=False)
            .head(top_n)
        )

        logger.debug(f"Top {top_n} chapters selected for plotting.")

        plt.figure(figsize=(10, 6))

        sns.barplot(
            data=df_top,
            y="Chapter Name",
            x=shift_column,
        )

        plt.title(f"Top {top_n} Chapters - {subject} ({shift_column})")
        plt.xlabel("Number of Questions")
        plt.ylabel("Chapter")
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300)
            logger.info(f"Chapter distribution plot saved to {save_path}")

        if show:
            plt.show()

        plt.close()
        logger.info("Chapter distribution plot completed successfully.")

    except Exception as e:
        logger.exception(f"Error while plotting chapter distribution: {e}")
        raise


def plot_percentile_vs_marks(
    df: pd.DataFrame,
    subject: str = "Overall",
    save_path: str = None,
    show: bool = True
) -> None:
    """
    Plot percentile vs marks curve for a subject.
    """
    logger.info(f"Starting percentile vs marks plot | Subject: {subject}")

    try:
        df_sub = df.copy()

        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=df_sub,
            x="Percentile",
            y="Marks",
            hue="Shift",
            marker="o"
        )

        plt.title(f"{subject} - Percentile vs Marks")
        plt.xlabel("Percentile")
        plt.ylabel("Marks")
        plt.legend(title="Shift", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300)
            logger.info(f"Percentile vs Marks plot saved to {save_path}")

        if show:
            plt.show()

        plt.close()
        logger.info("Percentile vs marks plot completed successfully.")

    except Exception as e:
        logger.exception(f"Error while plotting percentile vs marks: {e}")
        raise