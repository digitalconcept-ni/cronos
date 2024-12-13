var select_subject;

var utils = {
    addSubject: function(item) {
        workload.details.subjects.push(item)
        workload.list()
    },
}

$(function () {
    select_subject = $('select[name="subject"]');

    select_subject.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                console.log(params);
                return {
                    term: params.term,
                    action: 'search_subject'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese codigo o nombre',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                // '<div class="col-lg-8">' +
                // '<img alt="" src="' + repo.cover + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                // '</div>' +
                '<div class="col-md-8 text-left align-items-center shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre: </b>' + repo.name + '<br>' +
                '<b>Codigo: </b>' + repo.code +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    }).on('select2:select', function (e) {
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            let insert = {
                id_subject: data.id,
                code: data.code,
                name: data.name,
            };
            utils.addSubject(insert)

            console.log(data);

            $(this).val('').trigger('change.select2');
        });
})