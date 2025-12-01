from lxml import etree as etree
from pathlib import Path
import shutil


def get_filenames(data_paths, suffix="xml"):
    ''' Function gets the list of files of the specified type in the data folder

        Returns list of filenames
    '''

    filenames = set()
    
    for data_path in data_paths:
        for file in Path(data_path).glob("*." + suffix):  
            base_filename = Path(file).stem
            print(base_filename)
            
            if base_filename[0] == "-":
                base_filename_trimmed = base_filename[1:]
                if base_filename_trimmed in filenames:
                    filenames.remove(base_filename_trimmed)
            
            if "-" + base_filename not in filenames:
                filenames.add((data_path, base_filename + "." + suffix))
    
    return filenames


def parse_file(folder, filename, transformation_filename):
    ''' Function reads the specified XML file and runs the transformations on it to extract the requested values. Returns the values.
    '''
    
    transform_file = Path("data", "xslt", transformation_filename)
    
    xml_file = Path(folder, filename) 

    try:
        tree = etree.parse(xml_file)       
    except etree.ParseError as e:
        with open("data/errors-ParsingError.txt", "a", encoding="utf-8") as myfile:
            myfile.write("Parser error in " + filename + ": " + str(e) + "\n")
        
        shutil.move(Path(folder, filename), Path(folder, "ParsingError", filename))     
    
    try: 
        transform = etree.parse(transform_file)  
    except etree.ParseError as e:
        print(e)
    
    transform = etree.XSLT(transform)  
    
    extracted_values = transform(tree)
    
    return(extracted_values)
