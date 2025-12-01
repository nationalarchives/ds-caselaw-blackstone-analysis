import xml_helper_functions as xf
from pathlib import Path
import pandas as pd
import csv, io

# get xml files in folder
# for each file
# parse the xml to extract the text sections as defined by the parser (The text in each span or span + sibling if sibling is not a span), and the related eId and paragraph number if the spans are descendants of numbered paragraphs
# output a csv of extracted data

xml_folder = ["C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-data-analysis/data/xml-enriched-bucket-test/"]

transformation_filename = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/data/xslt/getComponentValues.xsl"



files_for_parsing = xf.get_filenames(xml_folder)

temp_list = []

for path, xml_file in files_for_parsing:

    values = xf.parse_file(Path(path), xml_file, transformation_filename)

    temp_df = pd.read_table(io.StringIO(str(values)), delimiter="\|\@\|", quoting=csv.QUOTE_NONE, engine="python")
    temp_df['file'] = xml_file
    temp_df['folder'] = path

    temp_list.append(temp_df)

judgments = pd.concat(temp_list, axis=0, ignore_index=True)







