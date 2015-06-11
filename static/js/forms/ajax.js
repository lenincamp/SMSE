/**
 * Created by Lenin on 05/08/2014.
 */
$(function () {

    $.AJAX = function(url, data, funcion, async){
        $.ajax({
            async:async,
            dataType:"json",
            type: 'POST',
            url: url,
            data: data,
            success:  function(respuesta){
                funcion(respuesta);
            }
        });
    };

    $.datepicker.regional['es'] = {
      closeText: 'Cerrar',
      prevText: '&#38;#x3c;Ant',
      nextText: 'Sig&#38;#x3e;',
      currentText: 'Hoy',
      monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
      'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
      monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun',
      'Jul','Ago','Sep','Oct','Nov','Dic'],
      dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
      dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
      dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
      weekHeader: 'Sm',
      //dateFormat: 'yy-mm-dd', 
      dateFormat: 'dd/mm/yy', 
      firstDay: 1,
      isRTL: false,
      /* esto agrege */
      changeYear: true,
      changeMonth: true, 
      yearRange: '-100:+0',
      /* hasta aca*/
      showMonthAfterYear: false,
      yearSuffix: ''
    };
   $.datepicker.setDefaults($.datepicker.regional['es']);
    
});
