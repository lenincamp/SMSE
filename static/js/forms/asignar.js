$(function(){

	$.cargarCmbCurso = function(respuesta){
		var curso= $("#cmbCurso");
		var datos = "";
		$.each(respuesta, function(i,item) {
			 datos+= "<option value="+item.id+">"+item.descripcion+"</option>";
		});
		curso.html(datos);
	}

	$.cargarCmbEspecialidad = function(respuesta){
		var especialidad = $("#cmbEspecialidad");
		var datos = "";
		$.each(respuesta, function(i,item) {
			 datos+= "<option value="+item.id+">"+item.nombre+"</option>";
		});
		especialidad.html(datos);
	}

	$.cargarParalelos = function(request){
		var paralelos = $("#bodyTablaParalelos");
		var datos = "";
		$.each(request,	function(i , item){

			 		datos+= "<tr id="+item.id+"> <td>"+item.descripcion+"</td> 	<td> <input type='checkbox' id='estadoCheck"+i+"'> </td> <td>		<input type='text' class='col-xs-6' id='txtCupo"+i+"'> 	</td> </tr>";
				
			 			
		});
		paralelos.html(datos);
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}


	
	

	/*
	$.cargarAsignaciones = function(request){
		var tabla = $("#bodyTablaAsignacion");
		datos = "<tr>";
		for (var i= 0; i < request.length; i++) {
			var col ="";
			for (var j = 0; j < request[i].length; j++) {										
				col+="<td>"+request[i][j]+"</td>";							
			};
			datos+=col+"</tr>";
		};
		tabla.html(datos);
	}*/

	$.eliminar = function(padre){
		var fila = $(padre).parent().attr('id');
		//console.log(fila);
		$("#txtIdAsignar").val(fila);
		$("#texto").html("Está seguro de eliminar");
	}


	$.cargarAsignaciones = function(respuesta){
		var tabla = $("#bodyTablaAsignacion");
		var datos = "";		
		$.each(respuesta , function(i , item){
			datos+="<tr id = '"+(item[5])+"'>"+
				 	"<td> "+(i+1)+"</td>"+
			 		"<td> "+item[0]+"</td>"+
			 		"<td> "+item[1]+"</td>"+
			 		"<td> "+item[2]+"</td>"+
			 		"<td> "+item[3]+"</td>"+
			 		"<td> "+item[4]+"</td>"+
			 		"<td><a class='btn btn-danger desactivar' data-toggle='modal' onclick='$.eliminar($(this).parent())'	data-target='#idEliminar'>	<i class='glyphicon glyphicon-remove-circle'> </i> Eliminar </a> </td>"
			 		"</tr>";
		})
		tabla.html(datos)
	}


	$("#btnEliminar").click(function(){
		var id = $("#txtIdAsignar").val();
		$.AJAX("/si/asignar_curso/eliminarAsignacion/",{"id":id},$.retornoMensajeGuardar,true);
		//$.get("/si/asignar_curso/eliminarAsignacion/",{"id":id});

	})

	var contador=0;
	$("#btnAsignar").click(function(){

		
			for(var i = 0+contador ; i < $("#bodyTablaParalelos >tr").length ; i++)
			{			
				if ($("#estadoCheck"+i).is(':checked')) 
				{
					if($("#txtCupo"+i).val() !="" && $("#txtCupo"+i).val() > 0)
					{
						var curso = $("#cmbCurso").val();
						var especialidad = $("#cmbEspecialidad").val();
						var paralelo = $("#bodyTablaParalelos >tr")[i].id;
						var cupo = $("#txtCupo"+i).val();
						$.AJAX("/si/asignar_curso/guardarAsignacion/",{"curso":curso , "especialidad":especialidad , "paralelo":paralelo, "cupo":cupo},$.retornoMensajeGuardar,true);
					}
					else
					{
						
						$("#alert").html("Asigne cupos al paralelo");
						$("#alert").fadeIn(1000);
						$("#alert").fadeOut(1000);
						$("#txtCupo").val("");
						contador = i--;

						return false;
					}
				}
			}
	}) // fin evento boton asignar





	$.AJAX("/si/asignar_curso/cargarEspecialidad/","",$.cargarCmbEspecialidad,true);
	$.AJAX("/si/asignar_curso/cargarParalelos/","",$.cargarParalelos,true);	
	$.AJAX("/si/asignar_curso/cargarCursos/","",$.cargarCmbCurso,true);	
	$.AJAX("/si/asignar_curso/cargarAsignacion/","",$.cargarAsignaciones,true);

});