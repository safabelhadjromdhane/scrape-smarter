import pandas as pd
from pathlib import Path
import json
import csv
from typing import Union, Dict, List
from src.utils.logger import setup_logger

logger = setup_logger("file_utils")

def save_to_csv(data: Union[pd.DataFrame, List[Dict]], 
               file_path: str, 
               mode: str = "w") -> None:
    """
    Save data to CSV with automatic directory creation.
    
    Args:
        data: DataFrame or list of dictionaries
        file_path: Output file path
        mode: Write mode ('w' for overwrite, 'a' for append)
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, mode=mode, index=False, header=mode=="w")
        else:
            with open(path, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                if mode == "w":
                    writer.writeheader()
                writer.writerows(data)
                
        logger.info(f"Saved data to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {e}")
        raise

def load_scraped_data(file_path: str) -> pd.DataFrame:
    """
    Load scraped data from CSV/JSON with validation.
    
    Args:
        file_path: Path to data file
        
    Returns:
        Loaded DataFrame
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError
    
    try:
        if path.suffix == ".csv":
            return pd.read_csv(path)
        elif path.suffix == ".json":
            return pd.read_json(path)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise

def save_metadata(metadata: Dict, file_path: str) -> None:
    """Save scraping metadata (e.g., last run timestamp)"""
    try:
        with open(file_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save metadata: {e}")

# Example usage:
if __name__ == "__main__":
    test_data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    save_to_csv(test_data, "data/test_output.csv")