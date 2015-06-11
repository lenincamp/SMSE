$(function(){

    /*$( "#txtFechaMatricula" ).datepicker({
        changeMonth: true,
        changeYear: true
    });*/


    $('.filterable .btn-filter').click(function(){
        var $panel = $(this).parents('.filterable'),
        $filters = $panel.find('.filters input'),
        $tbody = $panel.find('.table tbody');
        if ($filters.prop('disabled') == true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });
    $.filtros=function(){
        $('.filterable .filters input').keyup(function(e){
            /* Ignore tab key */
            var code = e.keyCode || e.which;
            if (code == '9') return;
            /* Useful DOM data and selectors */
            var $input = $(this),
            inputContent = $input.val().toLowerCase(),
            $panel = $input.parents('.filterable'),
            column = $panel.find('.filters th').index($input.parents('th')),
            $table = $panel.find('.table'),
            $rows = $table.find('tbody tr');
            /* Dirtiest filter function ever ;) */
            var $filteredRows = $rows.filter(function(){
                var value = $(this).find('td').eq(column).text().toLowerCase();
                console.log(value);
                return value.indexOf(inputContent) === -1;
            });
            /* Clean previous no-result if exist */
            $table.find('tbody .no-result').remove();
            /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
            $rows.show();
            $filteredRows.hide();
            /* Prepend no-result row if all rows are filtered */
            if ($filteredRows.length === $rows.length) {
                $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">Resultado No Encontrado</td></tr>'));
            }
        });
    }


    /*Va tomar funcion de cargarCombos.js(debe estar agregada en el template) Para carar tipos usuarios*/
    $.AJAX("/si/cargar_tipo_usuario/","", $.cargarTipoUsuario, true);

    $.AJAX("/si/registro_matricula/cmb_cursos/","", $.cargarCmbCursos, false);

    $.quitarFiltros = function(){
        $("#divSeccion").fadeOut(400);
        $("#divCurso").fadeOut(400);
        $("#divParalelo").fadeOut(400);
    }

    $.colocarFiltros = function(){
        $("#divSeccion").fadeIn(400);
        $("#divCurso").fadeIn(400);
        $("#divParalelo").fadeIn(400);
    }

    $("#cmbTipoUsuario").change(function (e) {
        var opcion = $("#cmbTipoUsuario option:checked").text();
        if (opcion == "Estudiante"){
            $.colocarFiltros();
        }else if(opcion == "Administrador" || opcion == "Dobe" || $("#cmbTipoUsuario").val()==0){
            $.quitarFiltros();

        }
    })

    /*===FILTROS===*/
    var encabezadosEstudiantes = ""+
                    "<thead>"+
                        "<tr class='filters' id='tblEncabezados'>"+
                            "<th><input type='text' class='form-control' placeholder='#CÉDULA' disabled></th>"+
                            "<th><input type='text' class='form-control' placeholder='ESTUDIANTE' disabled></th>"+
                            "<th><input type='text' class='form-control' placeholder='FO' disabled></th>"+
                            "<th><input type='text' class='form-control' placeholder='CC' disabled></th>"+
                            "<th><input type='text' class='form-control' placeholder='CM' disabled></th>"+
                            "<th><input type='text' class='form-control' placeholder='ED' disabled></th>"+
                        "</tr>"+
                    "</thead>"+

                    "<tbody id='cuerpoTablaEstudiantes'>"+
                    "</tbody>";



    //onmouseover='$.boton()'  onclick="doStuff();"  onmouseout="out()"

    $.retornoFolio=function(r){
        if(r.bool){
            $(".close").click();
        }
    };

    $("#frmFolio").submit(function(){
        datos = {
            "idMatricula":$("#idMatricula").val(),
            "fecha_matricula": $("#txtFechaMatricula").val(),
            "numero_folio": $("#txtNumeroFolio").val(),
            "tipo_matricula": $("#cmbTipo").val()
        }
        $.AJAX("/si/edita_folio/",datos,$.retornoFolio,true)
        return false;
    })

    $.cargaActaMatricula = function(r){
        $("#txtNombres").val(r.e.nombres+" "+r.e.apellidos)
        $("#txtFechaMatricula").val(r.m.fecha_matricula)
        $("#txtNumeroFolio").val(r.m.folio)
        $("#txtNumeroMatricula").val(r.m.numero_matricula)
        $("#idMatricula").val(r.m.id)

    };

    $.obtenerCedulaTabla = function(padre){
        var row = $(padre).parent()
        return (row.children()[0]).textContent

    }
    $.folio = function(padre){
        $.AJAX("/si/usuarios_admins/acta_matricula/",{"cedula":$.obtenerCedulaTabla(padre)},$.cargaActaMatricula,true)
    }

    $.boton = function(){
         $('[data-toggle="modal"]').tooltip(100);
    }


    $.cargarFiltroSeccion = function (response) {
        if (response!=''){

            $("#tablaFiltros").html(encabezadosEstudiantes)
            var tbody = $("#cuerpoTablaEstudiantes")

            var rows = "";
            $.each (response, function(i, item){

                rows += "<tr onmouseover='$.boton()'>"+
                            "<td>"+item[0]+"</td>"+
                            "<td>"+item[1]+" "+item[2]+"</td>"+
                            "<td>"+
                                "<button onclick='$.folio($(this).parent())' class='btn btn-default' style='border:none;background-color:transparent;' data-toggle='modal' data-placement='top' title='FOLIOS' data-target='#modalFrmFolio'>"+
                                    "<span class='glyphicon glyphicon-folder-open'></span>"+
                                "</button>"+
                            "</td>"+
                            "<td>"+
                                "<button class='btn btn-default' style='border:none;background-color:transparent;' data-toggle='modal' data-placement='top' title='CAMBIAR CURSO'>"+
                                    "<span class='glyphicon glyphicon-edit'></span>"+
                                "</button>"+
                            "</td>"+
                            "<td>"+
                                "<button class='btn btn-default'   style='border:none;background-color:transparent;' data-toggle='modal' data-placement='top' title='CERTIFICADO DE MATRICULA'>"+
                                    "<span class='glyphicon glyphicon-list-alt'></span>"+
                                "</button>"+
                            "</td>"+
                            "<td>"+
                                "<button onclick='$.adminCargarDatosEstudiante($(this).parent())'class='btn btn-default' data-toggle='modal' style='border:none;background-color:transparent;' data-placement='top' title='EDITAR/VER'>"+
                                    "<span class='glyphicon glyphicon-pencil'></span>"+
                                "</button>"+
                            "</td>"
                       "</tr>";
            });
            //rows += "</tbody>";

            //$("#tablaFiltros").html(rows);
            tbody.html(rows);
            $.filtros();
            $("#tablaFiltros").fadeIn('slow');
        }else{
            $("#tablaFiltros").fadeOut('slow');
        }
    };


    
    $("#btnFiltrar").click(function(){
        datos = {"cmbCurso":$("#cmbCurso").val(),"cmbEspecialidad":$("#cmbEspecialidad").val(),"cmbParalelo":$("#cmbParalelo").val()}
        $.AJAX('/si/usuarios_admins/filtros_estudiantes/',datos,$.cargarFiltroSeccion, true);
    });





    /*EDITAR DATOS ESTUDIANTES*/
    $.adminCargarDatosEstudiante = function(padre){
        $.AJAX('/si/registro_matricula/admin_cargar_datos_estudiante/',{"cedula":$.obtenerCedulaTabla(padre)}, $.cargarDatos, false);
        $("#cambiarDatos").fadeIn(400);
    }

});

