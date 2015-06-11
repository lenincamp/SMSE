$(function(){


	$.cargarCanton = function(request){
		var canton = $("#bodyTablaCanton");
		var datos = "";
		$.each(request,function(i , item){
			datos += "<tr id = "+item.id+"> <td>"+(i+1)+"</td> 		<td> "+item.nombre+"</td> 	<td>"+item.provincia__nombre+"</td>	 <td> 	<a class='btn btn-info' data-toggle='modal' onclick='$.devolverCanton($(this).parent()),$.setProvinciaOnComboBox("+item.provincia__id+");' data-target='#idCanton'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td></tr>";
		})
		canton.html(datos);
	}

	$.setProvinciaOnComboBox = function(idProvincia){
		var comboProvincia = $("#cmbProvincia");
		comboProvincia.val(idProvincia);		
	}

	
	$.cargarComboProvincia = function(request){
		var provincia = $("#cmbProvincia");
		var datos = "";
		$.each(request , function(i , item){
			datos += "<option value = "+item.id+">"+item.nombre+"</option>";
		});
		provincia.html(datos);
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	$.devolverCanton = function(elementoPadre){

		var fila = $(elementoPadre).parent();
		$("#txtNuevoCanton").val((fila.children()[1]).textContent);		
		$("#txtIdCanton").val(fila.attr("id"));		
		$("#myModalLabel").html("Editar Canton");	
	}


	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdCanton").val("0");
		$("#txtNuevoCanton").val("");
	}


	$("#btnGuardarCanton").click(function(){
		var idProvincia = $("#cmbProvincia").val();
		var nuevoCanton = $("#txtNuevoCanton").val();
		var idCanton = $("#txtIdCanton").val();

		if(nuevoCanton !="")
		{
			if(idCanton == 0)
			{
				$.AJAX("/si/crear_ppcp/canton/guardarCanton/",{"canton":nuevoCanton, "provincia":idProvincia},$.retornoMensajeGuardar,false);
			}
			else{
				$.AJAX("/si/crear_ppcp/canton/modificarCanton/",{"canton":nuevoCanton, "provincia":idProvincia, "id":idCanton},$.retornoMensajeGuardar,false);				
			}
		}
		else
		{
			$("#alert").html("Llenar el campo Provincia");
			$("#alert").fadeIn(1000);
			$("#alert").fadeOut(2000);
			return false;
		}

	})

	$.AJAX("/si/crear_ppcp/canton/cargarTablaCanton/","",$.cargarCanton,false);
	$.AJAX("/si/crear_ppcp/canton/cargarComboProvincia/","",$.cargarComboProvincia,false);

});