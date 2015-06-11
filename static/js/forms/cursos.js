$(function(){

	$.cargarCmbCurso = function(respuesta){
		var curso= $("#cmbCurso");
		var datos = "";
		$.each(respuesta, function(i,item) {
			 datos+= "<option value="+item.id+">"+item.nombre+"</option>";
		});
		curso.html(datos);
	}

	$.setEditar = function(elementoPadre){

		var fila = $(elementoPadre).parent();		
		$("#txtNuevoCurso").val(fila.children()[1].textContent);
		$("#txtIdCurso").val(fila.attr("id"));
		$("#myModalLabel").html("Editar Curso");	
	}



	$.botonEstado = function(padre,val){
		var tr = $(padre).parent()
		var id =	tr.attr("id");
		var nombre = tr.children()[1].textContent;
		
		/*
		if ((nombre.textContent) && (typeof (nombre.textContent) != "undefined")) 
		{
	        nombre = nombre.textContent;
	    } 
	    else 
	    {
	        nombre = nombre.innerText;
	    }*/

		if(val == 0)
		{
			$.AJAX("/si/crear_cursope/cursos/btnModificarCurso/",{"curso":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)			
			
		}
		else
		{
			$.AJAX("/si/crear_cursope/cursos/btnModificarCurso/",{"curso":nombre , "id":id, "estado":val},$.retornoMensajeGuardar,false)	
			
		}
			$.AJAX("/si/crear_cursope/cursos/tablaCursos/","", $.cargarTablaCurso,true);
	}


	$.cargarTablaCurso = function(respuesta){
		var curso= $("#bodyTablaCursos");
		var datos = "";
		console.log(respuesta);
		$.each(respuesta, function(i,item) 
		{																				
			 if(item.estado==true)
			 	{
			 		datos+= "<tr id="+item.id+">"+
			 		 			"<td>"+(i+1)+"</td>"+
			 		 			"<td>"+item.descripcion+"</td>"+
			 		 			"<td>"+
			 		 				"<a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idCurso'>"+
			 		 					"<i class='glyphicon glyphicon-edit'></i> Editar"+
			 		 				"</a>"+
			 		 			"</td>"+
			 		 			"<td>"+
			 		 				"<a role='button' class='btn btn-danger desactivar' data-toggle='modal' id='0' onclick='$.botonEstado($(this).parent(),this.id)'>"+
			 		 					"<i class='glyphicon glyphicon-remove-circle'></i> Desactivar"+"
			 		 				</a>"+
			 		 			"</td>"+
			 		 		"</tr>";
				}
			 else
			 	{
			 		datos+= "<tr id="+item.id+"> <td>"+(i+1)+"</td> <td>"+item.descripcion+"</td> 	<td> <a class='btn btn-info' data-toggle='modal' onclick='$.setEditar($(this).parent());' data-target='#idCurso'><i class='glyphicon glyphicon-edit'></i> Editar</a> </td>	<td> <a role='button' class='btn btn-success activar' data-toggle='modal' id='1' onclick='$.botonEstado($(this).parent(),this.id)'><i class='glyphicon glyphicon-check'></i> Activar</a> </td> </tr>";
			 	}					
		}
		);		
		curso.html(datos);
	
	}

	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	$.devolverCurso = function(){
		
		$("#txtNuevoCurso").val("");		
		$("#txtIdCurso").val("0");		
		$("#myModalLabel").html("Agregar Nuevo Curso");	
	}

	//Accion click en el Modal guardar curso
	$("#btnGuardarCurso").click(function(){
		var nuevoCurso = $("#txtNuevoCurso").val()
		var idCurso = $("#txtIdCurso").val();
		//var nuevoEstado = $("input:checked[id='checkBoxEstado']").val() | false

			if (nuevoCurso != "") 
			{
				if(idCurso == 0)
				{
					$.AJAX("/si/crear_cursope/cursos/btnGuardarCurso/",{"curso":nuevoCurso , "estado":true},$.retornoMensajeGuardar,false)	
				}
				else
				{
					$.AJAX("/si/crear_cursope/cursos/btnModificarCurso/",{"curso":nuevoCurso , "id":idCurso, "estado":true},$.retornoMensajeGuardar,false)
				}
			} 
			else
			{
				$("#alert").html("Llene el Campo Curso");
				$("#alert").fadeIn(800);
				$("#alert").fadeOut(1800);
				return false
			}	
		
	})

	


	$.AJAX("/si/crear_cursope/cursos/tablaCursos/","", $.cargarTablaCurso,true);


});