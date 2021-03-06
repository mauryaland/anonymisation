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

from spacy.gold import biluo_tags_from_offsets, GoldParse

no_action_bilou = None
unknown_type_name = "UNKNOWN"


def convert_bilou_with_missing_action(doc, offsets: list) -> list:
    """
    Convert unknown type token to missing value for NER
    Therefore no Loss will be applied to these tokens
    https://spacy.io/api/goldparse#biluo_tags_from_offsets
    :param doc: text tokenized by Spacy
    :param offsets: original offsets
    :return: list of BILOU types
    """
    result1 = biluo_tags_from_offsets(doc, offsets)
    return [no_action_bilou if unknown_type_name in action_bilou else action_bilou
            for action_bilou in result1]


def convert_unknown_bilou(doc, offsets: list) -> GoldParse:
    """
    Convert entity offsets to list of BILOU annotations
    and convert UNKNOWN label to Spacy missing values
    https://spacy.io/api/goldparse#biluo_tags_from_offsets
    :param doc: spacy tokenized text
    :param offsets: discovered offsets
    :return: tuple of docs and BILOU annotations
    """
    bilou_annotations = convert_bilou_with_missing_action(doc=doc, offsets=offsets)
    return GoldParse(doc, entities=bilou_annotations)


def convert_unknown_bilou_bulk(docs: list, offsets: list) -> list:
    """
    Convert list of entity offsets to list of BILOU annotations
    and convert UNKNOWN label to Spacy missing values
    https://spacy.io/api/goldparse#biluo_tags_from_offsets
    :param docs: spacy tokenized text
    :param offsets: discovered offsets
    :return: tuple of docs and GoldParse
    """
    list_of_gold_parse = list()
    for doc, current_offsets in zip(docs, offsets):
        bilou_annotations = convert_unknown_bilou(doc=doc,
                                                  offsets=current_offsets)
        list_of_gold_parse.append(bilou_annotations)
    return list_of_gold_parse
