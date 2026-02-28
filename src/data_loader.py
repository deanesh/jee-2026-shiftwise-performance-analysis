# src/data_loader.py

import pandas as pd
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


def load_percentile_data(data_folder: str) -> dict:
    """
    Load percentile CSV files for Overall and individual subjects.
    """
    logger.info("Starting to load percentile data.")
    data_folder = Path(data_folder)

    files = {
        "Overall":   data_folder / "JEE-Mains-2026-Jan-Percentile-Summary.csv",
        "Maths":     data_folder / "JEE-Mains-2026-Jan-Maths-Percentile-Summary.csv",
        "Physics":   data_folder / "JEE-Mains-2026-Jan-Physics-Percentile-Summary.csv",
        "Chemistry": data_folder / "JEE-Mains-2026-Jan-Chemistry-Percentile-Summary.csv"
    }

    df_dict = {}

    for subject, fpath in files.items():
        try:
            logger.info(f"Loading {subject} data from {fpath}")
            
            if not fpath.exists():
                logger.error(f"File not found: {fpath}")
                raise FileNotFoundError(f"{fpath} does not exist.")

            df = pd.read_csv(fpath, encoding='utf-8-sig')
            df.columns = df.columns.str.strip()

            logger.debug(f"{subject} raw shape: {df.shape}")

            # Melt wide-format to long-format for all shift columns
            shift_cols = [col for col in df.columns if 'Shift' in col]
            logger.debug(f"{subject} shift columns detected: {shift_cols}")

            df_melted = df.melt(
                id_vars=['Percentile', 'Exam-Total-Marks'],
                value_vars=shift_cols,
                var_name='Shift',
                value_name='Marks'
            )

            df_melted = df_melted.dropna(subset=['Marks']).reset_index(drop=True)
            df_melted['Marks'] = pd.to_numeric(df_melted['Marks'], errors='coerce')
            df_melted.rename(columns={'Exam-Total-Marks': 'Exam_Total'}, inplace=True)

            # Clean shift names
            df_melted['Shift'] = (
                df_melted['Shift']
                .str.replace('-Marks', '', regex=False)
                .str.replace('-', ' ')
                .str.replace('Jan ', 'Jan-', regex=False)
            )

            logger.info(f"{subject} processed successfully. Final shape: {df_melted.shape}")
            df_dict[subject] = df_melted

        except Exception as e:
            logger.exception(f"Error while processing {subject}: {e}")
            raise

    logger.info("Completed loading all percentile datasets.")
    return df_dict


def load_question_data(data_folder: str) -> pd.DataFrame:
    """
    Load chapter-wise questions summary CSV.
    """
    logger.info("Starting to load question summary data.")

    try:
        fpath = Path(data_folder) / "JEE-Mains-2026-Jan-Questions-Summary.csv"

        if not fpath.exists():
            logger.error(f"File not found: {fpath}")
            raise FileNotFoundError(f"{fpath} does not exist.")

        df = pd.read_csv(fpath, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()

        logger.debug(f"Question data raw shape: {df.shape}")

        # Convert numeric columns to int
        shift_cols = [col for col in df.columns if 'Shift' in col]
        total_cols = ['Total', 'Total-Questions-Per-Shift']

        for col in shift_cols + total_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        logger.info("Question summary data loaded and cleaned successfully.")
        return df

    except Exception as e:
        logger.exception(f"Error while loading question summary data: {e}")
        raise