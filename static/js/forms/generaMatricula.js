/**
 * Created by Lenin on 04/11/2014.
 */
$(function(){


    $.cargaTxtMaximoDisponible = function(respuesta){        
        
        if(respuesta.paralelos[0].cupos_disponibles==0){
        
            alert("el cupo en este curso esta completo seleccione otro paralelo");
            /*$("#divMatricula").html("");*/
        }
         $("#txtCupoMaximo").val(respuesta.paralelos[0].maximo_cupos);
         $("#txtCuposDisponibles").val(respuesta.paralelos[0].cupos_disponibles);
        
    }

    
    
    $.AJAX("/si/registro_matricula/cmb_cursos/","", $.cargarCmbCursos, false);   

    /*Generar Matricula*/
    $.gestionarMatricula = function(respuesta){
        $("#divMatricula").html(respuesta.mensaje);        
    }
    
    $("#frmRegistroMatricula").submit(function(){
        
        var data = $("#frmRegistroMatricula").serialize();        
        
        if($("#txtCuposDisponibles").val()>0){
             $.AJAX("/si/generaMatricula/",data, $.gestionarMatricula);
        }else{
            alert("El cupo del curso esta lleno, seleccione otro paralelo y vuelva intentar");
        }
        
        return false;
    });
});

