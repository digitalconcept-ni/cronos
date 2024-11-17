/*
Libreria auxiliar para data tables
Designed by Bryan Urbina Guevara | Digital Concept

se esta utilizando asyncronia para no tener errores en el procesodel dibujado

url = URL a donde haremos la llamada mediante AJAX
action = La accion en la vista donde recolectara la informacion para dibujar (metodo post)
insertInto = Indica en que tabla de todo el lienzo vamos a dibujar la tabla
th = Define una celda de encabezado en una tabla
table = nombre de la tabla donde se dibujara
modal = true (Mostrar el modal en caso que hayan datos que mostrar en tabla del modal) ---  false (para no mostrar el modal
config = configuracion por separado de las columnas formato de DataTables ejm:
config = [{
             targets: [0, 1],
             class: 'text-center'
          }];
  modal: true / false (si la tabla esta dentro de un modal esta opcion activa el modal)
*/

/* SE AGREGO drawTableNoAjax funcion, para dibujar tabla dinamicamente cunado ya traigamos los dato desde otras
* llamada desde el server para no hacf muchas llamadas y utilizara las siguiente configuracion:
* data: variable donde llevara lso datos para dibujar la tabla
* table: id de table
* inserInto: id del tr
* th: Nombre de las columnas
* config: configutacion para etilo de cada columna
* */

const clean = (table, insertInto) => {

    return new Promise((resolve) => {
        let tr = $(`tr[rel='${insertInto}']`); // fila de la tabla donde se insertaran los encabezados

        if (!$.trim(tr.html()).length) {
            resolve(true)
        } else {
            try {
                // Si tiene contenido lo limpia y devuelve true para proceder con el proceso
                let tableName = $(`#${table}`);
                tr.empty();
                tableName.DataTable().clear();
                tableName.DataTable().destroy();
                resolve(true);
            } catch (error) {
                console.log(error)
                message_error(error)
            }
        }
    })
}

const tableColumn = async (data, table, insertInto) => {
    const cleaned = await clean(table, insertInto);

    if (cleaned === true) {
        let trow = $(`#${table} tr[rel=${insertInto}]`).empty();
        let th = '';
        $.each(data, v => {
            th += `<th style="width: auto" class="text-center">${data[v]}</th>`;
        })
        trow.append(th)
    }
    return true;
}

const drawTables = async (data) => {

    var header = await tableColumn(data.th, data.table, data.inserInto);

    if (header === true) {
        $.fn.dataTable.ext.errMode = 'none';

        tableData = $(`#${data.table}`).on('error.dt', function (e, settings, techNote, message) {
            message_error(message.split('-')[1]);
        }).DataTable({
            deferRender: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            orderable: false,
            ajax: {
                url: data.url,
                type: 'POST',
                data: data.action,
                // data: {
                //     'action': data.action,
                // },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            order: false,
            // paging: false,
            ordering: false,
            // info: false,
            // searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: '<i class="bi bi-file-earmark-excel-fill"></i> Descargar Excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat'
                }],
            columnDefs: data.config,
            initComplete: function (settings, json) {
                if (json.hasOwnProperty('error')) {
                    message_error(json.error)
                } else if (json.hasOwnProperty('info')) {
                    message_info(json)
                } else {
                    if (data.modal === true) {
                        $('#modalInfo').modal('show');
                    }
                }
            }
        })
    }
}

const drawTableNoAjax = async (data) => {

    var header = await tableColumn(data.th, data.table, data.inserInto);

    if (header === true) {
        $.fn.dataTable.ext.errMode = 'none';

        tableDataAux = $(`#${data.table}`).on('error.dt', function (e, settings, techNote, message) {
            message_error(message.split('-')[1]);
        }).DataTable({
            deferRender: true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            orderable: false,
            data: data.data,
            order: false,
            // paging: false,
            ordering: false,
            // info: false,
            // searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: '<i class="bi bi-file-earmark-excel-fill"></i> Descargar Excel',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-flat'
                }],
            columnDefs: data.config,
            // initComplete: function (settings, json) {
            //     console.log(json)
            //     // if (json.hasOwnProperty('error')) {
            //     //     message_error(json.error)
            //     // } else if (json.hasOwnProperty('info')) {
            //     //     message_info(json)
            //     // }
            // }
        })
    }
}