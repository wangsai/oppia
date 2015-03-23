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


class NumberWithUnitInput(base.BaseInteraction):
    """Interaction for number with unit input."""

    name = 'Number with Unit'
    category = 'Science'
    description = (
    'Allows learners to enter integers and floating point numbers followed by standard units.')
    display_mode = base.DISPLAY_MODE_INLINE
    dependency_ids = []
    _handlers = [{
    'name': 'submit', 'obj_type': 'RealWithUnit'}]

    # _customization_arg_specs = [] # Not sure about this one yet.
