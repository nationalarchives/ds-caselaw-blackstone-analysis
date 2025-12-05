import xml_helper_functions as xf
import pandas as pd
from pathlib import Path

# Read in CSVs of extraction from specified models
# Compare the extracted values with the default extractions

# Verify if the extracted links are valid links


csv_folder = [Path("C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/cache/")]
files_for_parsing = xf.get_filenames(csv_folder, "csv")

for path, file in files_for_parsing:

    print(file)

    if "_enrichmented_refs.csv" in file:
        df = pd.read_csv(Path(path, file))

        values = df.groupby(['folder', 'filename', 'type']).size().reset_index(name='counts')
        print(values)