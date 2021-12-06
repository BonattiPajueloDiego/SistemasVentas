$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            /*{"data": "category"},*/
            {"data": "desc"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    var buttons = '<a href="/erp/MarkUpdateView/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="far fa-edit"></i></a> ';
                    buttons += '<a href="/erp/MarkDeleteView/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="far fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});