import xml_helper_functions as xf
import pandas as pd
from pathlib import Path
import requests
from lxml import etree as etree

# Read in CSVs of extraction from specified models
# Compare the extracted values with the default extractions

# Verify if the extracted links are valid links

def compare_values(values, type="leg"):
    #print("Legislation Comparison:")
    #leg_values = leg_values.dropna(how='all', axis=1)
    #print(leg_values.info())

    #print(values)

    leg_enrichment_comparison = pd.DataFrame(index=values.index)


    columns = values.columns.values.tolist()
    comparision_dict = {}
    for column in columns:
        if column not in ['type', 'file', 'filename']:
            comparision_dict[column + "_comparison"] = []

    link_results = []

    for i, row in values.iterrows():

        #value comparison
        for column in columns:
            if column not in ['type', 'file', 'filename']:
                comparision_dict[column + "_comparison"].append(match_check(row, column))
                #print(column + "_comparison: " + str(len(comparision_dict[column + "_comparison"])))

        #link check
        if len(row['href']) == 1:
            link = list(row['href'])[0]
            if link and link != "" and link != '#':
                link_doc = check_url(link, type=type)
                if link_doc:
                    link_results.append({link_doc})
                else:
                    link_results.append({"Bad URI"})
            else:
                link_results.append({"No valid URI"})
        else:
            print("Warning!: Link difference")
            link_set = ()
            for link in row['href']:
                if link and link != "" and link != '#':
                    link_doc = check_url(link, type=type)
                    if link_doc:
                        link_set.add(link_doc)
                    else:
                        link_set.add("Bad URI")

            link_results.append(link_set)

    #print(comparision_dict)
    leg_enrichment_comparison = df.from_dict(comparision_dict)
    leg_enrichment_comparison['link check'] = link_results  

    #print(values)
    return leg_enrichment_comparison


def match_check(row, colname):
    if len(row[colname]) > 1:
        return False
    else:
        return True

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
                print("Root: " + str(root))
                citation = root.find(".//uk:cite", namespaces={"uk": "https://caselaw.nationalarchives.gov.uk/akn"})
                if citation is not None:
                    return(citation.text)
                else:
                    print("Could not find citation element in " + url)
                    return(None)

        except etree.ParseError as pe:
            print("Could not parse " + url + ": " + str(pe))
        except AttributeError as ae:
            print("No value found at " + url + ": " + str(ae))

    else:
        #print("Warning!: Bad URI: " + uri)
        return(None)




def compare_case_values(case_values):
    #print(judgment_values)
    pass



def get_parent_folder(row):
    return Path(row['folder']).name

def get_position(row):
    return len(row['text before'])

if __name__ == '__main__':

    csv_folder = [Path("C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/cache/")]
    files_for_parsing = xf.get_filenames(csv_folder, "csv")

    for path, file in files_for_parsing:

        #print(file)

        if "_enrichmented_refs.csv" in file:
            df = pd.read_csv(Path(path, file), encoding='UTF-8')
            df['parent_folder'] = df.apply(get_parent_folder, axis=1)
            df['position'] = df.apply(get_position, axis=1)

            #print(df[['position', 'text before', 'text after']])

            values = df.groupby(['parent_folder', 'filename', 'type']).size().reset_index(name='counts').sort_values(['type'])

            #print(values[['parent_folder', 'filename', 'type', 'counts']])
            
            case_values = df[df['type'] == 'case']
            leg_values = df[df['type'] == 'legislation']
        
            type_error_values = df[~df['type'].isin(['legislation', 'case'])]
            if not(type_error_values.empty):
                print("Warning!: Unexpected type in values " + str(type_error_values))

            print(df['filename'].unique()[0])
            #leg_comparison = compare_values(leg_values.groupby('position').agg(set).sort_index())
            #print(leg_comparison)


            case_comparison = compare_values(case_values.groupby('position').agg(set).sort_index(), type="case")
            print(case_comparison)
            