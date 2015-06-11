$(function() {
	//$("#frmEncuesta input[type='text']").val('')
	$("#txtFechaDesde").datepicker({changeYear: false, changeMonth: false});
	$("#txtFechaHasta").datepicker({changeYear: false, changeMonth: false});
	$('[data-toggle="modal"]').tooltip(100);

	$.mostrarMensaje = function(mensaje){
		$("#mesajeFrmEncuesta").html("<h6><b>"+mensaje+"</b></h6>");
		$("#mesajeFrmEncuesta").slideDown('fast');
		$("#mesajeFrmEncuesta").fadeOut(2500);
	}

	/*$.crearEncuesta = function(respuesta){
		if (respuesta.mostrar){
		
			$("#txtIdEncuesta").val(respuesta.id_encuesta);

			$("#crearEncuesta").fadeOut('fast', function() {
				$("#crearPreguntas").slideToggle('slow');	
			});
			
			
		}else{
			$.mostrarMensaje("La encuesta ya existe!");
		}
	};*/
	$.cargarCmbTipoP = function(respuesta){
		var cmb = $("#cmbTipoP");
		var option = "";
		$.each(respuesta, function(index, val) {
			 option += "<option value="+val.id+">"+val.nombre+"</option>";
		});
		cmb.html(option);
	};

	$("#btnCrearEncuesta").click(function(event) {		
		if($("#frmEncuesta input[type='text']").val()!=''){
			//$.AJAX("/si/guardarEncuestaAdmin/",$("#frmEncuesta").serialize(),$.crearEncuesta,false);
			$("#crearEncuesta").fadeOut('fast', function() {
				$.AJAX("/si/cargar_cmb_tipo_pregunta/","",$.cargarCmbTipoP,true);
				$("#crearPreguntas").slideToggle('slow');					
			});
		}else{
			$.mostrarMensaje("Todos los campos son obligatorios!");
		}
	});

	$("#btnAgregarOpcion").click(function(event) {
		if ($("#txtPregunta").val()!=''){
			if($("#cmbTipoP option:selected").text().toUpperCase()!="SOLO TEXTO"){
				$("#modalFrmOpcion").modal('show');	
			}else{
				$.mostrarMensaje("Escoja bien el tipo de pregunta.");
			}
			
		}else{
			$.mostrarMensaje("Antes de agregar opcion agrege la pregunta!");
		}
		
	});

	var contador = 0, bandera=0;

	$("#btnAgregarOpcionP").click(function(){
		preguntas = $("#txtPregunta").val();
		opciones = ""; 
		for (var i = 0; i < contador; i++) {
			if ($("input[id="+i+"]").val()!=""){
				var val = $("#chkTexto"+i+":checked").val() ; 
				if (val === undefined){
					val = "No";
				}
				opciones+="<li id="+val+">"+$("input[id="+i+"]").val()+"</li>";	
			}
		}
		ol ="<li class='pregunta' style=''>"+
				"<div class='pull-right' style='margin-top:-20px;'>"+
					"<a role='button' class='btn btn-info btn-md' data-toggle='modal' data-placement='top' title='Editar Pregunta' data-target='#modalFrmPregunta'>"+
						"<i class='glyphicon glyphicon-edit'></i>"+
					"</a>"+
				"</div>"+
				"<li id='"+$("#cmbTipoP").val()+"'>"+preguntas+"</li>"+				
				"<ol type=a class='opciones'>"+
					opciones										
				"</ol>"+
			"</li>";
		if (bandera==0){
			$("#divContenedorPreguntas").html(ol);
			bandera = 1;
		}else{
			$("#divContenedorPreguntas").html($("#divContenedorPreguntas").html()+ol);
		}	
		$("#txtPregunta").val("");	
		$("#cerrarFrmOpcion").click();
		$("#modalFrmOpcion :input").val("");
		$("#bodyAgregarOpcion").html("");
		return false;
	});

	$("#btnCrearInputsOpcion").click(function(event) {
        var rows = "";
        var nroOpt = $("#txtNroOpcion").val();
        contador = nroOpt;
        var bodyOpt = $("#bodyAgregarOpcion");
        for (var i = 0; i < nroOpt; i++) {
        	rows += "<div class='row'>"+
        			  "<div class='col-md-5 col-md-offset-2' >"+
	                	(i+1)+') '+
		                "<input type='text' id="+i+">"+  
		              "</div>"+
	            	  "<div class='col-md-5' >"+
		                "<label class='checkbox-inline'>"+
		                "con texto<input type='checkbox' id='chkTexto"+i+"' name='chkTexto' value='Si'>"+ 
		                "</label>"+   
		              "</div>"+
			        "</div>" 	
        };
        bodyOpt.html(rows);
		return false;
	});

	$("#btnPregunta").click(function(){
		if($("#txtPregunta").val()!="")
			if($("#cmbTipoP option:selected").text().toUpperCase()=="SOLO TEXTO"){
				
				var ol ="<li class='pregunta' style=''>"+
							"<div class='pull-right' style='margin-top:-20px;'>"+
								"<a role='button' class='btn btn-info btn-md' data-toggle='modal' data-placement='top' title='Editar Pregunta' data-target='#modalFrmPregunta'>"+
									"<i class='glyphicon glyphicon-edit'></i>"+
								"</a>"+
							"</div>"+
							"<li id='"+$("#cmbTipoP").val()+"'>"+$("#txtPregunta").val()+"</li>"+				
						"</li>";

				if (bandera==0){
					$("#divContenedorPreguntas").html(ol);
					bandera = 1;
				}else{
					$("#divContenedorPreguntas").html($("#divContenedorPreguntas").html()+ol);
				}
			}else{
				$.mostrarMensaje("El tipo de pregunta debe ser: solo texto!");
			}
		else{
			$.mostrarMensaje("Antes de agregar opcion agrege la pregunta!");
		}
		$("#txtPregunta").val("");
	});

});