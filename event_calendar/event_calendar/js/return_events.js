$(document).ready(function() {

    $('#return_date').datepicker({format: 'yyyy-mm-dd', weekStart: 1});


    function serialize_product(product_div) {
        return {
            'product': $(product_div).find(".product_name").text(),
            'amount': $(product_div).find(".product_amount").text()
        };
    }

    function serialize_products(products_div) {
        var result = [];
        $(products_div).find(".product_div").each(function() {
            result.push(serialize_product($(this)));
        });
        return result;
    }

    function serialize_transport(transport_div) {
        return {
            'from': $(transport_div).find("input[name=from]").val(),
            'to': $(transport_div).find("input[name=to]").val(),
            'products': serialize_products($(transport_div).find('.products_div'))
        }
    }

    function serialize_transports(transports_div) {
        var result = [];
        $(transports_div).find(".transport_div").each(function() {
            transport = serialize_transport($(this))
            result.push(transport);
        });
        return result;
    }

    $("#add_transport_button").click(function() {
        $transport_div = $("<div/>", {class: "transport_div panel"});
        $from_row = $("<div/>", {class: "row"});
        $from_div = $("<div/>", {class: "col-md-5"});
        $from_div_label = $("<div/>", {class: "col-md-5", text: "from:"});
        $from_div_input = $("<div/>", {class: "col-md-6"}).append("<input type='text' name='from'/>");

        $remove_div = $("<div/>", {class: "col-md-2 col-md-offset-5"}).append("<button class='btn btn-sm btn-default rm_transport_button'>remove</button>");

        $to_row = $("<div/>", {class: "row"});
        $to_div = $("<div/>", {class: "col-md-5"});
        $to_div_label = $("<div/>", {class: "col-md-5", text: "to:"});
        $to_div_input = $("<div/>", {class: "col-md-6"}).append("<input type='text' name='to'/>");


        $products_div = $("<div/>", {class: "panel products_div col-md-10 col-md-offset-1"}).css("border", "0px");

        $product_inputs_row = $("<div/>", {class: "row"});
        $product_inputs = $("<div/>", {class: "col-md-10"}).append("product: <input type='text' name='product'/> amount: <input type='text' name='amount' size=14/>");

        $product_button = $("<div/>", {class: "col-md-2"}).append(" <button class='btn btn-primary btn-md' name='add_product_button'>add</button>");


        $from_div.append($from_div_label).append($from_div_input);
        $to_div.append($to_div_label).append($to_div_input);
        $transport_div.append($from_row.append($from_div).append($remove_div));
        $transport_div.append($to_row.append($to_div));
        $transport_div.append($products_div);
        $transport_div.append($product_inputs_row.append($product_inputs).append($product_button));

        $("#transports_div").append($transport_div);
    });


    $("body").on("click", "button[name=add_product_button]", function() {
        $product_div = $("<div/>", {class: "panel-body product_div row"});
        $product_name = $("<div/>", {class: "product_name col-md-7", text: $(this).parent().parent().parent().find("input[name=product]").val()});
        $product_amount = $("<div/>", {class: "product_amount col-md-3", text: $(this).parent().parent().parent().find("input[name=amount]").val()});
        $remove_button = $("<button/>", {class: "btn btn-default btn-sm rm_product_button", text:"remove"});
        $product_div.append($product_name);
        $product_div.append($product_amount);
        $product_div.append($remove_button);

        $(this).parent().parent().parent().find(".products_div").append($product_div).css("border", "inherit");
    });

    function prepare_request_content() {
        var result = {
            'event_id': $('#event_id').val(),
            'vehicle_id': $('#vehicle_id').val(),
            'return_date': $('#return_date').find('input').val(),
            'comment': $('#comment').val(),
            'transports': serialize_transports($('#transports_div'))
        }

        return result;
    }

    $('#save_button').click(function() {
        $.post(
            "/events/edit_return/"+$('#event_id').val()+"/",
            JSON.stringify(prepare_request_content())
        ).done(function(data) {
            alert(data);
        }).fail(function(data) {
            $('#errors_div').html(data).show();
        })
    });
    $('#create_button').click(function() {
        $.post(
            '/events/create_return/',
            JSON.stringify(prepare_request_content())
        ).done(function(data) {
            alert(data);
        }).fail(function(data) {
            $('#errors_div').html(data).show();
        })
    });

    $('#cancel_button').click(function() {
        window.location.href = "/home/";
    });

    $("body").on('click', '.rm_product_button', function() {
        if($(this).parent().parent().find(".product_div").length == 1) {
            $(this).parent().parent().css("border", "0px");
        }
        $(this).parent().remove();
    });
    $("body").on('click', '.rm_transport_button', function() {
        $(this).parent().parent().parent().remove();
    });
});