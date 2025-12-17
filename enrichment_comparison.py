import xml_helper_functions as xf
import pandas as pd
from pathlib import Path
import requests
from lxml import etree as etree

# Read in CSVs of extraction from specified models
# Compare the extracted values with the default extractions

# Verify if the extracted links are valid links

def compare_values(values, folders, type="leg"):
    #print("Legislation Comparison:")
    #leg_values = leg_values.dropna(how='all', axis=1)
    #print(leg_values.info())

    #print(values)

    columns = values.columns.values.tolist()
    comparision_dict = {}
    no_compare = ['type', 'file', 'filename', 'parent_folder', 'folder', 'position', 'eID']
    for column in columns:
        if column not in no_compare:
            comparision_dict[column + "_comparison"] = []

    link_results = []
    enrichment_source = []

    for i, row in values.iterrows():

        #value comparison
        if len(folders) == len(row['parent_folder']):
            enrichment_source.append(["All"])
        else:
            enrichment_source.append(list(row['parent_folder']))

        for column in columns:
            if column not in no_compare:
                comparision_dict[column + "_comparison"].append(match_check(row, column))
                #print(column + "_comparison: " + str(len(comparision_dict[column + "_comparison"])))

        #link check
        if len(row['href']) == 1:
            link = list(row['href'])[0]
            #print("href: " + link)
            if check_link_url(link):
                link_doc = check_url(link, type=type)
                if link_doc:
                    #print(link_doc)
                    link_results.append({link_doc})
                else:
                    link_results.append({"Error: " + link})
            else:
                link_results.append({"Not checked: " + link})
                #print("Warning!: href is '" + link + "'")
        else:
            print("Warning!: Link difference")
            link_set = ()
            for link in row['href']:
                #print("href: " + link)
                if check_link_url(link):
                    link_doc = check_url(link, type=type)
                    if link_doc:
                        link_set.add(link_doc)
                    else:
                        link_set.add("Bad URI: " + link)
                else:
                    link_set.add("Not checked: " + link)

            link_results.append(link_set)

    #print(comparision_dict)
    
    leg_enrichment_comparison = df.from_dict(comparision_dict)
    leg_enrichment_comparison['link check'] = link_results  
    leg_enrichment_comparison['source'] = enrichment_source 
    leg_enrichment_comparison['position'] = values['position']
    leg_enrichment_comparison['eID'] = values['eID']
    

    #print(values)
    return leg_enrichment_comparison

def match_check(row, colname):

    if colname == 'parent_folder':
        return row[colname]
    elif len(row[colname]) > 1:      
        return False
    else:
        return True

def check_link_url(link):
    if link and ("www.legislation.gov.uk" in link or "caselaw.nationalarchives.gov.uk" in link) :
        return True
    else:
        return False


def check_url(uri, type="leg"):
    url = uri + '/data.xml'
    response = requests.get(url)

    if response.ok:
        try: 
            tree = etree.ElementTree(etree.fromstring(response.content))
            root = tree.getroot()
            if type == "leg":
                title = root.find(".//dc:title", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})
                return(title.text)
            else:
                #print("Root: " + str(root) + " in " + url)
                citation = root.find(".//uk:cite", namespaces={"uk": "https://caselaw.nationalarchives.gov.uk/akn"})
                if citation is not None:
                    #print("Citation found in " + url)
                    return(citation.text)
                else:
                    print("Could not find citation element in " + url)
                    return(None)

        except etree.ParseError as pe:
            print("Could not parse " + url + ": " + str(pe))
            return(None)
        except AttributeError as ae:
            print("No value found at " + url + ": " + str(ae))
            return(None)

    else:
        if type == "leg":
            print("Warning!: Bad URI: " + uri)
        else:
            print("Warning!: No XML file: " + uri)
        
        return("Bad URI: " + uri)


def get_parent_folder(row):
    return Path(row['folder']).name

def get_position(row):
    return len(row['text before'])

def output_report(output_path):

    report_text = []

    #number of unique files
    number_of_files = 0
    number_of_files_text = "Number of Files processed:" + str(number_of_files)
    report_text.append(number_of_files_text)

    #number of sources of enrichment
    number_of_sources = 0
    number_of_sources_text = "Number of sources processed:" 
    report_text.append(number_of_sources_text)

    #number of files / source
    files_sources_breakdown = ""
    report_text.append(files_sources_breakdown)

    #table with column with filename, columns with number of cases for each source
    #table with column with filename, columns with number of legislation for each source


    # Documents (order by number of references)
    # Split into matched values

    # Extranious values

    # Position
    #   Table with column for Source , columns for values...



    

    with open("demofile.txt", "w") as report:
        report.writelines(report_text)



if __name__ == '__main__':

    cache_path = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/cache/"
    csv_folder = [Path(cache_path)]
    files_for_parsing = xf.get_filenames(csv_folder, "csv")

    for path, file in files_for_parsing:

        #print(file)

        if "_enrichmented_refs.csv" in file:
            df = pd.read_csv(Path(path, file), encoding='UTF-8')
            df['parent_folder'] = df.apply(get_parent_folder, axis=1)
            df['position'] = df.apply(get_position, axis=1)

            folders = set(df['parent_folder'].unique())

            #print(df[['position', 'text before', 'text after']])

            values = df.groupby(['parent_folder', 'filename', 'type']).size().reset_index(name='counts').sort_values(['type'])

            #print(values[['parent_folder', 'filename', 'type', 'counts']])
            
            case_values = df[df['type'] == 'case']
            leg_values = df[df['type'] == 'legislation']
        
            type_error_values = df[~df['type'].isin(['legislation', 'case'])]
            if not(type_error_values.empty):
                print("Warning!: Unexpected type in values " + str(type_error_values))

            filename = df['filename'].unique()[0]
            print(filename)

            if not(leg_values.empty):
                grouped_leg_values = leg_values.groupby(['position', 'eID'], as_index=False).agg(set)
                grouped_leg_values.to_csv(Path(cache_path, 'output', filename + '_leg_data.csv'), index=False, encoding='utf-8')

                leg_comparison = compare_values(grouped_leg_values, folders=folders)
                if not(leg_comparison.empty):
                    leg_comparison.to_csv(Path(cache_path, 'output', filename + '_leg_comparison.csv', index=False, encoding='utf-8'))


            if not(case_values.empty):
                grouped_case_values = case_values.groupby(['position', 'eID'], as_index=False).agg(set)
                grouped_case_values.to_csv(Path(cache_path, 'output', filename + '_case_data.csv', index=False, encoding='utf-8'))

                case_comparison = compare_values(grouped_case_values, folders=folders, type="case")
                if not(case_comparison.empty):
                    case_comparison.to_csv(Path(cache_path, 'output', filename + '_case_comparison.csv', index=False, encoding='utf-8'))
            