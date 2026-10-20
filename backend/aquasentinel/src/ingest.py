import pandas as pd
import numpy as np
import logging
import os
from typing import Optional, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Expected core columns for normalization (can be adjusted based on actual data)
EXPECTED_COLUMNS_MAPPING = {
    'station': ['station_name', 'site_name', 'station', 'site'],
    'district': ['district_name', 'district'],
    'state': ['state_name', 'state'],
    'date': ['date', 'collection_date', 'year', 'data_acquisition_time'],
    'lat': ['latitude', 'lat'],
    'lon': ['longitude', 'lon', 'long'],
    'ph': ['potential_of_hydrogen_ph', 'ph'],
    'ec': ['electric_conductivity_scm', 'ec'],
    'tds': ['total_dissolved_solids_mgl', 'tds'],
    'fluoride': ['fluoride_mgl', 'fluoride'],
    'nitrate': ['nitrate_n_mgnl', 'nitrate'],
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes dataframe column names: lowercase, strip whitespace, replace spaces with underscores.
    """
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True)
    return df

def standardize_core_columns(df: pd.DataFrame, file_type: str) -> pd.DataFrame:
    """
    Attempts to rename columns to standard names based on the EXPECTED_COLUMNS_MAPPING.
    """
    rename_dict = {}
    for standard_col, alternatives in EXPECTED_COLUMNS_MAPPING.items():
        if standard_col not in df.columns:
            for alt in alternatives:
                if alt in df.columns:
                    rename_dict[alt] = standard_col
                    break
    
    if rename_dict:
        df = df.rename(columns=rename_dict)
    
    # Ensure all core identifier columns exist, even if as empty/NaN to prevent join errors
    core_cols = ['station', 'district', 'state', 'date', 'lat', 'lon']
    for col in core_cols:
        if col not in df.columns:
            logging.warning(f"Core column '{col}' missing in {file_type} data. Adding as empty.")
            df[col] = np.nan
            
    return df

def ingest_cgwb_file(filepath: str, file_type: str, state_code: str) -> Optional[pd.DataFrame]:
    """
    Loads a single CGWB CSV file defensively.
    
    Args:
        filepath: Path to the CSV file.
        file_type: 'chemical', 'physical', or 'levels'
        state_code: State identifier (e.g., 'mh', 'ap')
        
    Returns:
        Normalized DataFrame or None if loading fails.
    """
    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}")
        return None
        
    try:
        # Load CSV defensively, ignoring bad lines if any
        df = pd.read_csv(filepath, on_bad_lines='skip', low_memory=False)
        original_shape = df.shape
        
        df = normalize_columns(df)
        df = standardize_core_columns(df, file_type)
        
        # Add metadata for provenance
        df['source_state'] = state_code
        df['source_type'] = file_type
        
        logging.info(f"Ingested {file_type}_{state_code}: {original_shape[0]} rows, {original_shape[1]} columns.")
        return df
        
    except Exception as e:
        logging.error(f"Error reading {filepath}: {str(e)}")
        return None

def ingest_all_states(data_dir: str, file_type: str, states: list[str]) -> pd.DataFrame:
    """
    Ingests files for a specific type across multiple states and concatenates them.
    """
    dfs = []
    for state in states:
        filepath = os.path.join(data_dir, f"{file_type}_{state}.csv")
        df = ingest_cgwb_file(filepath, file_type, state)
        if df is not None and not df.empty:
            dfs.append(df)
            
    if not dfs:
        logging.error(f"No valid data loaded for type '{file_type}' across any state.")
        return pd.DataFrame()
        
    combined_df = pd.concat(dfs, ignore_index=True)
    logging.info(f"Successfully concatenated {file_type} data: {combined_df.shape[0]} total rows.")
    return combined_df
