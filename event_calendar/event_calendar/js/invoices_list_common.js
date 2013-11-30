/**
 * Created with PyCharm.
 * User: MMA
 * Date: 11/16/13
 * Time: 3:46 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {

    $(".mark_paid_button").click(function(){
        invoice_id = $(this).attr("id");
        blockUX();
        $.post("/invoices/mark_paid/"+invoice_id+"/",
            {}
        ).done(function(data) {
            if(data.status && data.status == 'OK') {
                $parent_tr = $(this).parent().parent();
                $($parent_tr).find("td:nth-child(3)").text("").text("OK");
                $($parent_tr).find("td:nth-child(4)").empty();
            } else {
                $.each(data.errors, function() {
                    createErrorMessage(this);
                });
                showErrorsModal();
            }
        }).fail(function(data) {
            createErrorMessage('status: '+data.status+', statusTEXT: '+data.statusText);
            showErrorsModal();
        });
        unblockUX;
    });

});