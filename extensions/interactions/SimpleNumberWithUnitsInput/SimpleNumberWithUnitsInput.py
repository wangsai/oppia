# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwar
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from extensions.interactions import base


class SimpleNumberWithUnitsInput(base.BaseInteraction):
    """Interaction for entering numbers with units."""

    name = 'Simple Number with Units Input'
    description = 'Allows learners to enter numbers with units.'
    display_mode = base.DISPLAY_MODE_INLINE
    _dependency_ids = []
    _handlers = [{
        'name': 'submit', 'obj_type': 'NumberWithUnits'}]

    _customization_arg_specs = [{
        'name': 'unitChoices',
        'description': 'Choices for the units dropdown',
        'schema': {
            'type': 'list',
            'validators': [{
                'id': 'has_length_at_least',
                'min_value': 1,
            }],
            'items': {
                'type': 'unicode',
            },
        },
        'default_value': ['hours', 'days', 'years'],
    }]
