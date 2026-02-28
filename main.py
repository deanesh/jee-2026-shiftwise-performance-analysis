# main.py

from utils.logger import get_logger
from pipeline.pipeline import JEEAnalysisPipeline

logger = get_logger(__name__)


def main():
    logger.info("Application started.")

    try:
        pipeline = JEEAnalysisPipeline(data_dir="data")

        # We only run computation + logs.
        # No plot saving. No display.
        pipeline.run(generate_plots=False)

        logger.info("Application finished successfully.")

    except Exception as e:
        logger.exception(f"Application crashed: {e}")
        raise


if __name__ == "__main__":
    main()
