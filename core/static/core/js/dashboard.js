$(document).ready(function(){
    $('.dropdown-toggle').dropdown();

    $("#grow-type-radio-button :input").change(function() {
        $('.grow-container').hide();
        var filter_val = $(this).val();
        var selector = '.grow-type-' + filter_val;
        $(selector).show();
        $('#no-active-grows-container').toggle(filter_val=='active');
    });

    function load_panel_state(){
        var storage = $.localStorage;
        var panel_store = storage.get('panel-store');
        if(panel_store){
            $.each(panel_store, function(k,v){
                var grow_id = k;
                // This doesn't need to be a loop because `v` should only ever be on k:v pair, but Javascript.
                for(var group in v){
                    var state = v[group];
                    if(state == false){
                        var panel_body_id = '#collapse-panel-body-'+grow_id+'-'+group;
                        $(panel_body_id).removeClass('in');
                    }
                }
            });
        }
    }
    load_panel_state();

    function panel_masonry(){
        $('.panel-row').masonry({
            itemSelector: '.col-md-6',
        });
    }
    panel_masonry();


    $('.add-plant-button').click(function(){
        $('#add-plant-modal').modal();
        $('#addplant-group').attr('placeholder', $(this).attr('data-group'));
        $('#addplant-grow').val($(this).attr('data-growid'));
        Dajaxice.core.ajax_get_breeders(populate_breeder_list);
    });


    $('.rename-group-group-button').click(function(){
        var kwargs = {'cur_group': $(this).attr('data-group'),
                  'grow_id': $(this).attr('data-growid')};
        show_rename_group_modal(kwargs);
    });

    $('.rename-group-plant-button').click(function(){
        var kwargs = {'cur_group': $(this).attr('data-group'),
                  'plant_id': $(this).attr('data-plantid')};
        show_rename_group_modal(kwargs);
    });

    $('.rename-plant-button').click(function(){
        var kwargs = {'plant_id': $(this).attr('data-plantid')};
        show_rename_plant_modal(kwargs);
    });

    $('.panel-heading[data-toggle-noauto^="collapse"]').click(function(){
        var target = $(this).attr('data-target');

        // This is kind of hacky to get masonry to work in realtime as the panel collapses/expands
        $(target).toggleClass('in')['height']('');
        panel_masonry();
        $(target).toggleClass('in')['height']('');
        // End hacky
        $(target).collapse('toggle');

        var expanded = $(target).attr('aria-expanded');

        var storage_key = 'panel-store';
        var grow_id = $(this).parent().data('growid');
        var group_key = $(this).parent().data('group');

        var storage=$.localStorage;
        var panel_store = storage.get(storage_key);
        if (panel_store == null){
            panel_store = {};
        }
        if(! (grow_id in panel_store) ){
            panel_store[grow_id] = {};
        }
        var value = panel_store[grow_id];
        value[group_key] = (expanded === 'true');
        panel_store[grow_id] = value;
        storage.set(storage_key, panel_store);
    });

    $(".panel-heading .btn, .panel-heading a").on("click", function(e){
        e.stopPropagation();
    });

    $('.change-stage-list').on('click', '.change-stage-option', function(){
      console.log($(this));
      var current_stage = $(this).closest('ul').siblings('button').attr('data-value');
      var new_stage = $(this).attr('data-value');
      var plant_id = $(this).attr('data-target');
      var kwargs = {'plant_id': plant_id, 'new_stage': new_stage}
      Dajaxice.core.ajax_change_plant_stage(change_plant_stage_callback, kwargs);
      $(this).remove();
    });

    $('.delete-plant-button').click(function(){
        var plant_id = $(this).attr('data-plant-id');
        var $confirm_modal = create_modal();
        $confirm_modal.find('.modal-title').text("Confirm Delete");
        $confirm_modal.find('.modal-body').append("<div class='modal-message'></div><p>Are you sure you want to delete this plant?</p>");
        $confirm_modal.modal();
        var primary_button = $confirm_modal.find('.btn-primary')
                                           .removeClass('btn-primary')
                                           .addClass('btn-danger')
                                           .text('Delete');
        primary_button.click(function(){
            var params = {'plant_id': plant_id, 'modal_id': $confirm_modal.attr('id')};
            console.log(params);
            Dajaxice.core.ajax_delete_plant(ajax_delete_plant_callback, params);
        })
    })
});

function create_plant_callback(data){
    $('#add-plant-modal').modal('hide');
    location.reload();
}

function change_plant_stage_callback(data){
    if('error' in data){
        alert(data.error);
    }
    else{
      var button = $('.change-stage-button[data-plant^="'+data.plant_pk+'"]');
      button.html(data.new_stage + " <span class='caret'></span>");
      button.attr('data-value', data.new_stage);

      var $ul = button.siblings('ul');
      $ul.append("<li><a href='#' class='change-stage-option' data-target='"+data.plant_pk+"' data-value='"+data.old_stage+"'>"+data.old_stage+"</a></li>");

      var old_border = button.css('border');
      button.css('border', '2px solid #0c0');
      setTimeout(function(){button.css('border', old_border)}, 3000);
      
    }
}


function ajax_delete_plant_callback(data){
    var modal_id = '#' + data.modal_id;
    if (data.hasOwnProperty('success') && data.success){
        $(modal_id).modal('hide');
        var plant_row = '.plantrow[data-plant-id^='+data.plant_id+']';
        $(plant_row).remove();
    }
    else {
        for (var i = 0; i < data.alerts.length; i++) {
            console.log(i);
            var alert = data.alerts[i];
            var alert_type = alert.type;
            var alert_msg = alert.msg;
            console.log(modal_id);
            show_alert(modal_id + ' .modal-message', alert_type, alert_msg)
        }
    }
}