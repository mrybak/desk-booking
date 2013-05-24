function validate_form() {
    var error_count = 0;
    $('.required').each(function () {
        $(this).removeClass('error');
        if ($(this).val() === '') {
            error_count++;
            $(this).addClass('error');
        }
    });

    console.log("1: " + error_count);


    $('.numeric').each(function () {
        $(this).removeClass('error');
        console.log(isNaN(parseInt($(this).val(), 10)));
        console.log($(this).val() !== '');
        if (isNaN(parseInt($(this).val(), 10)) && $(this).val() !== '') {
            error_count++;
            $(this).addClass('error');
        }
    });

    console.log("2: " + error_count);

    var hour_from = $('#hour_from').val();
    var hour_to = $('#hour_to').val();

    // FAIL
    if (hour_from !== '' && hour_to !== '') {
        if (hour_from >= hour_to /* is_numeric itd */) {
            error_count++;
        }
    }

    console.log("3: " + error_count);

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
