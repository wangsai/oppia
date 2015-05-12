// Copyright 2014 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


/**
 * Directive for the NumberWithUnitInput interaction.
 *
 * IMPORTANT NOTE: The naming convention for customization args that are passed
 * into the directive is: the name of the parameter, followed by 'With',
 * followed by the name of the arg.
 */

oppia.directive('oppiaInteractiveNumberWithUnitInput', [function() {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'interaction/NumberWithUnitInput',
    controller: ['$scope', '$attrs', function($scope, $attrs) {
      $scope.labelForFocusTarget = $attrs.labelForFocusTarget || null;

      $scope.NUMBER_WITH_UNIT_INPUT_FORM_SCHEMA = {
        type: 'unicode',
        ui_config: {}
      };

      $scope.preprocess = function(unprocessedAnswer) {
        var preprocessedAnswer = unprocessedAnswer.replace(/\s/g, '').replace(",", "");
        return preprocessedAnswer;
      }

      $scope.postprocess = function(answer, parsedAnswer) {
        var processedAnswer = {'raw': answer, 'parsed': parsedAnswer}
        return processedAnswer;
      }

      $scope.submitAnswer = function(answer) {
        if (answer) {
          var strippedAnswer = $scope.preprocess(answer);
          var parsedAnswer = numberWithUnitInputParser.parse(strippedAnswer);
          var processedAnswer = $scope.postprocess(answer, parsedAnswer);

          $scope.$parent.$parent.submitAnswer(parsedAnswer, 'submit');
        }
      }
    }]
  }
}]);

oppia.directive('oppiaResponseNumberWithUnitInput', ['oppiaHtmlEscaper', function(oppiaHtmlEscaper) {
  return {
    scope: {},
    templateUrl: 'response/NumberWithUnitInput',
    controller: ['$scope', '$attrs', function($scope, $attrs) {
      $scope.answer = oppiaHtmlEscaper.escapedJsonToObj($attrs.answer);
    }]
  }
}]);