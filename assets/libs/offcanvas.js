
$(document).ready(function(){


    $(document).on('click', '.newactivity-btn',function (event) {

        $('#task_details').animate({
            width: "show"
        });

        var aid = $(this).data('aid')
        var url = window.location.origin + '/utils/crf?aid='+aid;
            
        var jqXHR = $.ajax({
            type: "GET",
            url: url,
        }).done(function (data) {
            //alert(data)
            $('#task_details .offcanvas-body-req').html(data);

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('Failed to update progress');
            if (console && console.log) {
                console.log("Loading Ajax: " + textStatus + ", " + errorThrown);
            }
        });

    })


    $(document).on('click', '#createReq-btn',function (event) {
        
        event.preventDefault();

        var url = window.location.origin + '/utils/cra';
        var form = $('#newReq')[0];
        var formData = new FormData(form);

        var jqXHR = $.ajax({
            type: "POST",
            url: url,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
        }).done(function (data) {
            //alert(data)
            $('#task_details .offcanvas-body-req').html(data);

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('Failed to update progress');
            if (console && console.log) {
                console.log("Loading Ajax: " + textStatus + ", " + errorThrown);
            }
        });

    })






    $(document).on('click', '.offcanvas-btn',function (event) {

        var cid = $(this).data('cid');
        $('#'+cid).animate({
            width: "show"
        });

        var rid = $(this).data('rid');

        var url = window.location.origin + '/utils/drd?rid=' + rid;
            
        var jqXHR = $.ajax({
            type: "GET",
            url: url
        }).done(function (data) {
            //set temperature
            $('#'+cid+' .offcanvas-body-req').html(data);

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('Failed to update progress');
            if (console && console.log) {
                console.log("Loading Ajax: " + textStatus + ", " + errorThrown);
            }
        });



    })

    $(document).on('click','.offcanvas-close', function (event) {

        var cid = $(this).closest('.offcanvas-wrp').attr('id');
        $('#'+cid).animate({
            width: "hide"
        });
        $('#task_details .offcanvas-body-req').html('');
    })

    $(document).on('click', '.pgs_btn', function (event) {
            
        var act     = $(this).data('act');
        var pid     = $('#pid').val();
        var cmt     = $('#cmt').val();

        var url = window.location.origin + '/utils/cps?act='+act+'&pid='+pid+'&cmt='+cmt;
        
        var jqXHR = $.ajax({
            type: "GET",
            url: url
        }).done(function (data) {
            //set temperature
            $('#task_details .offcanvas-body-req').html(data);

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('Failed to update progress');
            if (console && console.log) {
                console.log("Loading Ajax: " + textStatus + ", " + errorThrown);
            }
        });
    });

});