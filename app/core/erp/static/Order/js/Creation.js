var tblProducts;
var vents = {
    item: {
        clients: '',
        date_order: '',
        subtotal: 0.00,
        igv: 0.00,
        total: 0.00,
        products: []

    },

    calculate_invoice: function () {
        var subtotal = 0.00;
        var igv = $('input[name="igv"]').val();

        $.each(this.item.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.sale_price);
            subtotal += dict.subtotal;
        });
        this.item.subtotal = subtotal;
        this.item.igv = this.item.subtotal * igv;
        this.item.total = this.item.subtotal + this.item.igv;

        $('input[name="subtotal"]').val(this.item.subtotal.toFixed(2));
        $('input[name="igvcalc"]').val(this.item.igv.toFixed(2));
        $('input[name="total"]').val(this.item.total.toFixed(2));
    },

    add: function (item) {
        this.item.products.push(item);
        this.list();
    },

    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.item.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "mark.name"},
                {"data": "sale_price"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="far fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="number" name="cant" class="form-control for-control-sm input-sm" autocomplete="off" value="' + row.cant + '" >';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'S/' + parseFloat(data).toFixed(2);
                    }
                },
            ],

            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1,
                });
            },

            initComplete: function (settings, json) {

            }
        });
    },
};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_order').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es-pe',
        maxDate: moment().format("YYYY-MM-DD"),//fecha maxima
        //minDate:moment().format("YYYY-MM-DD"),//fecha maxima
    });

    $("input[name='igv']").TouchSpin({
        min: 0,
        max: 1,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();
    })
        .val(0.18);

    //search product / busqueda de productos

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();//deterner el evento
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.item);

            vents.add(ui.item)
            $(this).val('');//limpiar la caja de texto
        }
    });

    //elimnar todos los productos agregados

    $('.btnRemoveAll').on('click', function () {
        if (vents.item.products.length === 0) return false;
        alert_action('Notificación', 'Estas Seguro de Eliminar TODOS los Producto', function () {
            vents.item.products = [];
            vents.list();
        }, function () {

        });
    });

    // evento de agregar mas producto

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td,li')).index();
            alert_action('Notificación', 'Estas Seguro de Eliminar Producto', function () {
                vents.item.products.splice(tr.row, 1);
                vents.list();
            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td,li')).index();
            vents.item.products[tr.row].cant = cant;
            vents.calculate_invoice();

            $('td:eq(5)', tblProducts.row(tr.row).node()).html('S/ ' + vents.item.products[tr.row].subtotal.toFixed(2));

        });

    //envio de datos

    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.item.products.length === 0) {
            mensaje_error('Debe de agregar almenos un Producto');
            return false;
        }

        vents.item.date_order = $('input[name="date_order"]').val();
        vents.item.clients = $('select[name="clients"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.item));

        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                alert_action('Notificación ', '¿Desea Imprimir la Boleta de Venta?', function () {
                    window.open('/erp/SaleInvoicePdfView/' + response.id + '/', '_blank')
                    location.href = '/erp/OrderCreateView/';
                }, function () {
                    location.href = '/erp/OrderCreateView/';
                });
            });
    });

    $('.btnClear').on('click', function () {
        $('input[name="search"]').val('').focus();
    })

    vents.list();
});