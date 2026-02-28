# app/model/fetch_data.py

from utils.logger import get_logger
from src.data_loader import load_percentile_data, load_question_data
from src.analysis import (
    calculate_shift_averages,
    rank_shift_difficulty,
    chapter_question_summary,
    predict_marks_for_percentile
)

logger = get_logger(__name__)


class DataService:
    """
    Service layer for Streamlit app.
    Handles data loading + core analysis.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.percentile_data = None
        self.question_data = None
        self.shift_avg_df = None
        self.rank_df = None
        self.chapter_summary_df = None

        logger.info("DataService initialized.")

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    def load_all(self):
        """
        Load all required datasets.
        """
        logger.info("Loading all datasets for Streamlit app.")

        self.percentile_data = load_percentile_data(self.data_dir)
        self.question_data = load_question_data(self.data_dir)

        logger.info("All datasets loaded successfully.")

    # ---------------------------------------------------
    # RUN CORE ANALYSIS
    # ---------------------------------------------------

    def run_analysis(self):
        """
        Compute shift averages, rankings, chapter summaries.
        """
        logger.info("Running analysis for GUI layer.")

        self.shift_avg_df = calculate_shift_averages(self.percentile_data)
        self.rank_df = rank_shift_difficulty(self.shift_avg_df)
        self.chapter_summary_df = chapter_question_summary(self.question_data)

        logger.info("GUI analysis computation completed.")

    # ---------------------------------------------------
    # SHIFT DIFFICULTY CLASSIFICATION
    # ---------------------------------------------------

    def classify_shifts(self):
        """
        Classify shifts into Easy / Moderate / Tough / Toughest.
        """
        logger.info("Classifying shifts by difficulty.")

        df = self.rank_df.copy()
        quantiles = df["Total_Avg"].quantile([0.25, 0.5, 0.75])

        def classify(avg):
            if avg <= quantiles[0.25]:
                return "Toughest"
            elif avg <= quantiles[0.5]:
                return "Tough"
            elif avg <= quantiles[0.75]:
                return "Moderate"
            else:
                return "Easy"

        df["Difficulty_Level"] = df["Total_Avg"].apply(classify)

        logger.info("Shift classification complete.")
        return df.sort_values("Difficulty_Rank")

    # ---------------------------------------------------
    # SUBJECT-WISE TOUGHEST SHIFT
    # ---------------------------------------------------

    def subject_toughest_shift(self):
        """
        Return toughest shift per subject.
        """
        logger.info("Computing subject-wise toughest shifts.")

        result = {}

        for subject in ["Maths", "Physics", "Chemistry"]:
            result[subject] = self.shift_avg_df[subject].idxmin()

        logger.info("Subject-wise toughest shift computation complete.")
        return result

    # ---------------------------------------------------
    # SHIFT VOLATILITY
    # ---------------------------------------------------

    def shift_volatility(self):
        """
        Compute std deviation of marks across percentiles per shift.
        """
        logger.info("Computing shift volatility.")

        overall_df = self.percentile_data["Overall"]

        volatility = (
            overall_df.groupby("Shift")["Marks"]
            .std()
            .sort_values(ascending=False)
        )

        logger.info("Shift volatility calculated.")
        return volatility

    # ---------------------------------------------------
    # PERCENTILE PREDICTION
    # ---------------------------------------------------

    def get_percentile_prediction(self, subject: str, percentile: float):
        """
        Predict marks range for a given percentile.
        """
        logger.info(
            f"Predicting marks for subject={subject}, percentile={percentile}"
        )

        df = self.percentile_data.get(subject)

        if df is None:
            logger.error(f"Invalid subject requested: {subject}")
            return None

        prediction = predict_marks_for_percentile(df, percentile)

        logger.info("Prediction complete.")
        return prediction