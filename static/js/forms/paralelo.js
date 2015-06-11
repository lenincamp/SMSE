$(function(){

	
	$.setEditar = function(elementoPadre){
		var fila = $(elementoPadre).parent();
		$("#txtNuevoParalelo").val((fila.children()[1]).textContent);
		$("#txtIdParalelo").val(fila.attr("id"));
		$("#myModalLabel").html("Editar Paralelo");	
	}

	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdParalelo").val("0");
		$("#txtNuevoParalelo").val("");
	}

	$.botonEstado = function(padre,val){
		var tr = $(padre).parent()
		var id =	tr.attr("id");
		var nombre = tr.children()[1].textContent;		
	

		if(val == 0)
		{
			$.AJAX("/si/crear_cursope/paralelo/btnModificarParalelo/",{"paralelo":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)			
			
		}
		else
		{
			$.AJAX("/si/crear_cursope/paralelo/btnModificarParalelo/",{"paralelo":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)	
			
		}
			$.AJAX("/si/crear_cursope/paralelo/cmbParalelos/","", $.cargarParalelos,true);
	}



	$.cargarParalelos = function(request){
		var paralelos = $("#bodyTablaParalelos");
		var datos = "";
			
			
			$.each(request,	function(i , item){
				if(item.estado==true)
				 	{
				 		datos+= "<tr id="+item.id+"> <td>"+(i+1)+"</td> <td>"+item.descripcion+"</td> 	<td> <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idParalelo'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td>	<td> <a role='button' class='btn btn-danger desactivar' data-toggle='modal' id='0' onclick='$.botonEstado($(this).parent(),this.id)'><i class='glyphicon glyphicon-remove-circle'></i> Desactivar</a> </td> </tr>";
					}
				 else
				 	{
				 		datos+= "<tr id="+item.id+"> <td>"+(i+1)+"</td> <td>"+item.descripcion+"</td> 	<td> <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idParalelo'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td>	<td> <a role='button' class='btn btn-success activar' data-toggle='modal' id='1' onclick='$.botonEstado($(this).parent(),this.id)'><i class='glyphicon glyphicon-check'></i> Activar</a> </td> </tr>";
				 	}

		});
		paralelos.html(datos);
	}


	

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}


	$("#btnGuardarParalelo").click(function(){

		//curso = $("#divCursos").children("[id='cmbCurso']").val()//recorre el div y busca el id
		var nuevoParalelo = $("#txtNuevoParalelo").val()		
		var idParalelo = $("#txtIdParalelo").val()
		var valor = $("#")
		if(nuevoParalelo != "")
		{
			if(idParalelo == 0)
			{
				$.AJAX("/si/crear_cursope/paralelo/btnGuardarParalelo/",	{"paralelo":nuevoParalelo},	$.retornoMensajeGuardar,false)			
			}
			else
			{
				$.AJAX("/si/crear_cursope/paralelo/btnModificarParalelo/",	{"paralelo":nuevoParalelo , "id":idParalelo , "estado":true},	$.retornoMensajeGuardar,false)
			}
		}
		else
		{
			$("#alert").html("Llene el campo Paralelo")
			$("#alert").fadeIn(1000)
			$("#alert").fadeOut(2000)
			return false   //no se da el evento
		};
	})

		$.AJAX("/si/crear_cursope/paralelo/cmbParalelos/","",$.cargarParalelos,true);


});