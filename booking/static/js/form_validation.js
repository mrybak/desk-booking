function validate_form() {
    var error_count = 0;
    $('.required').each(function () {
        $(this).removeClass('error');
        if ($(this).val() === '') {
            error_count++;
            $(this).addClass('error');
        }
    });

    var hour_from = $('')

    return error_count == 0;
}

$(function () {
    $('.submit').click(function () {
        if (!validate_form()) {
            return false;
        }
    });

    $( "#date_from" ).datepicker({
        defaultDate: "+1w",
        dateFormat: "yy-mm-dd",
        onClose: function( selectedDate ) {
            $( "#date_to" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#date_to" ).datepicker({
        defaultDate: "+1w",
        dateFormat: "yy-mm-dd",
        onClose: function( selectedDate ) {
            $( "#date_from" ).datepicker( "option", "maxDate", selectedDate );
        }
    });

})
