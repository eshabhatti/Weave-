  const isFormValid = require('./../src/auth/Register/Register');

  const login = '';
  const email = '';
  const pass = '';
  const pass2 = '';
  const isOverThirteen = '';
  const errorMsg = '';

  const inputLengthLimit = 30;
  const longText = '';
  var i;
  for(i = 0; i < inputLengthLimit; i++){
		longText += 'a';
  }
  console.log(longText);

test('username form validity Registration', () => {
  expect(isFormValid({login, pass, pass2, email, isOverThirteen, errorMsg})).toBeFalsy();
  expect(errorMsg).stringContaining("Please enter your username or email.");


});