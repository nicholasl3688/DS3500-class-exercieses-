import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug("DataFrame shape: %s", df.shape)
    print(f"Shape: {df.shape}")
    print(df.head())
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    logger.debug("Duplicates: %d rows before, %d rows after", before, len(df))
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)
    df = df.dropna()
    logger.debug("Missing values: %d rows before, %d rows after", before, len(df))
    return df



def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.
    new = value.strip().lower()
    new = re.sub(r"\s+", ' ', new)
    return new


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    pass
    if column not in df.columns:
        logger.error(f"Column: {column} not in column list")
        raise ValueError
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr
    before = len(df)
    df = df[(df[column] >= lower) & (df[column] <= upper)]
    logger.debug(
        "IQR bounds for %s: lower=%.2f, upper=%.2f, removed %d rows",
        column, lower, upper, before - len(df),
    )
    return df


