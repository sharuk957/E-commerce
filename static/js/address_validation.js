var house = false
var apartment = false
var city = false
var state = false
var pin = false
var phone = false
var firstname = false
var password = false
var lastname = false

function check_address_validation() {
    if (firstname && house && apartment && state && lastname && city && pin && phone && password) {

        $('#adress-submit').removeAttr('disabled');
    } else {
        $('#adress-submit').attr('disabled', true);
    }
}

function checkname() {
    var name = $('#address-firstname').val();
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
    var name = $('#address-lastname').val();
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

function checkmess() {
    console.log("hi")
    var msg = $('#address-country').val();
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

function checkhouse() {
    var msg = $('#address-house').val();
    var valid
    if (msg == "") {
        valid = "required field"
        house = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        house = false
    } else {
        valid = ""
        house = true
    }
    $('#check2').html(valid);
}

function checkapartment() {
    var msg = $('#address-apartment').val();
    var valid
    if (msg == "") {
        valid = "required field"
        apartment = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        apartment = false
    } else {
        valid = ""
        apartment = true
    }
    $('#check9').html(valid);
}

function checkstate() {
    var msg = $('#address-state').val();
    var valid
    if (msg == "") {
        valid = "required field"
        state = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        state = false
    } else {
        valid = ""
        state = true
    }
    $('#check4').html(valid);
}

function checkcity() {
    var msg = $('#address-city').val();
    var valid
    if (msg == "") {
        valid = "required field"
        city = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        city = false
    } else {
        valid = ""
        city = true
    }
    $('#check6').html(valid);
}

function checkpin() {
    var num = $('#address-pin_code').val();
    var valid
    var pattern = /^[0-9]*$/
    if (num == "") {
        valid = "required"
        pin = false
    } else if (num.match(pattern) && num.length < 6) {
        valid = "please enter 6 digit number"
        pin = true
    } else if (num.match(pattern)) {
        valid = ""
        pin = true
    } else {
        valid = "please enter numbers only"
        pin = false
    }
    $('#check7').html(valid);
}

function checknum() {
    var num = $('#address-phn_no').val();
    var valid
    var pattern = /^[0-9]*$/
    if (num == "") {
        valid = "required"
        phone = false
    } else if (num.match(pattern) && num.length < 10) {
        valid = "please enter 10 digit number"
        phone = true
    } else if (num.match(pattern)) {
        valid = ""
        phone = true
    } else {
        valid = "please enter numbers only"
        phone = false
    }
    console.log(firstname, lastname, house, apartment, state, password, city, pin, phone)
    $('#check8').html(valid);
}

$('#address-firstname').keyup(function() {
    checkname();
    check_address_validation()
});
$('#address-lastname').keyup(function() {
    checklastname();
    check_address_validation()
});

$('#address-country').keyup(function() {
    checkmess();
    check_address_validation()
});
$('#address-house').keyup(function() {
    checkhouse();
    check_address_validation()
});
$('#address-apartment').keyup(function() {
    checkapartment();
    check_address_validation()
});
$('#address-city').keyup(function() {
    checkcity();
    check_address_validation()
});
$('#address-state').keyup(function() {
    checkstate();
    check_address_validation()
});
$('#address-pin_code').keyup(function() {
    checkpin();
    check_address_validation()
});
$('#address-phn_no').keyup(function() {
    checknum();
    check_address_validation()
});

$('#adress-submit').click(function() {
    checklastname()
    checkname()
    checknum()
    checkpin()
    checkstate()
    checkcity()
    checkapartment()
    checkhouse()
    checkmess()
});