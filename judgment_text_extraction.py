import xml_helper_functions as xf
from pathlib import Path
import pandas as pd

# get xml files in folder
# for each file
# parse the xml to extract the text sections as defined by the parser (The text in each span or span + sibling if sibling is not a span), and the related eId and paragraph number if the spans are descendants of numbered paragraphs
# output a csv of extracted data

base_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/"
data_base_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-data-analysis/"

xml_folder = [Path(data_base_folder, "data/xml-enriched-bucket-test/")]
transformation_file = Path(base_folder, "data/xslt/getComponentValues.xsl")
cache_folder = Path(base_folder,"cache")


judgment_data = xf.get_data_from_transform(xml_folder, transformation_file)
print(judgment_data)

judgment_data.to_csv(Path(cache_folder, "extracted_text.csv"), index=False)
print("Saving csv to " + str(Path(cache_folder, "extracted_text.csv")))





