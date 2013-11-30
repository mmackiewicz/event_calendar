/**
 * Created with PyCharm.
 * User: Marek Mackiewicz
 * Date: 10/15/13
 * Time: 2:35 PM
 */

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

function blockUX() {
    $('#busy_modal').modal({"backdrop": "static"});
}

function unblockUX() {
    $('#busy_modal').modal("hide");
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