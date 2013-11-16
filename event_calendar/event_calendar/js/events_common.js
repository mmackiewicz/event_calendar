

function validate_add_product() {
    valid = true;
    if(!$('#products_list').val()) {
        createErrorMessage("No product selected. Please choose a product or add products first.");
        valid = false;
    }
    if(!validate_integer($('#amount').val())) {
        createErrorMessage("Invalid value for amount.");
        valid = false;
    }

    return valid;
}

function validate_create_event() {
    valid = true;
    now = new Date();
    today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    if($('#producer').val().trim() == "") {
        createErrorMessage("Empty producer name. Please enter valid producer name.");
        valid = false;
    }
    if($('#recipient').val().trim() == "") {
        createErrorMessage("Empty recipient name. Please enter valid recipient name.");
        valid = false;
    }

    if(new Date($('#recipients_date').find('input').val()) < today) {
        createErrorMessage("Recipient's date is not valid. Choose present of future date.");
        valid = false;
    }
    if(new Date($('#production_date').find('input').val()) < today) {
        createErrorMessage("Production date is not valid. Choose present of future date.");
        valid = false;
    }
    if(new Date($('#production_date').find('input').val()) > new Date($('#recipients_date').find('input').val())) {
        createErrorMessage("Production date is later than recipient's date.");
        valid = false;
    }
    return valid;
}