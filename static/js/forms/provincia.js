$(function(){
	
	//Evento click en el Modal guardar provincia
	$("#btnGuardarProvincia").click(function(){
		var nuevaProvincia = $("#txtNuevaProvincia").val()		
		var idPais = $("#cmbPais").val()		
		var idProvincia = $("#txtIdProvincia").val()		

		if(nuevaProvincia != "")
		{
			if(idProvincia != 0)
			{
				$.AJAX("/si/crear_ppcp/provincia/btnModificarProvincia/",{"id":idProvincia,	"provincia":nuevaProvincia, "pais":idPais},	$.retornoMensajeGuardar,false);
			}			
			else
			{
				$.AJAX("/si/crear_ppcp/provincia/btnGuardarProvincia/",{"provincia":nuevaProvincia, "pais":idPais},$.retornoMensajeGuardar,false);
			}
		}
		else
		{
			$("#alert").html("Llenar el campo Provincia")
			$("#alert").fadeIn(1000)
			$("#alert").fadeOut(3000)
			return false	
		}
	})

	$.devolverProvincia = function(elementoPadre){

		var fila = $(elementoPadre).parent();
		$("#txtNuevaProvincia").val((fila.children()[1]).textContent);		
		$("#txtIdProvincia").val(fila.attr("id"));		
		$("#myModalLabel").html("Editar Provincia");	
	}


	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdProvincia").val("0");
		$("#txtNuevaProvincia").val("");
	}

	$.setPaisOnComboBox = function(idPais){
		var comboPais = $("#cmbPais");
		comboPais.val(idPais);		
	}

	$.cargarTablaProvincia = function(request){
		var provincia = $("#bodyTablaProvincia");
		var datos = "";		
		$.each(request, function(i, item){
			datos += "<tr id = "+item.id+"> <td>"+(i+1)+"</td><td> "+item.nombre+"</td> <td>"+item.pais__nombre+"</td>        <td> <a class='btn btn-info' data-toggle='modal' onclick='$.devolverProvincia($(this).parent()),$.setPaisOnComboBox("+item.pais__id+");' data-target='#idProvincia'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td></tr>";
		});
		provincia.html(datos);
	}

	$.cargarComboPais = function(request){
		var pais = $("#cmbPais");
		var datos = "";
		$.each(request , function(i , item){
			datos += "<option value = "+item.id+">"+item.nombre+"</option>";
		});
		pais.html(datos);
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	$.AJAX("/si/crear_ppcp/provincia/cargarTablaProvincia/","",$.cargarTablaProvincia,false);
	$.AJAX("/si/crear_ppcp/provincia/cargarComboPais/","",$.cargarComboPais,false);

});