let boxes = ajax_get_data();

function ajax_get_data() {
    let event_info = {};
    $.ajax({
        type: "GET",
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        url: "data_3d_plot.json",
        async: false,
        cache: false,

        success: function (jsondata) {
            event_info = jsondata;
        }, error: function () {
            event_info = 'error on loading marker data';
        }, complete: function() {
            //console.logs('emergency event:', event_info)
        }
    });
    return event_info
}

// var boxes = [[0, 0, 0, 100, 20, 30]]
