describe('numberWithUnitInput', function() {
  var $httpBackend, $templateCache;
  var elt, scope, ctrlScope;

  beforeEach(module('oppia'));
  beforeEach(module('directiveTemplates'));
  beforeEach(inject(function($compile, _$templateCache_, $rootScope) {
    $templateCache = _$templateCache_;
    var templatesHtml = $templateCache.get(
      'extensions/interactions/NumberWithUnitInput/NumberWithUnitInput.html');
    $compile(templatesHtml)($rootScope);
    $rootScope.$digest();
  }));

  beforeEach(inject(function($compile, $rootScope, _$httpBackend_) {
    $httpBackend = _$httpBackend_;

    var TAG_NAME = 'oppia-interactive-number-with-unit-input';
    scope = $rootScope.$new();
    elt = angular.element('<' + TAG_NAME + '></' + TAG_NAME + '>');
    $compile(elt)(scope);
    scope.$digest();
    ctrlScope = elt.isolateScope();
  }));

  afterEach(function() {
    scope.$apply();
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('loads the template', function() {
    expect(elt.html()).toContain('row number-with-unit-container');
  });

  describe('preprocess', function() {
    it('gets rid of white spaces and commas', function() {
      expect(ctrlScope.preprocess('5,000 km^2  ')).toBe('5000km^2')
    });
  });

  describe('postprocess', function() {
    it('builds the whole schema from parts', function() {
      var answer = "5 km^2";
      var parsedAnswer = {
      "number": 5,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    };

      expect(ctrlScope.postprocess(answer, parsedAnswer)).toEqual({
        'raw': answer,
        'parsed': parsedAnswer
      });
    });
  });
});