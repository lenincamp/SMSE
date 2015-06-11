$(function(){
	

	$.cargarTipoUsuario = function(response){
		var cmbTipoUsuario = $("#cmbTipoUsuario");
		var option = "";
		if(!($("#txtCupoMaximo").length)){      
			var option = "<option value='0' selected='true' enable='false'>Tipos De Usuario:</option>";
		}
	    $.each(response, function(i, item) {
	        option += "<option value="+item.id+">"+item.nombre+"</option>";
	    });
	    cmbTipoUsuario.html(option);
	};

    $.cargarCmbEspecialidad = function (respuesta) {
        var cmbEspecialidad = $("#cmbEspecialidad");
        var option = "";
        if(!($("#txtCupoMaximo").length)){
        	var option = "<option value='0' selected='true' enable='false'>Especialidad:</option>";
        }
        $.each(respuesta, function(i, item) {
        	if (item.nombreE != "NINGUNA"){
            	option += "<option value="+item.idEspecialidad+">"+item.nombreE+"</option>";
        	}
        });
        cmbEspecialidad.html(option);
        $.cmbParalelos($("#cmbCurso").val(),respuesta[0].idEspecialidad);
    }

    $.cmbEspecialidad = function(idCurso){
    	//$.AJAX("/si/registro_matricula/cmb_paralelos/",{"idCurso":$("#cmbCurso").val(), "idEspecialidad":$("#cmbParalelo").val()}, $.cargarCmbParalelos, false);
    	$.AJAX("/si/registro_matricula/cmb_especialidad/",{"idCurso":$("#cmbCurso").val()}, $.cargarCmbEspecialidad, false);
    };

    $.txtMaximoMinimo = function(idParalelo, idCurso){
        $.AJAX("/si/registro_matricula/maximo_disponible/",{"idParalelo":idParalelo, "idCurso":idCurso}, $.cargaTxtMaximoDisponible, false);
    }


    $.cargarCmbParalelos = function (getData)
    {
        var cmbParalelos = $("#cmbParalelo");
        var datos = "";
        if(!($("#txtCupoMaximo").length)){
        	var datos = "<option value='0' selected='true' enable='false'>Paralelo:</option>";
        }
        $.each (getData.paralelos, function(i,item){
            datos+=  "<option value="+  item.id+">"+item.descripcion+"</option>";
        });
        cmbParalelos.html(datos);
        /*COMPARA SI EXISTE EL COMBO*/
        if($("#txtCupoMaximo").length){        	
        	$.txtMaximoMinimo(getData.paralelos[0].id, $("#cmbCurso").val());
        }      

        

    }
    $.cmbParalelos = function(idCurso, idEspecialidad){
    	//$.AJAX("/si/registro_matricula/cmb_paralelos/",{"idCurso":$("#cmbCurso").val(), "idEspecialidad":$("#cmbParalelo").val()}, $.cargarCmbParalelos, false);
  		$.AJAX("/si/registro_matricula/cmb_paralelos/",{"idCurso":$("#cmbCurso").val(), "idEspecialidad":idEspecialidad}, $.cargarCmbParalelos, false);	
    	
    };


    $.cargarCmbCursos = function (respuesta)
    {
        var cmbCursos = $("#cmbCurso");
        var opcion="";
        if(!($("#txtCupoMaximo").length)){
        	var option = "<option value='0' selected='true' enable='false'>Curso:</option>";
        }
        $.each (respuesta, function(i, item)
        {
            option+=  "<option value="+  item.idCurso+">"+item.descripcion+"</option>";
        });
        cmbCursos.html(option);
        $.cmbParalelos(respuesta[0].idCurso,"");
    }

 	$("#cmbCurso").change(function(){
 		if($("#cmbCurso").val()>=5 && $("#cmbCurso").val()<=6){
         	$.cmbEspecialidad($(this).val());
 		}else{
 			$.cmbParalelos($(this).val(),"");
 		}
    });

 	//$("#cmbCurso").change();
    $("#cmbEspecialidad").change(function(){
 		$.cmbParalelos($("#cmbCurso").val(),$(this).val()); 		
    });

    $("#cmbParalelo").change(function(){
    	/*COMPARA SI UN ELEMENTO EXISTE*/
    	if($("#txtCupoMaximo").length){  
        	$.txtMaximoMinimo($(this).val(), $("#cmbCurso").val());
        }        
    });

    
    $("#cmbCurso").change(function(){
        
        if($("#cmbCurso").val() >= 5 && $("#cmbCurso").val() <= 6){
            $.AJAX("/si/registro_matricula/cmb_especialidad/",{"idCurso":$("#cmbCurso").val()}, $.cargarCmbEspecialidad, false);            
            $("#divEspecialidad").fadeIn(400);
            //$("#divEspecialidad").attr("style","display:block");
        }else{
        	$("#divEspecialidad").fadeOut(400);
        	$("#divEspecialidad option").remove();
            //$("#divEspecialidad").attr("style", "display:none");
        }
        
        if($("#cmbCurso").val() >= 1 && $("#cmbCurso").val() <= 3){
            $("#cmbSeccion").val("Vespertina");
        }else if($("#cmbCurso").val() >= 4 && $("#cmbCurso").val() <= 6){
            $("#cmbSeccion").val("Matutina");
        }

    });

});
