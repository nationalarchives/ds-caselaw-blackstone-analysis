import spacy, re
from pathlib import Path
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS
import pandas as pd


def segment_judgment(input_folder, output_dir, booknlp_data_folder = ""):

    nlp = spacy.load("en_blackstone_proto")

    # remove the default spaCy sentencizer from the model pipeline
    if "sentencizer" in nlp.pipe_names:
        nlp.remove_pipe('sentencizer')


    # add the Blackstone sentence_segmenter to the pipeline before the parser
    sentence_segmenter = SentenceSegmenter(nlp.vocab, CITATION_PATTERNS)
    nlp.add_pipe(sentence_segmenter, before="parser")


    for file in Path(input_folder).glob("*_body.txt"):  
        judgement_id = Path(file).stem

        with open(file, "r", encoding='utf-8') as rf:
            text = rf.read().replace('“','"').replace('”','"').replace("’", "'")
            doc = nlp(text)

            #for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

            with open(Path(output_dir, judgement_id + "_blackstone.tokens"), "w", encoding='utf-8') as wf:
                word_num = 0            
                line_num = 0

                data_dict = {"sentence_ID":[], "word":[]}

                #wf.write("Token ID \t Sentence ID \t Token in Sentence ID \t Text \t Lemma \t POS \t Tag \t Dep \t Shape \t Alpha \t Stop \n")
                wf.write("token_ID_within_document | sentence_ID | token_ID_within_sentence | Word | Lemma | POS | Tag | Dep | Shape | Alpha | Stop \n")

                for line in doc.sents:
                    word_num_in_sentence = 0
                    #line_length = len(line)
                    #print(line)

                    for sen_token in line:                    
                        for token in doc[word_num:word_num+1]:
                            #print(str(word_num) + ", " + str(line_num) + ", " +  str(word_num_in_sentence) + ", " + token.text)
                            #wf.write(str(word_num) + "\t" + str(line_num) + "\t" +  str(word_num_in_sentence) + "\t" + token.text + "\t" + token.lemma_ + "\t" + token.pos_ + "\t" + token.tag_ + "\t" + token.dep_ + "\t" + token.shape_ + "\t" + str(token.is_alpha) + "\t" + str(token.is_stop) + "\n")
                            wf.write(str(word_num) + "|" + str(line_num) + "|" +  str(word_num_in_sentence) + "|" + token.text + "|" + token.lemma_ + "|" + token.pos_ + "|" + token.tag_ + "|" + token.dep_ + "|" + token.shape_ + "|" + str(token.is_alpha) + "|" + str(token.is_stop) + "\n")
                            data_dict["sentence_ID"].append(str(line_num))
                            data_dict["word"].append(token.text)

                            if sen_token.text != token.text:
                                print("Warning! Text mismatch on word num " + str(word_num) + " in line " + str(line_num) + ": " + sen_token + " - " + token.text)

                            word_num += 1
                            word_num_in_sentence += 1

                    line_num += 1

        if booknlp_data_folder != "":
            combine_with_booknlp(booknlp_data_folder, judgement_id, data_dict)


            '''
            with open(Path(output_dir, judgement_id + ".csv"), "w", encoding='utf-8') as wf:
                line_num = 0
                for line in doc.sents:
                    wf.write(str(line_num) + '|' + line.text + '\n')
                    line_num += 1
                
        '''

def combine_with_booknlp(booknlp_data_folder, judgement_id, blackstone_data):
    
    booknlp_data_path = Path(booknlp_data_folder, 'cache', judgement_id+"_lines.csv")
    print("Loading values from csv for " + judgement_id)
    booknlp_df = pd.read_csv(booknlp_data_path)


    booknlp_tokens = booknlp_df["word"].to_list()

    booknlp_length = len(booknlp_tokens)
    blackstone_length = len(blackstone_data["word"])

    blackstone_offset = 0
    blackstone_token = blackstone_data["word"][0]
    compared_blackstone_data = {"sentence_ID":[], "word":[]}


    print("Length booknlp:" + str(booknlp_length) + ", length blackstone: " + str(blackstone_length))
    print(booknlp_tokens[-1] + ", " + booknlp_tokens[-1])

    for token_index, booknlp_token in enumerate(booknlp_tokens):
            #if not(bool(re.fullmatch(booknlp_token,  blackstone_token))):

            #print("booknlp: [" + blackstone_token + "] - blackstone: [" + blackstone_token + "] (offset:" + str(blackstone_offset) + ")")
        
        compared_blackstone_data["sentence_ID"].append(blackstone_data["sentence_ID"][token_index + blackstone_offset])

        if booknlp_token != blackstone_token:    

            booknlp_token_length = len(booknlp_token)
            blackstone_token_length = len(blackstone_token)
            print("Mismatch found at " + str(token_index) +  " - booknlp: [" + booknlp_token + "] - blackstone: [" + blackstone_token + "]")
            #print("booknlp_token_length: " + str(booknlp_token_length) + " blackstone_token_length: " + str(blackstone_token_length))

            if booknlp_token_length > blackstone_token_length:
                print("merge blackstone tokens until they match the booknlp token")
                

                while booknlp_token_length > blackstone_token_length:
                    blackstone_offset += 1
                    #print(blackstone_offset)

                    if token_index + blackstone_offset < blackstone_length:
                        blackstone_token = blackstone_token + blackstone_data["word"][token_index + blackstone_offset]
                        #print("New token: " + blackstone_token)
                        blackstone_token_length = len(blackstone_token)
                    else:
                        break
                
                if (token_index + 1 + blackstone_offset) < blackstone_length:
                    next_blackstone_token = blackstone_data["word"][token_index + 1 + blackstone_offset]
                else:
                    next_blackstone_token = ""

            else:
                print("split blackstone token to match booknlp token")
                #print("Before: " + blackstone_token)
                next_blackstone_token = blackstone_token[booknlp_token_length:]
                #print("Next: " + next_blackstone_token)
                blackstone_token = blackstone_token[:booknlp_token_length]
                #print("After: " + blackstone_token)
                blackstone_offset = blackstone_offset - 1               
                

            print("Changed to - booknlp: [" + blackstone_token + "] - blackstone: [" + blackstone_token + "] (offset:" + str(blackstone_offset) + ")" + " next blackstone token: [" + next_blackstone_token + "]")
            
            compared_blackstone_data["word"].append(blackstone_token)
            blackstone_token = next_blackstone_token
        else:
            compared_blackstone_data["word"].append(blackstone_token)

            if (token_index + 1 + blackstone_offset) < blackstone_length:
                blackstone_token = blackstone_data["word"][token_index + 1 + blackstone_offset]
            else:
                blackstone_token = ""

    booknlp_df["blackstone_sentence_ID"] = compared_blackstone_data["sentence_ID"]

    booknlp_df.to_csv(Path(booknlp_data_folder, 'cache', judgement_id+"_blackstone.csv"))

    #booknlp_df[["sentence_ID", "blackstone_sentence_ID"]].to_csv("C:/Users/flawrence/Documents/Projects/FCL/Research Area/blackstone/data/sentence_compare.csv")


if __name__ == '__main__':

    input_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-data-analysis/data/extracted_text/test"
    booknlp_data_folder = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/booknlp/data"
    output_dir = "C:/Users/flawrence/Documents/Projects/FCL/Research Area/ds-caselaw-blackstone-analysis/data"

    segment_judgment(input_folder, output_dir, booknlp_data_folder)