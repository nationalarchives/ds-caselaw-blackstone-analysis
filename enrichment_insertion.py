from pathlib import Path
import pandas as pd
import shutil
#import xml_helper_functions as xf
#from lxml import etree as etree
from saxonche import PySaxonProcessor, PySaxonApiError


def saxon_transformation(xml):
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()

        document = proc.parse_xml(xml_text=xml)

        xsltproc.set_source(xdm_node=document)
        xsltproc.compile_stylesheet(stylesheet_text="")

        output2 = xsltproc.transform_to_string()
        print(output2)


def saxon_parse_file(folder, filename, transformation_filename):
    ''' Function reads the specified XML file and runs the transformations on it to extract the requested values. Returns the values.
    '''
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()

        transform_file = Path("data", "xslt", transformation_filename)       
        xml_file = Path(folder, filename) 

        try:
            tree = proc.parse_xml(xml_file_name=xml_file)       
        except PySaxonApiError as e:
            with open("data/errors-ParsingError.txt", "a", encoding="utf-8") as myfile:
                myfile.write("Parser error in " + filename + ": " + str(e) + "\n")
            
            shutil.move(Path(folder, filename), Path(folder, "ParsingError", filename))     
        
        try: 
            xsltproc.set_source(xdm_node=tree)
            transform = xsltproc.compile_stylesheet(stylesheet_file=transform_file)
        except PySaxonApiError as e:
            print(e)
               
        extracted_values = transform.transform_to_string(xdm_node=tree, encoding='utf-8')
        
        return(extracted_values)


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
