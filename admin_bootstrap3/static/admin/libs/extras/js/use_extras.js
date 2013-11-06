$(document).ready(function() {
    $('.time-field').timepicker({showMeridian: false, showSeconds: true, minuteStep: 1});
    $('.date-field').datepicker();
    $(".tooltip-toggle").tooltip({placement:'top'});
});

function ActivateChosen(target_id, b, c, d) {
    $("#"+target_id).chosen();
}