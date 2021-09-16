var n = false
var e = false
var p = false
var m = false
var l = false
var us = false

function checkvalidation() {
    if (n && e && m && p && l && us) {
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
        n = false;

    } else if (name.match(pattern) && name.length <= 2) {
        valid = "please enter atleast 3 letter";
        n = false;
        checkvalidation()
    } else if (name.match(pattern)) {
        valid = "";
        n = true;
        checkvalidation()
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        n = false
        checkvalidation()
    } else {
        n = false;
        valid = "characters only";
        checkvalidation()
    }
    $('#check1').html(valid);
}

function checklastname() {
    var name = $('#lastname').val();
    var valid;
    var pattern = /^[a-zA-Z-()]+(\s+[-a-zA-Z-()]+)*$/;
    if (name == "") {
        valid = "required field";
        l = false;
        checkvalidation()
    } else if (name.match(pattern) && name.length <= 1) {
        valid = "please enter atleast 3 letter";
        l = false;
        checkvalidation()
    } else if (name.match(pattern)) {
        valid = "";
        l = true;
        checkvalidation()
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        l = false
        checkvalidation()
    } else {
        l = false;
        valid = "characters only";
        checkvalidation()
    }
    $('#check5').html(valid);
}

function checkemail() {
    var mail = $('#emailfield').val();
    var valid
    var pattern = /^[^]+@[^]+\.[a-z]{2,3}$/
    if (mail == "") {
        valid = "required field"
        e = false
        checkvalidation()
    } else if (mail.match(pattern)) {
        valid = ""
        e = true
        checkvalidation()
    } else {
        e = false
        valid = "please enter valid email"
        checkvalidation()
    }
    $('#check2').html(valid);
}

function checkmess() {
    var msg = $('#passwordfield').val();
    var valid
    if (msg == "") {
        valid = "required field"
        m = false
        checkvalidation()
    } else if (msg.length < 4) {
        valid = "atleast 4 digit"
        m = false
        checkvalidation()
    } else {
        valid = ""
        m = true
        checkvalidation()
    }
    $('#check3').html(valid);
}

function checkmess1() {
    var msg = $('#passwordfield').val();
    var msg1 = $('#passwordfield1').val();
    var valid
    if (msg != msg1) {
        valid = "passwords doesn't match"
        p = false
        checkvalidation()
    } else {
        valid = ""
        p = true
        checkvalidation()
    }
    $('#check4').html(valid);
}

function checkusername() {
    var msg = $('#username').val();
    var valid
    if (msg.length <= 5) {
        valid = "atleast 5 character"
        us = false
        checkvalidation()
    } else {
        valid = ""
        us = true
        checkvalidation()
    }
    $('#check6').html(valid);
}
$('#lastname').keyup(function() {
    checkname();
});
$('#lastname').keyup(function() {
    checklastname();
});
$('#emailfield').keyup(function() {
    checkemail();
});
$('#passwordfield').keyup(function() {
    checkmess();
});
$('#passwordfield1').keyup(function() {
    checkmess1();
});
$('#username').keyup(function() {
    checkusername();
});
$('#submitbtn').click(function() {
    checklastname()
    checkname()
    checkusername()
    checkemail()
    checkmess()
});