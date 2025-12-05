from lxml import etree as etree
from pathlib import Path
import shutil, csv, io, os
import pandas as pd


def get_filenames(data_paths, suffix="xml"):
    ''' Function gets the list of files of the specified type in the data folder

        Returns list of filenames
    '''

    filenames = set()
    
    for data_path in data_paths:
        
        if data_path.exists():
            for file in Path(data_path).glob("*." + suffix):  
                base_filename = Path(file).stem
                #print(base_filename)
                
                if base_filename[0] == "-":
                    base_filename_trimmed = base_filename[1:]
                    if base_filename_trimmed in filenames:
                        filenames.remove(base_filename_trimmed)
                
                if "-" + base_filename not in filenames:
                    filenames.add((data_path, base_filename + "." + suffix))
        else:
            print("Warning: " + data_path + " not found!")
    
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


def get_data_from_transform(xml_folder, transformation_file, filter=[]):
    ''' Function runs the specified XSLT transformation on all the XML files in the specified folder.
    '''

    files_for_parsing = get_filenames(xml_folder)

    #print(files_for_parsing)

    if len(filter) > 0:
        #need to deal with files with optional hyphens in front because want -eat-2022-2 and eat-2022-2 to match
        files_for_parsing = [file_tuple for file_tuple in files_for_parsing if file_tuple[1] in filter]

        if len(files_for_parsing) < 1:
            print("No files found that match specified filters (" + str(filter) + ")")

    #print(files_for_parsing)

    temp_list = []

    for path, xml_file in files_for_parsing:

        values = parse_file(Path(path), xml_file, transformation_file)

        #print(values)

        temp_df = pd.read_table(io.StringIO(str(values)), delimiter="\|\@\|", quoting=csv.QUOTE_NONE, engine="python")
        temp_df['file'] = xml_file

        base_filename = Path(xml_file).stem            
        if base_filename[0] == "-":
            base_filename = base_filename[1:]
        temp_df['filename'] = base_filename

        temp_df['folder'] = path

        temp_list.append(temp_df)
        #print(temp_df)

    #print(len(temp_list))

    if len(temp_list) > 1:
        combined_df = pd.concat(temp_list, axis=0, ignore_index=True)
        #print(combined_df)
        return combined_df
    elif len(temp_list) == 1:
        return temp_list[0]
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    print("Running helper functions file")