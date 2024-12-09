var classroom = {
    config: [
        {
            targets: [0, 1, 2, 3, 4, 5],
            class: 'text-center',
        },
        {
            targets: [-1],
            orderable: false,
            render: function (data, type, row) {
                var buttons = '<a rel="edit" href="' + pathname + 'change/' + row[0] + '/" class="btn btn-warning btn-xs ml-1"> <i class="bi bi-pencil"></i></a> ';
                buttons += '<a rel="delete" class="btn btn-danger btn-xs"><i class="bi bi-trash"></i></a>';
                return buttons;
            }
        },
    ],
    list: function () {

        let data = {
            'data': {'action': 'search'},
            'inserInto': 'rowList',
            'th': ['Nro', 'Nombre', 'Tipo', 'Edificio', 'Estado', 'Opciones'],
            'table': 'tableList',
            'config': classroom.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    classroom.list();
});