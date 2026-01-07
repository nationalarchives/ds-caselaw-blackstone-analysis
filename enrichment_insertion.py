from pathlib import Path
import pandas as pd
import xml_helper_functions as xf
from lxml import etree as etree

# read in spreadsheet

cache_path = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/cache/output"
data_base_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-data-analysis/"
data = []

for file in Path(cache_path).glob("*_data.csv"):  
    temp_df = pd.read_csv(Path(file), encoding='UTF-8')
    data.append(temp_df)
    

# read in XML

xml_folder =Path(data_base_folder, "data/xml-enriched-bucket-test/")



# for each line in spreadsheet add in matching node