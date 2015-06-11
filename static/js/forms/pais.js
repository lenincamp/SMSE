$(function(){

	//Evento click en el Modal guardar curso
	$("#btnGuardarPais").click(function(){
		var nuevoPais = $("#txtNuevoPais").val()
		var opcion = $("#txtIdPais").val()		


		if(nuevoPais != "")
		{
			if(opcion != 0)
			{				
				$.AJAX("/si/crear_ppcp/pais/btnModificarPais/",{"pais":nuevoPais , "id":opcion},$.retornoMensajeGuardar,false)
			}
			else{
				$.AJAX("/si/crear_ppcp/pais/btnGuardarPais/",{"pais":nuevoPais},$.retornoMensajeGuardar,false)
			}
		}
		else{
			$("#alert").html("Llenar el campo País")
			$("#alert").fadeIn(1000)
			$("#alert").fadeOut(3000)
			return false	
		}
		
	
	})


	$.setEditar = function(elementoPadre){

		var fila = $(elementoPadre).parent();
		$("#txtNuevoPais").val((fila.children()[1]).textContent);
		$("#txtIdPais").val(fila.attr("id"));
		$("#myModalLabel").html("Editar Pais");	
	}


	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdPais").val("0");
		$("#txtNuevoPais").val("");
	}

	$.cargarTablaPais = function(request){
		var pais = $("#bodyTablaPais");
		var datos = "";		
		$.each(request, function(i, item){
			datos += "<tr id = "+item.id+"> <td>"+(i+1)+"</td><td> "+item.nombre+"</td> <td> <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idPais'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td></tr>";
		});
		pais.html(datos);
	}



	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	
	//$.AJAX("/si/crear_ppcp/pais/","",$.cargarTablaPais,false);
	$.AJAX("/si/crear_ppcp/pais/cargarTablaPais/","",$.cargarTablaPais,false);

});