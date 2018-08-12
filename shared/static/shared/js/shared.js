$(function() {
    $('[data-toggle="popover"]').popover();

    $.fn.exists = function () {
        return this.length !== 0;
    };


});

function show_alert(container, type, content){
    var $container = $(container);
    var $alert = $('<div class="alert"></div>');
    $alert.html('<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                  '<span aria-hidden="true">&times;</span></button>');
    $alert.addClass('alert-'+type);
    $alert.append(content);
    $alert.appendTo($container);
}

function create_modal(uniqueid){
    if(typeof uniqueid == "undefined"){
        uniqueid = Math.round(new Date().getTime() + (Math.random() * 100));
    }
    var $modal = $(''+
    '<div class="modal fade" id="' + uniqueid + '" tabindex="-1">' +
    '   <div class="modal-dialog">' +
    '       <div class="modal-content">' +
    '           <div class="modal-header">' +
    '               <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
    '               <h4 class="modal-title">Modal title</h4>' +
    '           </div>' +
    '           <div class="modal-body">' +
    '           </div>' +
    '           <div class="modal-footer">' +
    '               <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>' +
    '               <button type="button" class="btn btn-primary">Confirm</button>' +
    '           </div>' +
    '       </div>' +
    '   </div>' +
    '</div>');
    return $modal;
}