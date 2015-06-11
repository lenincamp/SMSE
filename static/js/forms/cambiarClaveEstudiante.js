$(function(){
	var valor = $("#nombreUsuario").text()
	$("#txtUsuario").val(valor.substring(6));
	
	$.mensaje = function(m){
		$("#mesajeBase").html(m);
		$("#mesajeBase").fadeIn('fast');
		$("#mesajeBase").fadeOut(3000);
	};
	
	$.cambioClave = function(respuesta){
		console.log(respuesta);
		if (respuesta.mensaje!="no_mostrar"){
			$.mensaje(respuesta.mensaje);
		}else{
			$("#nombreUsuario").text($("#txtUsuario").val());
			$("#btnCerrarModal").click();	
		}
		
	}
	
	$("#frmCambioClave").submit(function(event) {		
		if($("#frmCambioClave input").val()!=""){
			if($("#txtClaveNueva").val() === $("#txtClaveNuevaConfirma").val()){
				if($("#txtClaveNueva").val()!=$("#txtClaveActual").val()){
					$.AJAX('/si/cambioClaveEstudiante/', $("#frmCambioClave").serialize(), $.cambioClave, true);			
					
					
				}else{
					$.mensaje("Error: La nueva contraseña debe ser diferente a la actual");
				}
				
				
			}else{
				$.mensaje("Error: Las contraseñas no coinciden");
			}
		}else{
			$.mensaje("Error: Todos los campos son obligatorios");
		}

		return false;
	});
});