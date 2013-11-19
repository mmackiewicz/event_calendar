/**
 * Created with PyCharm.
 * User: Marek Mackiewicz
 * Date: 10/15/13
 * Time: 2:35 PM
 */

$.extend($.fn.datepicker.defaults, {
    onRender: function(date) {
        if(date.getDay() == 6 || date.getDay() == 0) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 1 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 1 && date.getDate() == 6) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 3) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 19) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 8 && date.getDate() == 15) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 11 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 11 && date.getDate() == 11) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 12 && date.getDate() == 25) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 12 && date.getDate() == 26) {
            return 'holiday';
        }
        // begin: dates for easter monday
        // 2013
        if(date.getFullYear() == 2013 && date.getMonth()+1 == 4 && date.getDate() == 1) {
            return 'holiday';
        }
        // 2014
        if(date.getFullYear() == 2014 && date.getMonth()+1 == 4 && date.getDate() == 21) {
            return 'holiday';
        }
        // 2015
        if(date.getFullYear() == 2015 && date.getMonth()+1 == 4 && date.getDate() == 6) {
            return 'holiday';
        }
        // 2016
        if(date.getFullYear() == 2016 && date.getMonth()+1 == 3 && date.getDate() == 28) {
            return 'holiday';
        }
        // 2017
        if(date.getFullYear() == 2017 && date.getMonth()+1 == 4 && date.getDate() == 17) {
            return 'holiday';
        }
        // 2018
        if(date.getFullYear() == 2018 && date.getMonth()+1 == 4 && date.getDate() == 2) {
            return 'holiday';
        }
        // 2019
        if(date.getFullYear() == 2019 && date.getMonth()+1 == 4 && date.getDate() == 22) {
            return 'holiday';
        }
        // 2020
        if(date.getFullYear() == 2020 && date.getMonth()+1 == 4 && date.getDate() == 13) {
            return 'holiday';
        }
        // 2021
        if(date.getFullYear() == 2021 && date.getMonth()+1 == 4 && date.getDate() == 5) {
            return 'holiday';
        }
        // 2022
        if(date.getFullYear() == 2022 && date.getMonth()+1 == 4 && date.getDate() == 18) {
            return 'holiday';
        }
        // 2023
        if(date.getFullYear() == 2023 && date.getMonth()+1 == 4 && date.getDate() == 10) {
            return 'holiday';
        }
        // 2024
        if(date.getFullYear() == 2024 && date.getMonth()+1 == 4 && date.getDate() == 1) {
            return 'holiday';
        }
        // end: dates for easter monday
        // begin: dates for corpus christi
        // 2013
        if(date.getFullYear() == 2013 && date.getMonth()+1 == 5 && date.getDate() == 30) {
            return 'holiday';
        }
        // 2014
        if(date.getFullYear() == 2014 && date.getMonth()+1 == 6 && date.getDate() == 19) {
            return 'holiday';
        }
        // 2015
        if(date.getFullYear() == 2015 && date.getMonth()+1 == 6 && date.getDate() == 4) {
            return 'holiday';
        }
        // 2016
        if(date.getFullYear() == 2016 && date.getMonth()+1 == 5 && date.getDate() == 26) {
            return 'holiday';
        }
        // 2017
        if(date.getFullYear() == 2017 && date.getMonth()+1 == 6 && date.getDate() == 15) {
            return 'holiday';
        }
        // 2018
        if(date.getFullYear() == 2018 && date.getMonth()+1 == 5 && date.getDate() == 31) {
            return 'holiday';
        }
        // 2019
        if(date.getFullYear() == 2019 && date.getMonth()+1 == 6 && date.getDate() == 20) {
            return 'holiday';
        }
        // 2020
        if(date.getFullYear() == 2020 && date.getMonth()+1 == 6 && date.getDate() == 11) {
            return 'holiday';
        }
        // 2021
        if(date.getFullYear() == 2021 && date.getMonth()+1 == 6 && date.getDate() == 3) {
            return 'holiday';
        }
        // 2022
        if(date.getFullYear() == 2022 && date.getMonth()+1 == 6 && date.getDate() == 16) {
            return 'holiday';
        }
        // 2023
        if(date.getFullYear() == 2023 && date.getMonth()+1 == 6 && date.getDate() == 8) {
            return 'holiday';
        }
        // 2024
        if(date.getFullYear() == 2024 && date.getMonth()+1 == 5 && date.getDate() == 30) {
            return 'holiday';
        }
        // end: dates for corpus christi
        return '';
    }
});

$(document).ready(function() {
    $('button[id^=errors_modal_close]').click(function() {
        closeErrorsModal();
    });
});

function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(d);
    d.setHours(0,0,0);
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setDate(d.getDate() + 4 - (d.getDay()||7));
    // Get first day of year
    var yearStart = new Date(d.getFullYear(),0,1);
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7)
    // Return array of year and week number
    return [d.getFullYear(), weekNo];
}

function showErrorsModal() {
    $('#errors_modal').modal('show');
}

function closeErrorsModal() {
    $('#errors_div').empty();
    $('#errors_modal').modal('hide');
}

function validate_integer(value) {
    var intRegex = /^\d+$/;
    if(!intRegex.test(value)) {
        return false;
    }
    return true;
}

function createErrorMessage(message) {
    $col = $("<div/>", {class: "col-md-12 error_msg", text: message});
    $('#errors_div').append($col);
}

function validate_password(password) {
    passwordRegex = /^[a-zA-Z0-9]{8,15}$/;
    containsNumberRegex = /^.*\d.*$/;
    containsCapitalRegex = /^.*[A-Z].*$/;
    if(!passwordRegex.test(password)) {
        createErrorMessage("Invalid password value. Password must be at least 8 characters long and consist of letters and numbers.")
        return false;
    } else if(!containsNumberRegex.test(password)) {
        createErrorMessage("Password must contain at least one number.");
        return false;
    } else if(!containsCapitalRegex.test(password)) {
        createErrorMessage("Password must contain at least one capital letter.");
        return false;
    }
    return true;
}