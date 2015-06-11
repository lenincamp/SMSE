# -*- coding: utf-8 -*-
from django.core.paginator import  Paginator,EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.db import connection
from principal.models import *
from principal.views import convertDate
from random import choice

import json

def cargarTipoUsuario(request):
    print "cargarTipoUsuario"
    if request.is_ajax():
        if request.method == 'POST':
            print "Entro"
            tipo_usuario = TipoUsuario.objects.all().order_by("nombre").values()
            print tipo_usuario
            return HttpResponse(
                json.dumps(list(tipo_usuario)),
                content_type = "application/json; charset=utf8"
                )
    else:
        raise Http404


def generarClave():
    longitud = 8
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
    p = ""
    p = p.join([choice(valores) for i in range(longitud)])
    return p


def crearUsuario(request):
    if request.is_ajax():                    
            try:
                clave = generarClave()
                usuario = Usuario(
                    usuario = request.POST["usuario"],
                    clave = clave,
                    tipo_usuario_id = request.POST["tipo_usuario"]
                )
                usuario.save()
                print("creo el usuario")
                
                # Guarda Estudiante
                if request.POST["cmbTipoUsuario"] == 'Estudiante':
                    print "entro a guardar estudiante "+request.POST["nombres"]
                    estudiante = Estudiantes(
                        nombres = request.POST["nombres"],
                        apellidos = request.POST["apellidos"],
                        cedula = request.POST["cedula"],
                        email = request.POST["email"],
                        usuario_id = usuario.id
                        )
                    estudiante.save()
                # Guarda Administrador o Dobe
                else:
                    print "entro a guardar empleado "+request.POST["nombres"]+" "+request.POST["email"] 
                    empleado = Empleados(
                        nombres = request.POST["nombres"],
                        apellidos = request.POST["apellidos"],
                        cedula = request.POST["cedula"],
                        email = request.POST["email"],
                        sexo = request.POST["sexo"],
                        telefono_celular = request.POST["telefonoCelular"],
                        usuario_id = usuario.id
                        )
                    empleado.save()

                print("guardo datos")
                send_mail('Se ha generado su usuario para ingresar al sitio web:','usuario:'+str(request.POST['usuario'])+'\n' + 'password:'+clave,'cachabacha.03@gmail.com',[str(request.POST['email'])], fail_silently=False)
                print("envio")
                




                return HttpResponse(
                    json.dumps({"mensaje":"Usuario Creado Correctamente"}),
                    content_type = "application/json; charset=utf8"
                    )

            except Exception, e:
                print e

def cargarNombreUsuario(request, template):
    empleado = Empleados.objects.get(id=request.session["empleados"]["id"])
    usuario = Usuario.objects.get(id=empleado.usuario_id)
    request.session["empleados"]["nombre"] = usuario.usuario
    
    tipo_usuario = TipoUsuario.objects.get(id=usuario.tipo_usuario_id)
    
    if tipo_usuario.nombre.upper() == "ADMINISTRADOR":
        return render(request, template, {"nombre_usuario":request.session["empleados"]["nombre"],"es_admin":True})
    else:
        return render(request, template, {"nombre_usuario":request.session["empleados"]["nombre"],"es_admin":False})

def actaMatricula(request):
    if request.is_ajax():
        estudiante = Estudiantes.objects.get(cedula=request.POST['cedula'])
        matricula = Matricula.objects.get(estudiantes=estudiante)
        matricula = matricula.__dict__
        estudiante = estudiante.__dict__
        del matricula['_state']
        del estudiante['_state']
        return HttpResponse(
                    json.dumps({"m":matricula,"e":estudiante},cls=DjangoJSONEncoder),
                    content_type = "application/json; charset=utf8"
                )
    else: raise Http404

def editaFolio(request):
    if request.is_ajax():
        matricula = Matricula.objects.get(id=request.POST['idMatricula'])
        matricula.fecha_matricula = request.POST['fecha_matricula']
        matricula.folio = request.POST['numero_folio']
        matricula.tipo_matricula = request.POST['tipo_matricula']
        matricula.save()
        return HttpResponse(
                    json.dumps({"bool":True}),
                    content_type = "application/json; charset=utf8"
                )

    else: raise Http404
    
#Filtros Listar Estudiantes
def filtrosEstudiantes(request):
    if request.POST:
       
        try:
            cursor = connection.cursor()
            id_curso=request.POST['cmbCurso']
            id_paralelo=request.POST['cmbParalelo']
            print id_curso, id_paralelo, request.POST['cmbEspecialidad']
            
            if request.POST['cmbEspecialidad']!='0':
                id_especialidad=request.POST['cmbEspecialidad']
                if id_paralelo!='0':
                    cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso= %s and id_paralelo=%s and id_especialidad=%s",(id_curso, id_paralelo, id_especialidad,))
                else:
                    cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso= %s and id_especialidad=%s",(id_curso, id_especialidad,))
            elif id_paralelo!='0':
                cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso= %s and id_paralelo=%s",(id_curso,id_paralelo,))
            else:
                cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso= %s",(id_curso,))
            cur = cursor.fetchall()
            cursor.close()
        except Exception, e:
            print e
        
        return HttpResponse(
                    json.dumps(cur,cls=DjangoJSONEncoder),
                    content_type = "application/json; charset=utf8"
                )
    else: raise Http404


#Cargar Listas
def cargar_listas(request,pagin):
    try:
        cursor = connection.cursor()
        if request.POST:
            try:
                id_curso=request.POST['cmbCurso']
                request.session["id_curso"]=id_curso
                id_paralelo=request.POST['cmbParalelo']
                request.session["id_paralelo"]=id_paralelo
                id_especialidad=request.POST['cmbEspecialidad']
                request.session["id_especialidad"]=id_especialidad
                request.session["bandera"]=1
                cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso=%s and id_paralelo=%s and id_especialidad=%s ORDER BY apellidos asc",(id_curso,id_paralelo,id_especialidad))
            except:
                request.session["bandera"]=2
                cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso=%s and id_paralelo=%s ORDER BY apellidos asc",(id_curso,id_paralelo))
        else:
            if request.session["bandera"]==1:
                cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso=%s and id_paralelo=%s and id_especialidad=%s ORDER BY apellidos asc",(request.session["id_curso"],request.session["id_paralelo"],request.session["id_especialidad"]))
            else:
                if request.session["bandera"]==2:
                    cursor.execute("SELECT * FROM estudiantes_view WHERE id_curso=%s and id_paralelo=%s ORDER BY apellidos asc",(request.session["id_curso"],request.session["id_paralelo"]))
        cur = cursor.fetchall()
        diccionario=[]
        con = 0
        for a in cur:
            con+= 1
            d = {
                "cedula":a[0],
                "alumno":(a[2])+" "+str(a[1]),
                "columna":con
            }
            diccionario.append(d)
        cursor.close()
        paginator=Paginator(diccionario,10)
        try:
            page=int(pagin)
        except:
            page=1
        try:
           pagina=paginator.page(page)
        except EmptyPage:
           pagina=paginator.page(paginator.num_pages)
        except PageNotAnInteger:
           pagina=paginator.page(1)
        if len(cur)>=1:
            return  render(request,"verMatriculas.html",{"mostrar":"ok","pages":pagina,"numeros":len(cur),"nombre_usuario":request.session["empleados"]["nombre"]})
        else:
            return  render(request,"verMatriculas.html",{"mostrar":"no","nombre_usuario":request.session["empleados"]["nombre"]})

    except:
          return  render(request,"verMatriculas.html",{"mostrar":"","nombre_usuario":request.session["empleados"]["nombre"]})

"""===FUNCIONES LI ROY==="""
def cargarComboCurso(request):
    print "cargarComboCurso"
    if request.is_ajax():
        #if request.method == 'POST':
            comboCurso = Cursos.objects.all().order_by("id").values()
            return HttpResponse(
            json.dumps(list(comboCurso)),
            content_type="application/json; charset=utf8"
            )
    else:
            raise Http404

def cargarCursoAsignacion(request):
    
    if request.is_ajax():        
            comboCurso = Cursos.objects.filter(estado=True).order_by("descripcion").values()
            return HttpResponse(
            json.dumps(list(comboCurso)),
            content_type="application/json; charset=utf8"
            )
    else:
            raise Http404

def cargarParalelosAsignacion(request):    
    if request.is_ajax():
        if request.method == 'POST':
            comboParalelo = Paralelos.objects.filter(estado=True).order_by("descripcion").values()
            return HttpResponse(
            json.dumps(list(comboParalelo)),
            content_type="application/json; charset=utf8"
            )
        else:
            raise Http404

def cargarEspecialidadAsignacion(request):
    if request.is_ajax():
        especialidad = Especialidad.objects.filter(estado=True).order_by("nombre").values() #carga datos desde la BD
        return HttpResponse(
            json.dumps(list(especialidad)),
            content_type= "application/json; charset=utf8"
            )
    else:
        raise Http404


def cargarComboParalelos(request):    
    if request.is_ajax():
        if request.method == 'POST':
            comboParalelo = Paralelos.objects.all().order_by("descripcion").values()
            return HttpResponse(
            json.dumps(list(comboParalelo)),
            content_type="application/json; charset=utf8"
            )
        else:
            raise Http404



def cargarEspecialidad(request):
    if request.is_ajax():
        especialidad = Especialidad.objects.all().order_by("nombre").values() #carga datos desde la BD
        return HttpResponse(
            json.dumps(list(especialidad)),
            content_type= "application/json; charset=utf8"
            )
    else:
        raise Http404


def cargarPais(request):
    if request.is_ajax():
        pais = Pais.objects.all().order_by("nombre")       
        return HttpResponse(
            json.dumps(list(pais.values())),
            content_type= "application/json; charset=utf8"
            )
    else:
        raise Http404

def cargarProvincia(request):
    if request.is_ajax():
        provincia = Provincia.objects.select_related('pais__id').all().order_by('nombre')
        vista = provincia.values('id','nombre','pais__nombre','pais__id')

        return HttpResponse(
            json.dumps(list(vista)),
            content_type= "application/json; charset=utf8"
            )
    else:
        raise Http404

def cargarCanton(request):
    if request.is_ajax():        
        canton = Canton.objects.select_related('provincia__id').all().order_by('nombre')
        vista = canton.values('id' , 'nombre' , 'provincia__id' , 'provincia__nombre')
        return HttpResponse(
            json.dumps(list(vista)),content_type="application/json; charset=utf8")
    else:
        raise Http404

def cargarParroquia(request):
    if request.is_ajax():
        print("cargando parroquias")
        parroquia = Parroquia.objects.select_related('ciudad__id').all().order_by('nombre')
        print parroquia.values
        vista = parroquia.values('id','nombre','ciudad__id','ciudad__nombre')
        return HttpResponse(json.dumps(list(vista)),
                content_type="application/json; charset=utf8"
                )
    else:
        raise Http404




def cargarAsignacion(request):
    if request.is_ajax():
        print ("entro a asignacion")
        get = connection.cursor()        
        get.execute("SELECT * FROM asignacion_view")
        data = get.fetchall()
        get.close()
        print data

        return HttpResponse(
                    json.dumps(data,cls=DjangoJSONEncoder),
                    content_type = "application/json; charset=utf8"
                )
    else: 
        raise Http404

def guardarEspecialidad(request):
    if request.is_ajax():
        print("entro a guardar especialidad")
        nuevaEspecialidad = Especialidad(
            nombre= request.POST["especialidad"],
            estado= True
            )
        nuevaEspecialidad.save()

        return HttpResponse(
            json.dumps({"mensaje":"Especialidad guardada"}),
            content_type= "application/json; charset=utf8"
            )


def guardarCurso(request):
    if request.is_ajax():
        curso = request.POST["curso"]       
        est = request.POST["estado"]
        cur = Cursos(
            descripcion = curso,
            estado      = est
            )
        cur.save()
        return HttpResponse(
            json.dumps({"mensaje":"Curso guardado"}),
            content_type="application/json; charset=utf8"
            )



def guardarParalelo(request):
    if request.is_ajax():
        paralelo = Paralelos(
            descripcion= request.POST["paralelo"]
            )
        paralelo.save()
        return HttpResponse(
            json.dumps({"mensaje":"Paralelo guardado"}),
            content_type="application/json; charset=utf8"
            )

def guardarPais(request):
    if request.is_ajax():
        pais = Pais(
            nombre = request.POST["pais"]
            )
        pais.save()
        return HttpResponse(
            json.dumps({"mensaje":"Pais guardado"}),
            content_type="application/json; charset=utf8"
            )

def guardarProvincia(request):
    if request.is_ajax():
        provincia = Provincia(
            nombre = request.POST["provincia"],
            pais_id = request.POST["pais"]
            )
        provincia.save()
        return HttpResponse(
            json.dumps({"mensaje":"Provincia guardada"}),
            content_type="application/json; charset=utf8"
            )

def guardarCanton(request):
    if request.is_ajax():
        canton = Canton(
            nombre = request.POST["canton"],
            provincia_id= request.POST["provincia"]
            )
        canton.save()
        return HttpResponse(
            json.dumps({"mensaje":"Canton guardado"}),
            content_type="application/json; charset=utf8"
            )

def guardarParroquia(request):
    if request.is_ajax():
        print request.POST["parroquia"]
        print request.POST["canton"]
        parroquia = Parroquia(
            nombre = request.POST["parroquia"],
            ciudad_id = request.POST["canton"]
            )
        parroquia.save()
        return HttpResponse(
            json.dumps({"mensaje":"Parroquia guardada"}),
            content_type="application/json; charset=utf8"
            )



def guardarAsignar(request):
    if request.is_ajax():
        asignar = request.POST
        detallecpe = DetalleCursoParaleloEspecialidad(            
            cursos_id           =   asignar["curso"],
            especialidad_id     =   asignar["especialidad"],
            paralelos_id        =   asignar["paralelo"],
            cupos_disponibles   =   asignar["cupo"],
            maximo_cupos        =   asignar["cupo"]
            )
        detallecpe.save()
        return HttpResponse(
            json.dumps({"mensaje":"Curso Asignado"}),
            context_type="application/json; charset=utf8"
            )
    else:
        raise Http404

def modificarCurso(request):
    if request.is_ajax():
        print request.POST
        curso = Cursos.objects.get(id=request.POST["id"])
        curso.descripcion = request.POST["curso"]
        print(type(request.POST["estado"]))
        if request.POST["estado"] == '0':
            curso.estado = False
        else:
            curso.estado = True

        curso.save()
        return HttpResponse(json.dumps({"mensaje":"Curso Modificado"}),
            content_type="application/json ; charset=utf8"
            )
    else:
        raise Http404

def modificarParalelo(request):
    if request.is_ajax():        
        paralelo = Paralelos.objects.get(id=request.POST["id"])
        print paralelo
        paralelo.descripcion = request.POST["paralelo"]        
        if request.POST["estado"] == '0':
            paralelo.estado = False
        else:
            paralelo.estado = True

        paralelo.save()
        return HttpResponse(json.dumps({"mensaje":"Paralelo Modificado"}),
            content_type="application/json ; charset=utf8"
            )
    else:
        raise Http404




def modificarPais(request):
    if request.is_ajax():
        pais   = Pais.objects.get(id=request.POST["id"])
        pais.nombre  = request.POST["pais"]                   
        pais.save()
        return HttpResponse(
            json.dumps({"mensaje":"País Modificado"}),
            content_type="application/json; charset=utf8"
            )
    else:
        raise Http404


def modificarProvincia(request):    
    if request.is_ajax():            
        provincia   = Provincia.objects.get(id=request.POST["id"])
        print (provincia.nombre)
        provincia.nombre  = request.POST["provincia"]
        provincia.pais_id = request.POST["pais"]
        provincia.save()
        return HttpResponse(
                json.dumps({"mensaje":"Provincia Modificada"}),
                content_type="application/json; charset=utf8"
                )
    else:
        raise Http404
        

def modificarCanton(request):
    if request.is_ajax():
        canton = Canton.objects.get(id=request.POST["id"])
        canton.nombre = request.POST["canton"]
        canton.provincia_id = request.POST["provincia"]
        canton.save()
        return HttpResponse(
            json.dumps({"mensaje":"Canton Modificado"}),content_type="application/json; charset=utf8")
    else:
        raise Http404


def modificarParroquia(request):
    if request.is_ajax():
        print ("modificando parroquia")
        parroquia = Parroquia.objects.get( id = request.POST["id"])
        print parroquia.nombre
        print parroquia.ciudad_id
        parroquia.nombre = request.POST["parroquia"]
        parroquia.ciudad_id = request.POST["canton"]
        parroquia.save()
        return HttpResponse({"mensaje":"Parroquia Modificada"},
            content_type = "application/json , charset=utf8")
    else:
        raise Http404


def modificarEspecialidad(request):
    if request.is_ajax():
        especialidad = Especialidad.objects.get(id = request.POST["id"])   
        especialidad.nombre = str(request.POST["especialidad"])
        if request.POST["estado"] == '0':
            especialidad.estado = False    
        else:
            especialidad.estado = True
        especialidad.save()
        return HttpResponse(
            json.dumps({"mensaje":"Especialidad Guardada"}),
            content_type="application/json; charset=utf8"
        )
    else: raise Http404

def guardarEncuesta(request):
    if request.is_ajax():
        enc = EncuestasGraduados.objects.filter(tema=request.POST['txtTema'])
        if enc.count()>0:
            return HttpResponse(
                json.dumps({"mostrar":False}),
                content_type="application/json; charset=utf8"
            )
        else:    
            encuesta = EncuestasGraduados(
                tema = request.POST['txtTema'],
                descripcion = request.POST['txtDescripcion'],
                fecha_inicio = convertDate(request.POST['txtFechaDesde']),
                fecha_fin = convertDate(request.POST['txtFechaHasta'])
            )
            encuesta.save()
            return HttpResponse(
                json.dumps({"mostrar":True, "id_encuesta":encuesta.id}),
                content_type="application/json; charset=utf8"
            )
    raise Http404

def cmbTipoPregunta(request):
    if request.is_ajax():
        tipoP = TipoPregunta.objects.all().order_by('nombre').values('id','nombre')
        return HttpResponse(
                json.dumps(list(tipoP)),
                content_type="application/json; charset=utf8"
            )
    else: raise Http404