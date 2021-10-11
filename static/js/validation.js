var firstname = false
var email = false
var confirm_pass = false
var password = false
var lastname = false
var username = false


function checkvalidation() {
    if (firstname && email && password && confirm_pass && lastname && username) {
        $('#submit-btn').removeAttr('disabled');
    } else {
        $('#submit-btn').attr('disabled', true);
    }
}

function checkname() {
    var name = $('#firstname').val();
    var valid;
    var pattern = /^[a-zA-Z-()]+(\s+[-a-zA-Z-()]+)*$/;
    if (name == "") {
        valid = "required field";
        firstname = false;
    } else if (name.match(pattern) && name.length <= 2) {
        valid = "please enter atleast 3 letter";
        firstname = false;
    } else if (name.match(pattern)) {
        valid = "";
        firstname = true;
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        firstname = false
    } else {
        firstname = false;
        valid = "characters only";
    }
    $('#check1').html(valid);
}

function checklastname() {
    var name = $('#lastname').val();
    var valid;
    var pattern = /^[a-zA-Z-()]+(\s+[-a-zA-Z-()]+)*$/;
    if (name == "") {
        valid = "required field";
        lastname = false;
    } else if (name.match(pattern) && name.length < 3) {
        valid = "please enter atleast 3 letter";
        lastname = false;
    } else if (name.match(pattern)) {
        valid = "";
        lastname = true;
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        lastname = false
    } else {
        lastname = false;
        valid = "characters only";
    }
    $('#check5').html(valid);
}

function checkemail() {
    var mail = $('#emailfield').val();
    var valid
    var pattern = /^[^]+@[^]+\.[a-z]{2,3}$/
    if (mail == "") {
        valid = "required field"
        email = false
    } else if (mail.match(pattern)) {
        valid = ""
        email = true
    } else {
        email = false
        valid = "please enter valid email"
    }
    $('#check2').html(valid);
}

function checkmess() {
    var msg = $('#passwordfield').val();
    var valid
    if (msg == "") {
        valid = "required field"
        password = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        password = false
    } else {
        valid = ""
        password = true
    }
    $('#check3').html(valid);
}

function checkmess1() {
    var msg = $('#passwordfield').val();
    var msg1 = $('#passwordfield1').val();
    var valid
    if (msg != msg1) {
        valid = "passwords doesn't match"
        confirm_pass = false
    } else {
        valid = ""
        confirm_pass = true
    }
    $('#check4').html(valid);
}

function checkusername() {
    var msg = $('#username').val();
    var valid
    if (msg.length < 5) {
        valid = "atleast 5 character"
        username = false
    } else {
        valid = ""
        username = true
    }
    $('#check6').html(valid);
}
$('#firstname').keyup(function() {
    checkname();
    checkvalidation()
});
$('#lastname').keyup(function() {
    checklastname();
    checkvalidation()
});

$('#emailfield').keyup(function() {
    checkemail();
    checkvalidation()
});
$('#passwordfield').keyup(function() {
    checkmess();
    checkvalidation()
});
$('#passwordfield1').keyup(function() {
    checkmess1();
    checkvalidation()
});
$('#username').keyup(function() {
    checkusername();
    checkvalidation()
});

$('#submitbtn').click(function() {
    checklastname()
    checkname()
    checkusername()
    checkemail()
    checkmess()
});


//address