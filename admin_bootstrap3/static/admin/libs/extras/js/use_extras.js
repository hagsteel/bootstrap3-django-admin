$(document).ready(function() {
    $('.time-field').timepicker({showMeridian: false, showSeconds: true, minuteStep: 1});
    $('.date-field').datepicker();
    $(".tooltip-toggle").tooltip({placement:'top'});


});

function ActivateChosen(target_id, b, c, d) {
//    $("#"+target_id).chosen();

    var $t = $("#"+target_id);
    $t.multiSelect({
        selectableHeader: "<input type='text' class='search-input form-control' autocomplete='off' placeholder=''>",
        selectionHeader: "<input type='text' class='search-input form-control' autocomplete='off' placeholder=''>",
        afterInit: function(ms){
            var that = this,
                    $selectableSearch = that.$selectableUl.prev(),
                    $selectionSearch = that.$selectionUl.prev(),
                    selectableSearchString = '#'+that.$container.attr('id')+' .ms-elem-selectable:not(.ms-selected)',
                    selectionSearchString = '#'+that.$container.attr('id')+' .ms-elem-selection.ms-selected';

            that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                    .on('keydown', function(e){
                        if (e.which === 40){
                            that.$selectableUl.focus();
                            return false;
                        }
                    });

            that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                    .on('keydown', function(e){
                        if (e.which == 40){
                            that.$selectionUl.focus();
                            return false;
                        }
                    });
        },
        afterSelect: function(){
            this.qs1.cache();
            this.qs2.cache();
        },
        afterDeselect: function(){
            this.qs1.cache();
            this.qs2.cache();
        }
    });

    var $selectAll = $t.parents(".multi-select-wrapper").find(".select-all");
    var $deselectAll = $t.parents(".multi-select-wrapper").find(".deselect-all");

    $selectAll.click(function() {
        var visibles = $t.parents(".multi-select-wrapper").find("li:visible");
        var visibleValues = []
        visibles.each(function (e) {
            visibleValues.push('' + parseInt($(this).attr('id')));
        });
        $t.multiSelect('select', visibleValues);
        return false;
    });

    $deselectAll.click(function(){
        $t.multiSelect('deselect_all');
        return false;
    });
}