//document.ready
$(document).ready(function () {

    $('#region_id').on('change', function (e) {
        region_id = $(this).val();
        baseURL = window.location.origin;

        console.log(region_id)

        $.ajax({
            url: baseURL + '/ems/get_districts/' + region_id,
            type: "get",
            success: function (data) {
                $('#district_id').html(data);
            }
        });
    });


    $('#district_id').on('change', function (e) {
        district_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/ems/get_wards/' + district_id,
            type: "get",
            success: function (data) {
                $('#ward_id').html(data);
            }
        });
    });

    $('#ward_id').on('change', function (e) {
        ward_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/ems/get_villages/' + ward_id,
            type: "get",
            success: function (data) {
                $('#village_id').html(data);
            }
        });
    });


});