describe('numberWithUnitInputParser', function() {
  var parsedExpression = function(expressionString) {
    return numberWithUnitInputParser.parse(expressionString);
  };

  it('should match integers and units', function() {
    expect(parsedExpression('5km^2')).toEqual({
      "number": 5,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    });
  });

  it('should match floating point numbers and units', function() {
    expect(parsedExpression('0.5km^2')).toEqual({
      "number": .5,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    })
  });

  it('should match floating point numbers with no starting zero', function() {
    expect(parsedExpression('.5km^2')).toEqual({
      "number": .5,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    })
  });

  it('should handle negative numbers', function() {
    expect(parsedExpression('-500km^2')).toEqual({
      "number": -500,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    })
  });

  it('should handle trailing zeros after the decimal', function() {
    expect(parsedExpression('10.00km^2')).toEqual({
      "number": 10.00,
      "units": [
        {
          "unit": "km",
          "exponent": 2
        }
      ]
    })
  });

  it('should give an exponent of 1 to units without listed exponents', function() {
    expect(parsedExpression('5km')).toEqual({
      "number": 5,
      "units": [
        {
          "unit": "km",
          "exponent": 1
        }
      ]
    })
  });

  it('should handle negative exponents', function() {
    expect(parsedExpression('.5km^-2')).toEqual({
      "number": .5,
      "units": [
        {
          "unit": "km",
          "exponent": -2
        }
      ]
    })
  });

  it('should not allow negative numbers behind the decimal', function() {
    var errorMessageForNegNumbers = 'Expected [0-9] but "-" found.';
    expect(function() {parsedExpression('.-5km^2')}).toThrow(new Error(errorMessageForNegNumbers))
  });

  it('should not match units not in the list and give the right error', function() {
    var errorMessageForMadeUpUnit = 'Expected "C", "J", "N", "Pa", "V", "W", "cm", "coulomb", "coulombs", "ft", "g", "hr", "in", "inch", "inches", "joule", "joules", "kg", "km", "lb", "lbs", "m", "mg", "mile", "miles", "mm", "pa", "pascal", "qt", "qts", "s", "second", "seconds", "volt", "volts", "watt", "watts", "year", "years" or [0-9] but "d" found.';
    expect(function() { parsedExpression('.5dm^2'); }).toThrow(errorMessageForMadeUpUnit);
  });

  it('should throw an error if the unit is missing', function() {
    var errorMessageForUnit = 'Expected ".", "C", "J", "N", "Pa", "V", "W", "cm", "coulomb", "coulombs", "ft", "g", "hr", "in", "inch", "inches", "joule", "joules", "kg", "km", "lb", "lbs", "m", "mg", "mile", "miles", "mm", "pa", "pascal", "qt", "qts", "s", "second", "seconds", "volt", "volts", "watt", "watts", "year", "years" or [0-9] but end of input found.'
    expect(function() { parsedExpression('5'); }).toThrow(errorMessageForUnit);
  });

  it('should throw an error if the number is missing', function() {
    var errorMessageForNumber = 'Expected "-", "." or [0-9] but "k" found.';
    expect(function() { parsedExpression('km'); }).toThrow(errorMessageForNumber);
  });
});