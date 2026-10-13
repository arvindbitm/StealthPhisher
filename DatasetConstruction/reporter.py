import numpy as np
import pandas as pd
import os

def save_to_csv(MASTER, output_file_path):
    # Replace NaN values with 0
    MASTER = MASTER.replace(np.nan, 0)
    MASTER = MASTER.reset_index(drop=True)

    # Convert columns to int64 where possible
    for CL in MASTER.columns:
        try:
            MASTER[CL] = MASTER[CL].apply(np.int64)
        except:
            pass

    # Check if the file exists to determine whether to write the header
    file_exists = os.path.exists(output_file_path)
    
    # Save MASTER DataFrame to CSV
    with open(output_file_path, 'a', newline='') as f:
        MASTER.to_csv(f, index=False, header=not file_exists)