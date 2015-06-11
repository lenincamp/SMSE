$(function(){


	$.creaUsuario = function(response){
		alert(response.mensaje);
	};
	

	$("#frmCrearUsuario").submit(function(){
		$.AJAX("/si/crear_usuario_admin/",$("#frmCrearUsuario").serialize(), $.creaUsuario, true);
		return false;
	});


	$.cargarParalelos = function(request){
		var paralelos = $("#cmbParalelo");
		var datos = "";
		$.each(request,	function(i , item){
			datos+= "<option value="+item.id+">"+item.descripcion+"</option>";			
		});
		paralelos.html(datos);
	}


	$.cargarTipoUsuario = function(response){
		var cmbTipoUsuario = $("#cmbTipoUsuario");
		var option = "";
        $.each(response, function(i, item) {
            option += "<option value="+item.id+">"+item.nombre+"</option>";
        });
        cmbTipoUsuario.html(option);
	};


	$.retornoMensajeGuardar = function(respuesta){
		console.log(respuesta.mensaje)
	}

	//Accion click boton Modal Especialidad copia los datos del combo cursos inicial al modal en especialidad
	//$("#btnEspecialidadModal").click(function(){
	//	$("#divCursos").html($("#divCursos1").html());
	//})

	/*
	$("#btnGuardarCanton").click(function(){
		var nuevoCanton = $("#txtNuevoCanton").val()
		$.AJAX("/si/crear_cursope/btnGuardarCanton/",{"canton":nuevoCanton},$.retornoMensajeGuardar,false)		
	})


	$("#btnGuardarParroquia").click(function(){
		var nuevaParroquia = $("#txtNuevaParroquia").val()
		$.AJAX("/si/crear_cursope/btnGuardarParroquia/",{"parroquia":nuevaParroquia},$.retornoMensajeGuardar,false)		
	})

	*/

	
	$.cleanerTextBoxes = function(){

		$("#frmCrearUsuario").find(':input[type="text"]').val("");
	}

	//accion cambia el tipo de Usuario en el combo box
	$("#cmbTipoUsuario").change(function(){
		var cmbTipoUsuario = $("#cmbTipoUsuario option:selected").text()
		if (cmbTipoUsuario == "Estudiante")
			{
				$("#divNombre").attr("style","display: true;")
				$("#divApellido").attr("style","display: true;")
				$("#divCedula").attr("style","display: true;")
				$("#divTelefonoCelular").attr("style","display: none;")
				$("#divSexo").attr("style","display: none;")
			};
		if(cmbTipoUsuario == "Administrador" || cmbTipoUsuario == "Dobe" )
			{
				$("#divNombre").attr("style","display: true;")
				$("#divApellido").attr("style","display: true;")
				$("#divCedula").attr("style","display: true;")
				$("#divTelefonoCelular").attr("style","display: true;")
				$("#divSexo").attr("style","display: true;")

			};
			$.cleanerTextBoxes();		
	})



	$("#btnEnviar").click(function(){
		var cmbTipoUsuario = $("#cmbTipoUsuario option:selected").text()
		var nombre , apellido , cedula , telefonoCelular , sexo , usuario , tipoUsuario;
		//$.post("/si/crear_usuario_admin/",$("#frmCrearUsuario").serialize())
		
		if (cmbTipoUsuario == "Estudiante")
			{
				usuario = $("#txtUsuario").val(); 
				nombre = $("#txtNombre").val();
				apellido = $("#txtApellido").val();
				cedula = $("#txtCedula").val();				
				email = $("#txtEmail").val();
				tipoUsuario = $("#cmbTipoUsuario").val();				
				$.post("/si/crear_usuario_admin/",{"usuario":usuario , "nombres":nombre , "apellidos":apellido , "cedula":cedula , "email":email , "tipo_usuario":tipoUsuario, "cmbTipoUsuario":"Estudiante" });

			};
		if(cmbTipoUsuario == "Administrador" || cmbTipoUsuario == "Dobe")
			{
				
				usuario = $("#txtUsuario").val(); 
				nombre = $("#txtNombre").val();
				apellido = $("#txtApellido").val();
				cedula = $("#txtCedula").val();
				sexo = $("#txtSexo").val();
				telefonoCelular = $("#txtTelefonoCelular").val();
				email = $("#txtEmail").val();
				tipoUsuario = $("#cmbTipoUsuario").val();
				$.post("/si/crear_usuario_admin/",{"usuario":usuario , "nombres":nombre , "apellidos":apellido , "cedula":cedula , "email":email ,"sexo":sexo, "telefonoCelular":telefonoCelular, "tipo_usuario":tipoUsuario, "cmbTipoUsuario":cmbTipoUsuario });

			};

		$("#mensaje").fadeIn(1000);
		$("#mensaje").fadeOut(4000);
		$.cleanerTextBoxes();
		
	})


	$.AJAX("/si/cargar_tipo_usuario/","", $.cargarTipoUsuario, true);
	//$.AJAX("/si/crear_cursope/cmbCurso/","",	$.cargarCmbCurso,true);
	
	
	




});