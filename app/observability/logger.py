from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    enqueue=True,
)

def log_query(question: str):
    logger.info(f"User Query: {question}")

def log_ingestion(filename: str, chunks: int):
    logger.info(f"Ingested file={filename}, chunks={chunks}")

def log_error(error: Exception):
    logger.error(str(error))
