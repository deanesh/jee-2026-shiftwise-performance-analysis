# pipeline/pipeline.py

from utils.logger import get_logger
from src.data_loader import load_percentile_data, load_question_data
from src.analysis import (
    calculate_shift_averages,
    rank_shift_difficulty,
    chapter_question_summary,
)
from src.plots import (
    plot_shift_averages,
    plot_shift_difficulty,
    plot_chapter_distribution,
    plot_percentile_vs_marks,
)

logger = get_logger(__name__)


class JEEAnalysisPipeline:
    """
    End-to-end execution pipeline (no file outputs).
    Only runs computation + plots (display optional) + logging.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

        self.percentile_data = None
        self.question_data = None
        self.shift_avg_df = None
        self.rank_df = None
        self.chapter_summary_df = None

        logger.info("JEEAnalysisPipeline initialized.")
        logger.debug(f"Data directory set to: {self.data_dir}")

    # -------------------------
    # DATA LOADING
    # -------------------------

    def load_data(self):
        logger.info("Step 1: Loading datasets.")

        self.percentile_data = load_percentile_data(self.data_dir)
        self.question_data = load_question_data(self.data_dir)

        logger.info("Datasets loaded successfully.")

    # -------------------------
    # ANALYSIS
    # -------------------------

    def run_analysis(self):
        logger.info("Step 2: Running core analysis.")

        self.shift_avg_df = calculate_shift_averages(self.percentile_data)
        self.rank_df = rank_shift_difficulty(self.shift_avg_df)
        self.chapter_summary_df = chapter_question_summary(self.question_data)

        logger.info("Core analysis completed successfully.")

    # -------------------------
    # OPTIONAL VISUALIZATION
    # -------------------------

    def generate_plots(self, show: bool = False):
        """
        Generate plots without saving them.
        By default, plots are not displayed (show=False).
        """
        logger.info("Step 3: Generating plots (no file saving).")

        # Shift averages
        plot_shift_averages(self.shift_avg_df, save_path=None, show=show)

        # Difficulty ranking
        plot_shift_difficulty(self.rank_df, save_path=None, show=show)

        # Example: Chapter distribution (Maths, first shift column)
        shift_cols = [col for col in self.question_data.columns if "Shift" in col]
        if shift_cols:
            plot_chapter_distribution(
                self.question_data,
                subject="Maths",
                shift_column=shift_cols[0],
                save_path=None,
                show=show
            )

        # Percentile vs Marks (Overall)
        plot_percentile_vs_marks(
            self.percentile_data["Overall"],
            subject="Overall",
            save_path=None,
            show=show
        )

        logger.info("Plot generation completed (no files saved).")

    # -------------------------
    # FULL PIPELINE
    # -------------------------

    def run(self, generate_plots: bool = False):
        """
        Execute full pipeline.
        By default, plots are not generated (since GUI & notebook handle visuals).
        """
        logger.info("Starting full JEE Analysis pipeline.")

        try:
            self.load_data()
            self.run_analysis()

            if generate_plots:
                self.generate_plots(show=False)

            logger.info("Pipeline executed successfully.")

        except Exception as e:
            logger.exception(f"Pipeline execution failed: {e}")
            raise