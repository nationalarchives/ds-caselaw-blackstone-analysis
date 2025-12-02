import xml_helper_functions as xf
from pathlib import Path
import pandas as pd
import csv, io

# get xml files in folder
# for each file

# Extract marked up references within the XML

# Output CSV of extracted values

base_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/"
data_base_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-data-analysis/"

xml_folder = [Path(data_base_folder, "data/xml-enriched-bucket-test/"), Path(data_base_folder, "data/xml-third-phase-enriched-bucket-test/")]
transformation_file = Path(base_folder, "data/xslt/getReferenceValues.xsl")
cache_folder = Path(base_folder,"cache")

judgment_data = xf.get_data_from_transform(xml_folder, transformation_file)

judgment_data.to_csv(Path(cache_folder, "default_enrichmented_refs.csv"), index=False)