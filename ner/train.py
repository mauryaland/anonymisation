# coding: utf8

# https://github.com/explosion/spacy/blob/master/examples/training/train_ner.py
# https://github.com/explosion/spaCy/issues/1530
# https://spacy.io/usage/linguistic-features#named-entities


import spacy
from spacy.matcher import PhraseMatcher
from tqdm import tqdm

from generate_trainset.extract_header_values import parse_xml_header
from generate_trainset.extract_node_values import get_paragraph_from_file
from generate_trainset.generate_names import get_list_of_items_to_search, get_company_names
from generate_trainset.normalize_offset import normalize_offsets
from ner.training_function import train_model
from resources.config_provider import get_config_default

config_training = get_config_default()
xml_train_path = config_training["xml_train_path"]
model_dir_path = config_training["model_dir_path"]
n_iter = int(config_training["number_iterations"])
batch_size = int(config_training["batch_size"])
dropout_rate = float(config_training["dropout_rate"])

TRAIN_DATA = get_paragraph_from_file(path=xml_train_path,
                                     keep_paragraph_without_annotation=True)
TRAIN_DATA = TRAIN_DATA[0:1000]
case_header_content = parse_xml_header(path=xml_train_path)

nlp = spacy.blank('fr')
current_case_paragraphs = list()
current_case_offsets = list()
current_items_to_find = None
previous_case_id = None
current_item_header = None
matcher = None
doc_annotated = list()

with tqdm(total=len(TRAIN_DATA)) as progress_bar:
    for current_case_id, xml_paragraph, xml_extracted_text, xml_offset in TRAIN_DATA[0:100]:
        # when we change of legal case, apply matcher to each paragraph of the previous case
        if current_case_id != previous_case_id:
            if len(current_case_paragraphs) > 0:
                for current_paragraph, current_xml_offset in zip(current_case_paragraphs, current_case_offsets):
                    current_parag_as_doc = nlp(current_paragraph)
                    matcher_offset = [(current_parag_as_doc[start_word_index:end_word_index].start_char,
                                       current_parag_as_doc[start_word_index:end_word_index].end_char,
                                       nlp.vocab.strings[match_id])
                                      for match_id, start_word_index, end_word_index in matcher(current_parag_as_doc)]
                    company_names_offset = get_company_names(current_paragraph)
                    if len(matcher_offset) + len(current_xml_offset) + len(company_names_offset) > 0:
                        if len(current_xml_offset) > 0:
                            all_match = matcher_offset + current_xml_offset + company_names_offset
                        else:
                            all_match = matcher_offset + company_names_offset
                        normalized_offsets = normalize_offsets(all_match)
                        doc_annotated.append((current_paragraph, {'entities': normalized_offsets}))
            # init element specific to the current legal case
            current_case_paragraphs.clear()
            current_case_offsets.clear()
            previous_case_id = current_case_id
            current_item_header = case_header_content[current_case_id]
            current_items_to_find = get_list_of_items_to_search(current_item_header)
            matcher = PhraseMatcher(nlp.tokenizer.vocab, max_length=10)
            for type_span, text_span in current_items_to_find:
                try:
                    matcher.add(type_span, None, nlp(text_span))
                except:
                    pass
        progress_bar.update()
        current_case_paragraphs.append(xml_paragraph)
        current_case_offsets.append(xml_offset)

# for text, annot in doc_annotated:
#     start, end, type = annot[0]
#     print(start, end, "|", text[start:end], "|", type)


train_model(data=doc_annotated,
            folder_to_save_model=model_dir_path,
            n_iter=n_iter,
            batch_size=batch_size,
            dropout_rate=dropout_rate)
