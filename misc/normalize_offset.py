#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import regex


def normalize_offsets(offsets: list) -> list:
    """
    Normalize the provided list of offsets by merging or removing some of them
    Takes care of priority included in the tag label (as `_1`)
    :param offsets: original offsets as list of tuples generated by pattern matching
    :return: cleaned list of tuples
    """
    sorted_offsets = sorted(offsets, key=lambda tup: (tup[0], tup[1]))
    offset_to_keep = list()
    previous_start_offset, previous_end_offset, previous_type_tag = None, None, None

    for current_start_offset, current_end_offset, current_type_tag in sorted_offsets:

        # merge tags which appear as separated but are not really
        if (previous_end_offset is not None) and (previous_end_offset + 1 >= current_start_offset):
            previous_start_offset, previous_end_offset, previous_type_tag = previous_start_offset, \
                                                                            current_end_offset, \
                                                                            tag_priority(previous_type_tag,
                                                                                         current_type_tag)

        if (previous_end_offset is not None) and (previous_end_offset < current_end_offset):
            offset_to_keep.append((previous_start_offset, previous_end_offset,
                                   remove_tag_priority_info(previous_type_tag)))

        # keep longest tags when they are one on the other
        if (previous_end_offset is not None) and (previous_end_offset >= current_end_offset):
            current_start_offset, current_end_offset, current_type_tag = previous_start_offset, \
                                                                         previous_end_offset, \
                                                                         tag_priority(previous_type_tag,
                                                                                      current_type_tag)

        # delete short offsets (1 - 2 chars)
        if current_end_offset - current_start_offset <= 2:
            current_start_offset, current_end_offset, current_type_tag = previous_start_offset, \
                                                                         previous_end_offset, \
                                                                         previous_type_tag

        previous_start_offset, previous_end_offset, previous_type_tag = (current_start_offset,
                                                                         current_end_offset,
                                                                         current_type_tag)
    if previous_start_offset is not None:
        offset_to_keep.append((previous_start_offset, previous_end_offset,
                               remove_tag_priority_info(previous_type_tag)))
    return offset_to_keep


def tag_priority(previous_tag: str, current_tag: str) -> str:
    """
    Apply some rules to decide which tag to keep when merging 2 offsets
    In particular manage tag priority indicated by _1 in tag label
    :param previous_tag: tag as a string starting the earliest (start character of the offset)
    :param current_tag: tag as a string
    :return: the selected tag
    """

    if previous_tag[-2:] == "_1":
        return previous_tag
    elif current_tag[-2:] == "_1":
        return current_tag
    else:
        # return the first seen tag otherwise
        return previous_tag


def remove_tag_priority_info(tag: str) -> str:
    """
    Remove the tag priority information
    :param tag: original tag label
    :return: tag without priority information
    """
    if tag[-2:] == "_1":
        return tag[:-2]
    return tag


def remove_spaces_included_in_offsets(text: str, offsets: list):
    """
    If offset doesn't match a word boundary its type is removed by Spacy (unknown action)
    This function removes spaces when at the start or the end of the offset, if any
    More info -> https://spacy.io/usage/linguistic-features
    Test code:
    ----
    import spacy
    from spacy.gold import GoldParse
    from spacy.tokens import Doc
    nlp = spacy.blank('fr')
    doc2 = nlp('Who is Chaka Khan popo?')
    gold2 = GoldParse(doc2, entities=[(7, 18, 'PERSON')])
    print(gold2.ner)
    ----
    :param text: original text
    :param offsets: list of original offsets for this text
    :return: list of new offsets fixed
    """
    result = list()
    for start_offset, end_offset, type_name in offsets:
        if (start_offset >= 0) and (end_offset - 1 < len(text)) and (start_offset != end_offset):
            new_start = start_offset + 1 if text[start_offset].isspace() else start_offset
            # remove 1 because the closing offset is not included in the selection in Python
            new_end = end_offset - 1 if text[end_offset - 1].isspace() else end_offset
            result.append((new_start, new_end, type_name))
    return result


pattern_to_remove = regex.compile("^\s*\\b((M|m)adame|(M|m)onsieur|Mme(\.)?|Me|société|M(\.)?)\\b\s*",
                                  flags=regex.VERSION1)


def clean_offsets_from_unwanted_words(text: str, offsets: list) -> list:
    """
    Remove some words which should not appear inside an offset (e.g.: Monsieur, Madame, etc.)
    It is possible that sometimes the offset is empty because it only contains Madame for instance.
    It has to be cleaned in a next step
    :param text: original paragraph
    :param offsets: list of already extracted offsets
    :return: cleaned offsets
    """
    result = list()
    for start_offset, end_offset, type_name in offsets:
        offset_text = text[start_offset:end_offset]
        unwanted_text_found = pattern_to_remove.match(offset_text)
        if unwanted_text_found is not None:
            found_string = unwanted_text_found.captures()[0]
            result.append((start_offset + len(found_string), end_offset, type_name))
        else:
            result.append((start_offset, end_offset, type_name))
    return result
