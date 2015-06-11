 # -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Image, Drawing
from django.db import connection
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
import time

class report_matricula :
	def date_spanish(self, date):
	    array = date.split('-')
	    day = array[0]
	    number_day = array[1]
	    month = array[2]
	    year = array[3]
	    
	    months = {
	        'January':'Enero', 
	        'February' : 'Febrero', 
	        'March' : 'Marzo',
	        'April': 'Abril',
	        'May' : 'Mayo', 
	        'June': 'Junio', 
	        'July': 'Julio',
	        'August':'Agosto', 
	        'September':'Septiembre', 
	        'October':'Octubre', 
	        'November':'Noviembre', 
	        'December':'Diciembre' 
	    }

	    days = {
	        'Monday':'Lunes',
	        'Tuesday':'Martes',
	        'Wednesday':'Miercoles',
	        'Thursday':'Jueves',
	        'Friday':'Viernes',
	        'Saturday':'Sábado',
	        'Sunday':'Domingo'
	    }

	    for (english, espanish) in months.items() :
	        print english, espanish

	        if month.upper() == english.upper():
	            month = espanish

	    for (english, espanish) in days.items() :
	        if day.upper() == english.upper():
	            day = espanish
	    return day + ' ' +number_day + ' de ' + month + ' del ' + year

	def to_pdf(self, request, periodo):
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM hoja_matricula_view WHERE id_estudiante=%s AND periodo=%s",(request.session['estudiante']['id'], periodo,))
			cur = cursor.fetchall()
			
			response = HttpResponse (mimetype='application/pdf')
			response ['Content - Disposition'] = 'attachment; filename= hoja-de-matricula.pdf'

			p = canvas.Canvas(response)
			#p.drawImage("C:/Users/Lenin/Desktop/tesis/SMSE/static/img/logo.jpg", 60,720, width=105,height=80)
			#p.drawImage("../../static/img/logo.jpg", 60,720, width=105,height=80)

			p.setFont ('Helvetica-Bold',14)
			p.drawString (160,745,'COLEGIO DE BACHILLERATO "EL ORO"')			

			p.setFont ('Helvetica-Bold',12)
			p.drawString (172,705,'DATOS DEL ESTUDIANTE MATRICULADO')
			p.setFont ('Helvetica',10)
			p.drawString (60,680,'Año Lectivo:')

			p.drawString (125,680,str(cur[0][0])[:-2])
			p.line (124, 677, 210,677)

			p.drawString (450,680,'Folio:')
			p.line (475, 677, 550,677)
		
		
			p.drawString (60,660,'Fecha:')
			p.drawString (125,660,'MACHALA, '+self.date_spanish(time.strftime("%A-%d-%B-%Y")))
			p.line (124, 657, 440,657)
		
			p.rect(480,590, 70, 80,stroke=1,fill=0) 

			p.drawString (60,640,'Nombre:')
			p.drawString (125,640,str(cur[0][1]).upper())
			p.line (124, 637, 440,637)

			p.drawString (60,620,'Curso:')
			p.drawString (125,620,str(cur[0][2]).upper())
			p.line (124, 617, 270,617)

			p.drawString (285,620,'Paralelo:')
			p.drawString (330,620,str(cur[0][4]).upper())
			p.line (328, 617, 338,617)

			p.drawString (345,620,'Sección:')
			p.drawString (385,620,str(cur[0][5]).upper())
			p.line (383, 617, 440,617)

			p.drawString (60,600,'Especialidad:')
			p.drawString (125,600,str(cur[0][3]).upper())
			p.line (124, 597, 270,597)

			p.drawString (285,600,'Modalidad:')
			p.drawString (338,600,str(cur[0][6]).upper())
			p.line (336, 597, 440,597)

			p.drawString (60,580,'Matricula Nº:')
			p.drawString (125,580,str(cur[0][7]).upper())
			p.line (124, 577, 270,577)

			p.setFont ('Helvetica-Bold',12)
			p.drawString (232,530,'DATOS PERSONALES')

			p.setFont ('Helvetica',10)	
			p.drawString (60,505,'Cédula:')
			p.drawString (170,505,str(cur[0][8]).upper())
			p.line (168, 502, 270,502)

			p.drawString (285,505,'Fecha de Nacimiento:')
			p.drawString (385,505,str(cur[0][10]).upper())
			p.line (384, 502, 440,502)

			p.drawString (450,505,'Edad:')
			p.drawString (481,505,str(cur[0][13]).upper())
			p.line (479, 502, 550,502)


			p.drawString (60,485,'Dirección:')
			p.drawString (170,485,str(cur[0][9]).upper())
			p.line (168, 482, 550,482)

			p.drawString (60,465,'Email:')
			p.drawString (170,465,str(cur[0][11]).upper())
			p.line (168, 462, 295,462)

			p.drawString (60,445,'Teléfonos:')
			p.drawString (170,445,str(cur[0][12]).upper())
			p.line (168, 442, 295,442)

			p.drawString (60,425,'Lugar de Nacimiento:')
			p.drawString (170,425,str(cur[0][14]).upper())
			p.line (168, 422, 295,422)

			if str(cur[0][15]).upper() == 'M':
				genero = 'MASCULINO'
			else: genero = 'FEMENINO'
			p.drawString (60,405,'Género:')
			p.drawString (170,405,genero)
			p.line (168, 402, 295,402)

			p.setFont ('Helvetica-Bold',12)
			p.drawString (232,362,'DATOS FAMILIARES')

			p.setFont ('Helvetica',10)
			p.drawString (60,337,'Nombre del Padre:')
			p.drawString (170,337,str(cur[0][16]).upper())
			p.line (168, 335, 550,335)

			p.drawString (60,317,'Ocupación del Padre:')
			p.drawString (170,317,str(cur[0][17]).upper())
			p.line (168, 315, 550,315)

			p.drawString (60,297,'Nombre de la Madre:')
			p.drawString (170,297,str(cur[0][18]).upper())
			p.line (168, 295, 550,295)

			p.drawString (60,277,'Ocupación de la Madre:')
			p.drawString (170,277,str(cur[0][19]).upper())
			p.line (168, 275, 550,275)

			p.drawString (60,217,"""En consecuencia el INSTITUTO SUPERIOR TECNOLÓGICO "EL ORO" reconoce los derechos y obligaciones""")
			p.drawString (60,197,"""que le corresponden al alumno matriculado. Para mayor constancia, firman la presente matricula:""")
			p.drawString (152,177, """El Señor Rector, el Alumno Matriculado y el Secretario(a) Abogado(a) .""")
			
			p.line (60, 95, 210,95)
			p.drawString (80,79,'RECTOR DEL COLEGIO')

			p.line (230, 95, 380, 95)
			p.drawString (240,79,'SECRETARIO(A) ABOGADO')

			p.line (400, 95, 550, 95)
			p.drawString (450,79,'ALUMNO(A)')

			p.showPage ()
			p.save ()
			return response
		except Exception, e:
			print e
			raise Http404
		finally:
			cursor.close()

