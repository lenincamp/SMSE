$(function(){
	

	$.cargarParroquias = function(request){
		var parroquia = $("#bodyTablaParroquia");
		var datos = "";

		$.each(request, function(i,item){
			datos+= "<tr id='"+item.id+"'> <td>"+(i+1)+"</td> <td>"+item.nombre+" </td>  <td> "+item.ciudad__nombre+"</td> 	<td> 	<a class='btn btn-info' data-toggle='modal' onclick='$.devolverParroquia($(this).parent()),$.setCantonOnComboBox("+item.ciudad__id+");' data-target='#idParroquia'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td>	  </tr>";
		})
		parroquia.html(datos);
	}

	$.cargarComboCanton = function(request){
		var canton = $("#cmbCanton");
		var datos = "";
		$.each(request , function(i , item){
			datos += "<option value = "+item.id+">"+item.nombre+"</option>";
		});
		canton.html(datos);
	}


	$.devolverParroquia = function(elementoPadre){

		var fila = $(elementoPadre).parent();
		$("#txtNuevaParroquia").val((fila.children()[1]).textContent);		
		$("#txtIdParroquia").val(fila.attr("id"));		
		$("#myModalLabel").html("Editar Canton");	
	}


	$.editarText = function(mensaje){
		$("#myModalLabel").html(mensaje);
		$("#txtIdParroquia").val("0");
		$("#txtNuevaParroquia").val("");
	}

	$.setCantonOnComboBox = function(idCanton){
		$("#cmbCanton").val(idCanton);
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}	

	//Guardar y Modificar Parroquias
	$("#btnGuardarParroquia").click(function(){
		var nuevaParroquia = $("#txtNuevaParroquia").val();
		var idCanton = $("#cmbCanton").val();
		var valor = $("#txtIdParroquia").val();

		if(	nuevaParroquia != "")
		{
			if(valor==0)
			{
				//Guardar
				$.AJAX("/si/crear_ppcp/parroquia/guardarParroquia/",{"parroquia":nuevaParroquia,"canton":idCanton},$.retornoMensajeGuardar,false);
			}
			else
			{
				//Modificar
				$.AJAX("/si/crear_ppcp/parroquia/modificarParroquia/",{"parroquia":nuevaParroquia,"canton":idCanton , "id":valor},$.retornoMensajeGuardar,false);
			}
		}
		else
		{
			$("#alert").html("Llenar el Campo Parroquia");
			$("#alert").fadeIn(1000);
			$("#alert").fadeOut(2000);
			return false;
		}


	})

		$.AJAX("/si/crear_ppcp/parroquia/cargarComboCanton/","",$.cargarComboCanton,false);
		$.AJAX("/si/crear_ppcp/parroquia/cargarParroquia/","",$.cargarParroquias,false);


});