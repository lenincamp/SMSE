$(function(){


	$.setEditar = function(elementoPadre){

		var fila = $(elementoPadre).parent();
		$("#txtNuevaEspecialidad").val((fila.children()[1]).textContent).focus();
		$("#txtIdEspecialidad").val(fila.attr("id"));
		$("#myModalLabel").html("Editar Especialidad");
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdEspecialidad").val("0");
		$("#txtNuevaEspecialidad").val("");		
	}

	$.botonEstado = function(padre,val){
		var tr = $(padre).parent()
		var id =	tr.attr("id");
		var nombre = tr.children()[1].textContent;		
	

		if(val == 0)
		{
			$.AJAX("/si/crear_cursope/especialidad/modificarEspecialidad/",{"especialidad":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)			
			
		}
		else
		{
			$.AJAX("/si/crear_cursope/especialidad/modificarEspecialidad/",{"especialidad":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)	
			
		}
			
		$.AJAX("/si/crear_cursope/cmbEspecialidad/","", $.cargarEspecialidad,true);
	}


	$.cargarEspecialidad = function(request){
		var especialidad = $("#bodyTablaEspecialidad");
		var datos = "";
		$.each(request,function(i, item)
		{
			if(item.estado==true)
			{
				datos += "<tr id="+item.id+"> 	<td>"+(i+1)+"</td> 	<td>"+item.nombre+"</td> 	<td>  <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());'	data-target='#idEspecialidad'>	<i class='glyphicon glyphicon-edit'> </i> Editar </a> </td> 	<td> <a role='button' class='btn btn-danger desactivar' data-toggle='modal' id='0' onclick='$.botonEstado($(this).parent(),this.id)'><i class='glyphicon glyphicon-remove-circle'></i> Desactivar</a> </td>	</tr>";
			}
			else{
				datos+= "<tr id="+item.id+"> <td>"+(i+1)+"</td> <td>"+item.nombre+"</td> 	<td> <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idEspecialidad'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td>	<td> <a role='button' class='btn btn-success activar' data-toggle='modal' id='1' onclick='$.botonEstado($(this).parent(),this.id)'><i class='lyphicon glyphicon-check'></i> Activar</a> </td> </tr>";
			}
		});
		especialidad.html(datos);
	}



	

	//Guardar la especialidad
	$("#btnGuardarEspecialidad").click(function(){

		//curso = $("#divCursos").children("[id='cmbCurso']").val()//recorre el div y busca el id
		var nuevaEspecialidad = $("#txtNuevaEspecialidad").val()
		var idEspecialidad = $("#txtIdEspecialidad").val()
		
		if (nuevaEspecialidad != "") 
		{
			if(idEspecialidad != 0)
			{
				$.AJAX("/si/crear_cursope/especialidad/modificarEspecialidad/",	{"especialidad":nuevaEspecialidad, "id":idEspecialidad, "estado":true},	$.retornoMensajeGuardar,	false)
			}
			else
			{
				$.AJAX("/si/crear_cursope/especialidad/btnGuardarEspecialidad/",	{"especialidad":nuevaEspecialidad},	$.retornoMensajeGuardar,false)
			}

			
		} 
		else
		{
			$("#alert").html("Llenar el campo Especialidad")
			$("#alert").fadeIn(1000)
			$("#alert").fadeOut(1000)
			return false
		};		
		
		//return false;   //no se da el evento
	})


	$.AJAX("/si/crear_cursope/cmbEspecialidad/","",$.cargarEspecialidad,true);



});