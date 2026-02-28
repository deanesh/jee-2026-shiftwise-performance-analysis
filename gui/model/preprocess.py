# app/model/preprocess.py

import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

# Map numeric Difficulty_Rank to human-readable levels
DIFFICULTY_MAPPING = {
    1: "Toughest",
    2: "Tough",
    3: "Moderate",
    4: "Easy"
}


class PreprocessService:

    @staticmethod
    def prepare_shift_table(rank_df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare rank table for UI with Difficulty_Level labels.
        
        Parameters:
        -----------
        rank_df : pd.DataFrame
            DataFrame containing shifts with 'Difficulty_Rank' and 'Total_Avg'
        
        Returns:
        --------
        pd.DataFrame
            Shift table with added 'Difficulty_Level' column
        """
        df = rank_df.copy()
        df["Total_Avg"] = df["Total_Avg"].round(2)

        # Map difficulty rank to labels
        if "Difficulty_Rank" in df.columns:
            df["Difficulty_Level"] = df["Difficulty_Rank"].map(DIFFICULTY_MAPPING)
            df["Difficulty_Level"] = df["Difficulty_Level"].str.capitalize()
        else:
            logger.warning("'Difficulty_Rank' column not found. Creating default 'Difficulty_Level'.")
            df["Difficulty_Level"] = "Unknown"

        df.reset_index(inplace=True)
        df.rename(columns={"index": "Shift"}, inplace=True)

        logger.info("Shift table prepared for UI.")
        return df

    @staticmethod
    def subject_summary_table(shift_avg_df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare subject-wise average marks table for heatmap display.

        Parameters:
        -----------
        shift_avg_df : pd.DataFrame
            DataFrame with average marks per shift per subject
        
        Returns:
        --------
        pd.DataFrame
            Rounded average marks ready for heatmap
        """
        df = shift_avg_df.copy()
        for col in ["Maths", "Physics", "Chemistry"]:
            if col in df.columns:
                df[col] = df[col].round(2)
        df.reset_index(inplace=True)
        logger.info("Subject-wise averages table prepared for UI.")
        return df

    @staticmethod
    def volatility_table(shift_vol_df) -> pd.DataFrame:
        """
        Prepare shift-wise volatility (std dev of marks) for UI.

        Parameters:
        -----------
        shift_vol_df : pd.DataFrame or pd.Series
            Std dev of marks per shift
        
        Returns:
        --------
        pd.DataFrame
            Rounded volatility table ready for bar chart
        """
        # Convert Series to DataFrame if needed
        if isinstance(shift_vol_df, pd.Series):
            df = shift_vol_df.to_frame(name="Std_Deviation")
        else:
            df = shift_vol_df.copy()
            if "Std_Deviation" not in df.columns:
                df = df.rename(columns={df.columns[0]: "Std_Deviation"})

        df["Std_Deviation"] = df["Std_Deviation"].round(2)
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Shift"}, inplace=True)

        logger.info("Shift volatility table prepared for UI.")
        return df