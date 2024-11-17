var dash = {
    recentAdded: function (data) {
        container = $('#recentAdded');
        html = '';

        $.each(data, function (index, v) {
            html += `<div class="activity-item d-flex">
                <div class="activite-label text-center">${v[0]}</div>
                <i class='bi bi-circle-fill activity-badge text-success align-self-start'></i>
                    <div class="activity-content">
                        El usuario <kbd>${v[2]}</kbd> de la sucursal <strong>${v[1]}</strong>,
                        ha ingresado la caja Nro. <code>${v[3]}</code>.
                    </div>
                </div>`
        });
        container.append(html);

    },
    loadInfo: function () {
        $.ajax({
            url: pathname,
            type: 'POST',
            data: {'action': 'search_data'},
            dataSrc: '',
            headers: {
                'X-CSRFToken': csrftoken
            },
        }).done(function (data) {
            $.each(data[0], v => {
                $(`#${v}`).text(data[0][v])
            });

            // Draw the data of the last boxes added
            dash.recentAdded(data[1]);

            // Draw in the table Top Brannches
            dash.loadBranchTables(data[2]);
        })
    },
    loadBranchTables: function (info) {
        let valores_finales = [];

        let config = [
            {
                targets: [0],
                visible: false,
            },
            {
                targets: [0, 1, 2, 3, 4, 5],
                class: 'text-center',
            }
        ]

        // Realizamos un ciclo para reorganizar los datos
        // para poder mandarlos a la tabla y los dibuje

        var id = 0;

        console.log(info)

        $.each(info, function (i, v) {
            id += 1;
            total = v[0] + v[1] + v[2];
            valores_finales.push([id, i, total, v[0], v[1], v[2]])
        })

        let data = {
            'data': valores_finales,
            'th': ['id', 'Sucursal', 'Total Cajas', 'Pendientes', 'Revisión', 'Completas'],
            'table': 'tableDash',
            'inserInto': 'rowListDash',
            'config': config,
        };
        drawTableNoAjax(data)

    }
}

$(function () {

        dash.loadInfo();

        //btn card COMPLETE
        $('#btnComplete').on('click', () => {
            let data = {
                'action': 'complete',
                'inserInto': 'rowModal',
                'th': ['id', 'Sucursal', 'Caja', 'Items', 'Estado', 'Usuario', 'Fecha Creacion'],
                'table': 'tableInfoIndexado',
                'config': configOther,
                'modal': true
            };
            drawTables(data);
        });

        //btn card REVISION
        $('#btnRevision').on('click', () => {
            let data = {
                'action': 'revision',
                'inserInto': 'rowModal',
                'th': ['id', 'Sucursal', 'Caja', 'Items', 'Estado', 'Usuario', 'Fecha Creacion'],
                'table': 'tableInfoIndexado',
                'config': configOther,
                'modal': true
            };
            drawTables(data);
        });

        //btn card PENDING
        $('#btnPending').on('click', () => {
            let data = {
                'action': 'pending',
                'inserInto': 'rowModal',
                'th': ['id', 'Sucursal', 'Caja', 'Items', 'Estado', 'Usuario', 'Fecha Creacion'],
                'table': 'tableInfoIndexado',
                'config': configOther,
                'modal': true
            };
            drawTables(data);
        });

        //btn card CANTIDAD DE CAJAS POR SUCURSALES -- TOTAL CAJAS
        $('#btnBox').on('click', () => {
            let data = {
                'action': 'box',
                'inserInto': 'rowModal',
                'th': ['Sucursal', 'Cantidad de Cajas'],
                'table': 'tableInfoIndexado',
                'config': [{
                    targets: [0, 1],
                    class: 'text-center'
                }],
                'modal': true
            };
            drawTables(data);
        });


        //Funcion para dibujar salida de correos
        const email = () => {
            let data = {
                'action': 'notification',
                'inserInto': 'rowTable',
                'th': ['id', 'id_caja', 'id_Usuario', 'Numero de caja', 'Usuario', 'Fecha Movimiento', 'Comentario', 'Enviar'],
                'table': 'tableEmail',
                'config': [{
                    targets: [0, 1, 2],
                    visible: false
                },
                    {
                        targets: [3, 4, 5, 6, 7],
                        class: 'text-center'
                    },
                    {
                        targets: [7],
                        render: function (data, type, row) {
                            return '<a style="color: white;" rel="btnSendEmail" class="btn btn-success"><i class="fa fa-paper-plane"></i></a>'
                        }
                    }],
                'modal': false
            };
            drawTables(data);
        }

        // btn Notifications
        $('#btnNotification').on('click', () => {
            email();
            $('#cardEmail').css('display', 'block');

        });

        $('#tableEmail tbody').on('click', 'a[rel="btnSendEmail"]', function () {
            var tr = tbDash.cell($(this).closest('td, li')).index();
            var data = tbDash.row(tr.row).data();
            console.log(data)

            let parameters = new FormData();
            parameters.append('action', 'email');
            parameters.append('box_id', data[1]);

            submit_with_ajax(window.location.pathname, 'Envio de correo', '¿Has revisado correctamente los parametros?', parameters, () => {
                email();
            })
        })
    }
)