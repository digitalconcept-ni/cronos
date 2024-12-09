var group = {
    config: [
        {
            targets: [0, 1, 2, 3],
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
            'th': ['Nro', 'Codigo', 'Nombre', 'Opciones'],
            'table': 'tableList',
            'config': group.config,
            'modal': false,
        }
        drawTables(data);
    }
};

$(function () {
    group.list();
});