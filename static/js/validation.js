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
    } else if (name.match(pattern)) {
        valid = "";
        n = true;
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        n = false
    } else {
        n = false;
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
        l = false;
    } else if (name.match(pattern) && name.length < 3) {
        valid = "please enter atleast 3 letter";
        l = false;
    } else if (name.match(pattern)) {
        valid = "";
        l = true;
    } else if (name.endsWith(" ")) {
        valid = "do not enter space as last character"
        l = false
    } else {
        l = false;
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
        e = false
    } else if (mail.match(pattern)) {
        valid = ""
        e = true
    } else {
        e = false
        valid = "please enter valid email"
    }
    $('#check2').html(valid);
}

function checkmess() {
    var msg = $('#passwordfield').val();
    var valid
    if (msg == "") {
        valid = "required field"
        m = false
    } else if (msg.length < 3) {
        valid = "atleast 3 digit"
        m = false
    } else {
        valid = ""
        m = true
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
    } else {
        valid = ""
        p = true
    }
    $('#check4').html(valid);
}

function checkusername() {
    var msg = $('#username').val();
    var valid
    if (msg.length < 5) {
        valid = "atleast 5 character"
        us = false
    } else {
        valid = ""
        us = true
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





// function checkhouse() {
//     var msg = $('#passwordfield').val();
//     var valid
//     if (msg == "") {
//         valid = "required field"
//         m = false
//     } else if (msg.length < 3) {
//         valid = "atleast 3 digit"
//         m = false
//     } else {
//         valid = ""
//         m = true
//     }
//     $('#check3').html(valid);
// }

// function checkapartment() {
//     var msg = $('#passwordfield').val();
//     var valid
//     if (msg == "") {
//         valid = "required field"
//         m = false
//     } else if (msg.length < 3) {
//         valid = "atleast 3 digit"
//         m = false
//     } else {
//         valid = ""
//         m = true
//     }
//     $('#check3').html(valid);
// }

// function checkstate() {
//     var msg = $('#passwordfield').val();
//     var valid
//     if (msg == "") {
//         valid = "required field"
//         m = false
//     } else if (msg.length < 3) {
//         valid = "atleast 3 digit"
//         m = false
//     } else {
//         valid = ""
//         m = true
//     }
//     $('#check3').html(valid);
// }

// function checkcity() {
//     var msg = $('#passwordfield').val();
//     var valid
//     if (msg == "") {
//         valid = "required field"
//         m = false
//     } else if (msg.length < 3) {
//         valid = "atleast 3 digit"
//         m = false
//     } else {
//         valid = ""
//         m = true
//     }
//     $('#check3').html(valid);
// }

// function checkpin() {
//     var num = $('#number').val();
//     var valid
//     var pattern = /^[0-9]*$/
//     if (num == "") {
//         valid = "required"
//         nu = false
//     } else if (num.match(pattern) && num.length < 6) {
//         valid = "please enter 6 digit number"
//         nu = true
//     } else if (num.match(pattern)) {
//         valid = ""
//         nu = true
//     } else {
//         valid = "please enter numbers only"
//         nu = false
//     }
//     $('#check3').html(valid);
// }

// function checknum() {
//     var num = $('#number').val();
//     var valid
//     var pattern = /^[0-9]*$/
//     if (num == "") {
//         valid = "required"
//         nu = false
//     } else if (num.match(pattern) && num.length < 10) {
//         valid = "please enter 10 digit number"
//         nu = true
//     } else if (num.match(pattern)) {
//         valid = ""
//         nu = true
//     } else {
//         valid = "please enter numbers only"
//         nu = false
//     }
//     $('#check3').html(valid);
// }

// $('#address-firstname').keyup(function() {
//     checkname();
//     checkvalidation()
// });
// $('#address-lastname').keyup(function() {
//     checklastname();
//     checkvalidation()
// });

// $('#address-country').keyup(function() {
//     checkmess();
//     checkvalidation()
// });
// $('#address-house').keyup(function() {
//     checkhouse();
//     checkvalidation()
// });
// $('#address-apartment').keyup(function() {
//     checkapartment();
//     checkvalidation()
// });
// $('#address-city').keyup(function() {
//     checkcity();
//     checkvalidation()
// });
// $('#address-state').keyup(function() {
//     checkstate();
//     checkvalidation()
// });
// $('#address-pin_code').keyup(function() {
//     checkpin();
//     checkvalidation()
// });
// $('#address-phn_no').keyup(function() {
//     checknum();
//     checkvalidation()
// });

// $('#adress-submit').click(function() {
//     checklastname()
//     checkname()
//     checknum()
//     checkpin()
//     checkstate()
//     checkcity()
//     checkapartment()
//     checkhouse()
//     checkmess()
// });