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

from match_text.match_phone import get_phone_number


def test_phone_number():
    assert get_phone_number("phone: (06)-42-92 72- 29 et 01 44 23 65 89") == [(8, 25, 'PHONE_NUMBER'),
                                                                              (28, 42, 'PHONE_NUMBER')]
    assert get_phone_number("phone: (06)-42-92 72- 29 + 12") == []
    assert get_phone_number("phone: (00)-42-92 72- 29 ") == []
