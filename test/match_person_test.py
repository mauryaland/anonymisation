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

from match_text.match_natural_persons import get_partie_pers


def test_match_person():
    text1 = "- Toto Popo né le 30"
    assert get_partie_pers(text1) == [(2, 11, "PERS")]
    text2 = "- Toto Popo, né le 30"
    assert get_partie_pers(text2) == [(2, 11, "PERS")]
    text3 = "- Vanessa née le 1er octobre 1987 a TOULON (Var),"
    assert get_partie_pers(text3) == [(2, 9, "PERS")]
    text4 = "•   Eugène né le 23 mars 1997 à Grenoble ( 38"
    assert get_partie_pers(text4) == [(4, 10, "PERS")]
    text5 = "Elle ajoute que les sommes réclamées ne seraient éventuellement " \
            "dues que pour les années 2016 et suivantes"
    assert get_partie_pers(text5) == []
    text6 = "Je vois les consorts Toto BOBO au loin."
    assert get_partie_pers(text6) == [(21, 30, "PERS")]
    text7 = "Ne serait-ce pas le Docteur Toto BOBO au loin."
    assert get_partie_pers(text7) == [(28, 37, "PERS")]
    text8 = "C'est Madame Titi Toto épouse POPO PIPI"
    assert get_partie_pers(text8) == [(13, 39, "PERS")]
    text9 = "C'est Madame Titi épouse POPO qui est là"
    assert get_partie_pers(text9) == [(13, 29, "PERS")]
    text10 = "C'est Madame TOTO épouse Popo"
    assert get_partie_pers(text10) == [(13, 29, "PERS")]
    text11 = 'Par déclaration du 24 janvier 2011 Dominique FELLMANN et Marie Reine PIERRE épouse FELLMANN ont '
    assert get_partie_pers(text11) == [(57, 91, "PERS")]
