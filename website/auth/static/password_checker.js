
// Returns true if the passwords meet the necessary requirements, false otherwise.
function checkPassword() {
    let passwordInput1 = document.getElementById("password1");
    let passwordInput2 = document.getElementById("password2");

    if (checkEqual(passwordInput1.value, passwordInput2.value) && checkLength(passwordInput1.value) && checkDigits(passwordInput1.value) && checkLowerCase(passwordInput1.value) && checkUpperCase(passwordInput1.value)) {
        return true;
    }

    // The passwords are not valid: clear password fields, focus on pw1 and return false.
    passwordInput1.value = "";
    passwordInput2.value = "";
    passwordInput1.focus();
    return false;
}


// Returns true if the string inputs, false (and alert) otherwise.
function checkEqual(pw1, pw2) {
    if (pw1 == pw2) {
        return true;
    }
    alert("Passswords do not match.");
    return false;
}


// Returns true if the password's length is >= 6 characters, false (and alert) otherwise.
function checkLength(pw) {
    if (pw.length > 5) {
        return true;
    }
    alert("Password must be at least 6 characters long.");
    return false;
}


// Returns true if the password contains at least one numeric digit, flase (and alert) otherwise.
function checkDigits(pw) {
    if (pw.search(/\d/) > -1) { // Uses regular expressions to search for digits
        return true;
    }
    alert("Passwords must contain at least one numeric character.");
    return false;
}


// Returns true if the password contains at least one lower-case character, false (and alert) otherwise.
function checkLowerCase(pw) {
    if (pw.toUpperCase() != pw) {
        return true;
    }
    alert("Password must contain at least one lower-case character.");
    return false;
}


// Returns true if the password contains at least one upper-case character, false (and alert) otherwise.
function checkUpperCase(pw) {
    if (pw.toLowerCase() != pw) {
        return true;
    }
    alert("Password must contain at least one upper-case character.");
    return false;
}