var workload = {
    details: {
        subjects: [],
    },
    list: function () {

        tbListas = $('#tbListas').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.subjects,
            ordering: false,
            order: false,
            columns: [
                {"data": "id_subject"},
                {"data": "code"},
                {"data": "name"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    //orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" title="Eliminar registro" type="button" class="btn btn-danger" style="color: white;"><i class="bi bi-trash"></i></a>';
                    },
                },
                {
                    targets: [0, 1, 2],
                    class: 'text-center',
                },
            ],
            initComplete: function (settings, json) {
                // alert('finish')
            }
        });
    },
};

$(function () {
    let action = $('input[name=action]').val();

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //ELIMINACION DE UN EXPEDIENTE DE LA CAJA
    $('#tbListas tbody').on('click', 'a[rel="remove"]', function () {
        let tr = tbListas.cell($(this).closest('td, li')).index();
        workload.details.subjects.splice(tr.row, 1);
        workload.list();
    })

    //Event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if (workload.details.subjects.length === 0) {
            message_error({'Error de guardado': 'Asigne al menos 1 asignatura al profesor'});
            return false;
        } else {
            var success_url = this.getAttribute('data-url');
            var parameters = new FormData(this);
            parameters.append('subjects', JSON.stringify(workload.details.subjects));
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                location.href = success_url;
            });

        }
    });
    workload.list();
});