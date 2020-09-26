  const isFormValid = require('./../src/auth/Login/Login');
  const Login = require('./../src/auth/Login/Login');

  const login = '';
  const pass = '';
  const errorMsg = '';

  const inputLengthLimit = 30;
  const longText = '';
  var i;
  for(i = 0; i < inputLengthLimit; i++){
		longText += 'a';
  }
  console.log(longText);

test('username/email form validity Login', () => {
  expect(isFormValid({login, pass, errorMsg})).toBeFalsy();
  expect(errorMsg).stringContaining("Please enter your username or email.");

  login = longText;
  expect(isFormValid({login, pass, errorMsg})).toBeFalsy();
  expect(errorMsg).stringContaining("Please enter your username or email.");

  login = 'a';
  expect(isFormValid({login, pass, errorMsg})).toBeTruthy();
});

test('password form validity Login', () => {
  login = 'a';

  expect(isFormValid({login, pass, errorMsg})).toBeFalsy();
  expect(errorMsg).stringContaining("Please enter your password.");

  pass = longText;
  expect(isFormValid({login, pass, errorMsg})).toBeFalsy();
  expect(errorMsg).stringContaining("Please enter your password.");

  pass = 'a';
  expect(isFormValid({login, pass, errorMsg})).toBeTruthy();
});

test('Login test', () => {
  const $ = require('jquery');
  const

});