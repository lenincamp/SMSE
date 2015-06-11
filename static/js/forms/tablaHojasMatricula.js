$(function(){

	$.verHoja = function(padre){
		var tr = $(padre).parent();
		var periodo = tr.attr("id");
		window.open("/si/hoja_matricula/"+periodo,'_blank');	
	};

	$.cargarHojasMatriculas = function(response){
		console.log(response);
		var tbody = $("#bodyTableHojaMatricula");
		var rows = "";
        $.each (response, function(i, item){
        	console.log(response[i])
            rows += "<tr id='"+response[i][0]+"'>"+
                        "<td>"+response[i][0]+" - "+(response[i][0]+1)+"</td>"+
            			"<td>"+response[i][1]+"</td>"+
            			"<td>"+response[i][2]+"</td>"+
            			"<td>"+
            				"<a  style='cursor:pointer;' onclick='$.verHoja($(this).parent())'>Imprimir</a>"+
            			"</td>"+
            		"</tr>";
        });
        tbody.html(rows);
	}
	$.AJAX("/si/cargarTablaHojaMatriculas/", "",$.cargarHojasMatriculas, true);
});