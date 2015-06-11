
$(function(){
    /*Cargar Provincia, Canton, Parroquia*/
    
    $("#cmbProvinciaE").change(function(){
        $.cmbCanton($(this).val());
    });
    $("#cmbCantonE").change(function(){
        $.cmbParroquia($(this).val());
    });
    
    $.cargarCmbProvincia=function(respuesta){
        var cmbProvincias = $("#cmbProvinciaE");
        var option = "";
        $.each(respuesta, function(i, item) {
            option += "<option value="+item.idProvincia+">"+item.nombreP+"</option>";
        });
        cmbProvincias.html(option);
        $.cmbCanton(respuesta[0].idProvincia);
    }

    $.cmbCanton = function(idProvincia){
        $.AJAX("/si/datos_personales/cmb_canton/",{"idP":idProvincia}, $.cargarCmbCanton, false);
    };

    $.cargarCmbCanton =  function(respuesta){
        var cmbCanton = $("#cmbCantonE");
        var option = "";
        $.each(respuesta, function(i, item) {
            option += "<option value="+item.idCanton+">"+item.nombreC+"</option>";
        });
        cmbCanton.html(option);
        $.cmbParroquia(respuesta[0].idCanton);
    };

    $.cmbParroquia = function(idCanton){
        $.AJAX("/si/datos_personales/cmb_parroquia/",{"idC":idCanton}, $.cargarCmbParroquia, false);
    }

    $.cargarCmbParroquia =  function(respuesta){
        var cmbParroquia = $("#cmbParroquiaE");
        var option = "";
        $.each(respuesta, function(i, item) {
            option += "<option value="+item.idParroquia+">"+item.nombreP+"</option>";
        });
        cmbParroquia.html(option);
    };

    $.cargarCmbParentesco = function(respuesta){
        var cmbParentesco = $("#cmbParentezcoRepresentante");
        var option = "";
        $.each(respuesta, function(i, item) {
            option += "<option value="+item.id+">"+item.nombre+"</option>";
        });
        cmbParentesco.html(option);
    };

    $.AJAX("/si/datos_personales/cmb_provincias/","", $.cargarCmbProvincia, false);
    
    $("input[name='rdRepresentante']").change(function(){
       if (this.value == "Otros"){
            $('#pestania_representante').removeClass("hidden");
            $.AJAX("/si/datos_personales/cmb_parentesco/","",$.cargarCmbParentesco, true)
       }
       else
       {
            $('#pestania_representante').addClass("hidden");
       }


   });

    /*====================================*/

    $( "#txtFechaNacimientoE" ).datepicker();

    /*$("#txtFechaNacimientoE").datepicker('option', { dateFormat: 'dd/mm/yy' });*/

    $("#txtFechaNacimientoE").change(function () {
        var today = new Date();
        var birthDate = new Date($("#txtFechaNacimientoE").datepicker("getDate"));
        var age = today.getFullYear() - birthDate.getFullYear();
        var m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        $("#txtEdadE").val(age);
    });

    $.convertDate = function(fecha){
        var arreglo = fecha.split('-');
        return arreglo[2]+"/"+arreglo[1]+"/"+arreglo[0]
    };

    //cargar_datos_page
    $.cargarDatos=function(r)
    {
        if (r.estudiantes.primer_acceso) {
            $("#modalPrimerAcceso").modal('show');
            $('#txtNombresE').val(r.estudiantes.nombres);
            $('#txtApellidosE').val(r.estudiantes.apellidos);
            $('#txtCedulaE').val(r.estudiantes.cedula);
        
        }else{
            
            console.log("no es primero acceso")            
            $('#txtNombresE').val(r.estudiantes.nombres);
            $('#txtApellidosE').val(r.estudiantes.apellidos);
            $('#txtCedulaE').val(r.estudiantes.cedula);
            $('#txtFechaNacimientoE').val($.convertDate(r.estudiantes.fecha_nacimiento));
            var today = new Date();
            var birthDate = new Date(r.estudiantes.fecha_nacimiento);
            var age = today.getFullYear() - birthDate.getFullYear();
            var m = today.getMonth() - birthDate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            console.log("pepe")
            
            $("#txtEdadE").val(age);
            //console.log(r.pais);
            $("#txtLugarNacimiento").val(r.estudiantes.nacionalidad)
            $("#txtTelefonoConvencionalE").val(r.estudiantes.telefono_convencional);
            $("#txtTelefonoMovilE").val(r.estudiantes.telefono_celular);
            $("#txtNombresApellidosEmergenciaE").val(r.estudiantes.nombres_persona_emergencia);
            $("#txtTelefonoConvencionalEmergenciaE").val(r.estudiantes.telefono_convencional_e);
            $("#txtTelefonoMovilEmergenciaE").val(r.estudiantes.telefono_celular_e);
            $("#txtCallePrincipalE").val(r.direccion[0].calle_principal);
            $("#txtNumeroCasaE").val(r.direccion[0].numero_casa);
            $("#txtCalleSecundariaE").val(r.direccion[0].calle_secundaria);
            
            $("#cmbProvinciaE").val(r.provincia[0].id);
            $("#cmbCantonE").val(r.ciudad[0].id);
            $("#cmbParroquiaE").val(r.parroquia[0].id);
            console.log("mechoso");

            ///Datos del Padre
            $("#txtCedulaP").val(r.padre[0].cedula);
            $("#txtNombresP").val(r.padre[0].nombres);
            $("#txtApellidosP").val(r.padre[0].apellidos);
            $("#txtTelefonoConvencionalP").val(r.padre[0].telefono_convencional);
            $("#txtTelefonoCelularP").val(r.padre[0].telefono_celular);
            $("#txtProfesionP").val(r.padre[0].profesion);
            $("#txtOcupacionP").val(r.padre[0].ocupacion);

            console.log(r.datos_papa[0].es_huerfano);

            if (r.datos_papa[0].es_huerfano) {
                $("input:checked[id='chkHuerfanoPadre'][value='Si']").prop('checked', true);
                $("#chkHuerfanoPadre").prop('checked', true);
            }
            if (r.datos_mama[0].es_huerfano) {
                $("input:checked[id='chkHuerfanoMadre'][value='Si']").prop('checked', true);
                $("#chkHuerfanoMadre").prop('checked', true);
            }
            console.log(r.datos_papa[0].retira_carpeta_estudiantil)
            if(r.datos_papa[0].retira_carpeta_estudiantil) {

                $("input:radio[id='rdRetirarCarpetaP'][value='Si']").prop('checked', true);
                $("#rdRetirarCarpetaP").prop('checked', true);
            }
            else {
                $("input:radio[id='rdRetirarCarpetaP'][value='No']").prop('checked', true);
                $("#rdRetirarCarpetaP [value='No']").prop('checked', true);

            }
            if (r.datos_papa[0].vive_estudiante) {

                $("input:radio[id='rdVivePadre'][value='Si']").prop('checked', true);
                $("#rdVivePadre [value='Si']").prop('checked', true);
            }
            else {
                $("input:radio[id='rdVivePadre'][value='No']").prop('checked', true);
                $("#rdVivePadre [value='No']").prop('checked', true);
            }
            $("#cmbNivelEducacionP").val(r.padre[0].nivel_educacion);


            //Datos de la Madre
            $("#txtCedulaM").val(r.madre[0].cedula);
            $("#txtNombresM").val(r.madre[0].nombres);
            $("#txtApellidosM").val(r.madre[0].apellidos);
            $("#txtTelefonoConvencionalM").val(r.madre[0].telefono_convencional);
            $("#txtTelefonoCelularM").val(r.madre[0].telefono_celular);
            $("#txtProfesionM").val(r.madre[0].profesion);
            $("#txtOcupacionM").val(r.madre[0].ocupacion);

            //alert(r.datos_mama[0].retira_carpeta_estudiantil)

            if (r.datos_mama[0].retira_carpeta_estudiantil) {
                $("input:radio[id='rdRetirarCarpetaM'][value='Si']").prop('checked', true);
                $("#rdRetirarCarpetaM [value='Si']").prop('checked', true);
            }
            else {
                $("input:radio[id='rdRetirarCarpetaM'][value='No']").prop('checked', true);
                $("#rdRetirarCarpetaM [value='No']").prop('checked', true);
            }

            if (r.datos_mama[0].vive_estudiante) {
                $("input:radio[id='rdViveMadre'][value='Si']").prop('checked', true);
                $("#rdViveMadre [value='Si']").prop('checked', true);
            }
            else {
                $("input:radio[id='rdViveMadre'][value='No']").prop('checked', true);
                $("#rdViveMadre [value='No']").prop('checked', true);
            }

            $("#cmbNivelEducacionM").val(r.madre[0].nivel_educacion);

            console.log(r)
            if (r.representante == "No") {
                if (r.representante_p[0].sexo == "M") {
                    $("input:radio[id='rdRepresentante'][value='Papi']").prop('checked', true);
                    $("#rdRepresentante [value='Papi']").prop('checked', true);

                }
                else {
                    $("input:radio[id='rdRepresentante'][value='Mami']").prop('checked', true);
                    $("#rdRepresentante [value='Mami']").prop('checked', true);
                }
            }
            else {
                $("input[name='rdRepresentante']").change();
                $('#pestania_representante').removeClass("hidden");
                //Cargar datos de representante
                $("#txtCedulaRepresentante").val(r.representante[0].cedula);
                $("#txtNombresRepresentante").val(r.representante[0].nombres);
                $("#txtApellidosRepresentante").val(r.representante[0].apellidos);
                $("#cmbParentezcoRepresentante").val(r.representante[0].pariente_id);
                $("#txtTelefonoConvencionalR").val(r.representante[0].telefono_convencional);
                $("#txtTelefonoMovilR").val(r.representante[0].telefono_celular);
                $("#cmbNivelEducacionRepresentante").val(r.representante[0].nivel_educacion);
                $("#txtProfesionRepresentante").val(r.representante[0].profesion);
                $("#txtOcupacionRepresentante").val(r.representante[0].ocupacion);
                if (r.representante[0].vive_estudiante) {
                    var viveRep = "Si";
                }else{
                    var viveRep = "No";
                }
                $("input:radio[id='rdViveRepresentante'][value='"+viveRep+"']").prop('checked', true);
                $("#txtDireccionRepresentante").val(r.dir_rep[0].calle_principal);
                $("input:radio[id='rdRepresentante'][value='Otros']").prop('checked', true);
                $("#rdRepresentante [value='Otros']").prop('checked', true);

            }
        }

    }
    /*=== validacion de cedula ===*/
    var invalido = 0;

    $.validacionCedulas = function(id){
       $(id).validarCedulaEC({
            strict: true,
            events: "change",
            onValid: function () {
                invalido = 0;
                var padre = $(id).parent();
                var padreP = $(padre).parent();
                $(id).attr({'data-toggle':'tooltip','data-placement':'right', 'title':'Cédula Correcta'});
                padreP.removeClass('has-error has-feedback');
                padreP.addClass("has-success has-feedback");
                //$('<span>').addClass("glyphicon glyphicon-ok form-control-feedback").appendTo(padre);
                $('[data-toggle="tooltip"]').tooltip(100);
            },
            onInvalid: function () {
                invalido = 1;
                var padre = $(id).parent();
                var padreP = $(padre).parent();
                $(id).attr({'data-toggle':'tooltip','data-placement':'right', 'title':'Cédula Incorrecta'});
                padreP.removeClass('has-success has-feedback')
                padreP.addClass("has-error has-feedback");
                $('[data-toggle="tooltip"]').tooltip(100);            
            }
        }); 
    };
    $.validacionCedulas("#txtCedulaP");

    /*=========================*/
    $.mensaje = function(men){
        $("#mensaje").html(men);
        $("#mensaje").slideDown();
        $("#mensaje").fadeOut(1000);
            
    };

    $.respuestaGuarda = function(response){
        if (response.ok){
            $.mensaje("Los Datos Han Sido Actualizado Correctamente");
        }
    }

    $("#frmDatosPersonales").submit(function(){
        if (invalido == 0){
            $.AJAX("/si/datos_personales/",$(this).serialize(),$.respuestaGuarda,true);
        }else{
            $.mensaje("Los Datos Ingresados son incorrectos");
        }
        
        return false;
    });

});

