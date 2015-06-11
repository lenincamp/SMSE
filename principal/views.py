 # -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from models import *
from datetime import *
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from matricula import report_matricula

def to_pdf(request, periodo):
    if 'estudiante' in request.session:
        report = report_matricula()
        matricula = report.to_pdf(request, periodo)
        return matricula
    else: raise Http404


def cargaPaginas(request, template):
    return render(request, template, {})


@csrf_exempt
def cmbCursos(request):
    if request.is_ajax():
     if request.method == 'POST':
            print("1")
            cursos = Cursos.objects.all().order_by('id')
            data = []
            for curso in cursos:
                data.append({
                    'idCurso' : curso.id,
                    'descripcion' : curso.descripcion
                })
            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404


@csrf_exempt
def cmbParalelos(request):
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['idEspecialidad'] == "":
                detalle = DetalleCursoParaleloEspecialidad.objects.filter(cursos_id = request.POST['idCurso'])
            else:
                detalle = DetalleCursoParaleloEspecialidad.objects.filter(cursos_id = request.POST['idCurso'], especialidad_id=request.POST['idEspecialidad'])
            paralelos = Paralelos.objects.filter(id__in = detalle.values('paralelos_id')).order_by('descripcion')
            paralelos = paralelos.values('id','descripcion')
            #paralelos = paralelos.values('id','descripcion', 'cupos_disponibles','maximo_cupos')

            return HttpResponse(
                json.dumps({'paralelos':list(paralelos)},cls=DjangoJSONEncoder),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

@csrf_exempt
def dispobiblesMaximos(request):
    if request.is_ajax():
        if request.method == 'POST':
            detalle = DetalleCursoParaleloEspecialidad.objects.filter(cursos_id = request.POST['idCurso'], paralelos_id = request.POST['idParalelo'])
            paralelos = detalle.values('cupos_disponibles','maximo_cupos')
            return HttpResponse(
                json.dumps({'paralelos':list(paralelos)},cls=DjangoJSONEncoder),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404


@csrf_exempt
def cmbEspecialidad(request):
    if request.is_ajax():
        if request.method == 'POST':
            especialidad = DetalleCursoParaleloEspecialidad.objects.filter(cursos_id = request.POST['idCurso']).values('especialidad_id')            
            especialidad = Especialidad.objects.filter(id__in=especialidad)
            data = []
            if especialidad.count() > 0:

                for esp in especialidad:
                    data.append({
                        'idEspecialidad' : esp.id,
                        'nombreE'     : esp.nombre
                    })
            else:
                data.append({'idEspecialidad' : "",'nombreE': ""})

            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

def cmbPais(request):
    if request.is_ajax():
        if request.method == 'POST':
            paises = Pais.objects.all().order_by('nombre')
            data = []
            for pais in paises:
                data.append({
                    'idPais' : pais.id,
                    'nombreP': pais.nombre
                })
            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

@csrf_exempt
def cmbProvincias(request):
    if request.is_ajax():
        if request.method == 'POST':
            provincias = Provincia.objects.all().order_by('nombre')
            data = []
            for provincia in provincias:
                data.append({
                    'idProvincia' : provincia.id,
                    'nombreP'     : provincia.nombre
                })
            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

@csrf_exempt
def cmbCanton(request):
    if request.is_ajax():
        if request.method == 'POST':
            canton = Canton.objects.filter(provincia=request.POST['idP']).order_by('nombre')
            data = []
            for canton in canton:
                data.append({
                    'idCanton' : canton.id,
                    'nombreC'  : canton.nombre
                })
            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404


@csrf_exempt
def cmbParroquia(request):
    if request.is_ajax():
        if request.method == 'POST':
            parroquia = Parroquia.objects.filter(ciudad=request.POST['idC']).order_by('nombre')
            data = []
            for p in parroquia:
                data.append({
                    'idParroquia' : p.id,
                    'nombreP' : p.nombre
                })
            return HttpResponse(
                json.dumps(data),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

def cmbParentescoRepresentante(request):
    if request.is_ajax():
        parientes = Pariente.objects.all().values()
        return HttpResponse(
                    json.dumps(list(parientes)),
                    content_type = "application/json; charset=utf8"
                )
    else: raise Http404

def cambioClave(request):
    if request.is_ajax():
        estudiante = Estudiantes.objects.get(id=request.session["estudiante"]["id"])        
        usu = Usuario.objects.filter(usuario=request.POST['txtUsuario'])        
        usuario = Usuario.objects.get(id=estudiante.usuario_id)
        
        if usu.count() > 0: 
            if usu[0].id == estudiante.usuario_id:
                if usuario.clave == request.POST['txtClaveActual']:
                    usuario.usuario = request.POST['txtUsuario']
                    usuario.clave = request.POST['txtClaveNueva']
                    usuario.save()
                    return HttpResponse(
                        json.dumps({"mensaje":"no_mostrar"}),
                        content_type = "application/json; charset=utf8"
                    )
                else:
                    return HttpResponse(
                        json.dumps({"mensaje":"Error: La contraseña actual no es correcta"}),
                        content_type = "application/json; charset=utf8"
                    )
            else:
                return HttpResponse(
                        json.dumps({"mensaje":"Error: el nombre de usuario ya existe"}),
                        content_type = "application/json; charset=utf8"
                )
        else: 
            if usuario.clave == request.POST['txtClaveActual']:
                usuario.usuario = request.POST['txtUsuario']
                usuario.clave = request.POST['txtClaveNueva']
                usuario.save()
                return HttpResponse(
                    json.dumps({"mensaje":"no_mostrar"}),
                    content_type = "application/json; charset=utf8"
                )
            else:
                return HttpResponse(
                    json.dumps({"mensaje":"Error: La contraseña actual no es correcta"}),
                    content_type = "application/json; charset=utf8"
                )
                    
    else: raise Http404

def logueo(request):
    try:
        if request.POST:

            #request.session['id_usuario']=""
            usuario = Usuario.objects.filter(usuario=request.POST['txtUsuario'], clave=request.POST['txtClave'])
            if usuario.count() == 0:
                print "no encontrado"
                return HttpResponseRedirect("/logueo/")

            else:
                print "encontrado"
                tipo_usuario_id = usuario[0].tipo_usuario_id
                tipo_usuario = TipoUsuario.objects.get(id=tipo_usuario_id)

                if tipo_usuario.nombre == 'Estudiante': 
                    estudiante = Estudiantes.objects.get(usuario_id = usuario[0].id)

                    request.session["estudiante"]={
                        "id" : estudiante.id,
                        "nombre": estudiante.nombres,
                        "tipo_usuario_id" : tipo_usuario_id
                    }                  
                    return HttpResponseRedirect("/si/datos_personales1/")

                elif tipo_usuario.nombre.upper() == 'ADMINISTRADOR':
                    
                    empleados = Empleados.objects.get(usuario_id = usuario[0].id)
                    request.session["empleados"]={
                        "id" : empleados.id,
                        "nombre": empleados.nombres,
                        "tipo_usuario_id" : tipo_usuario_id
                    }                    
                  
                    return HttpResponseRedirect("/si/cargar_crear_usuario_admin/")

                elif tipo_usuario.nombre.upper() == 'DOBE':
                    
                    empleados = Empleados.objects.get(usuario_id = usuario[0].id)
                    request.session["empleados"]={
                        "id" : empleados.id,
                        "nombre": empleados.nombres,
                        "tipo_usuario_id" : tipo_usuario_id           
                    }
                    return HttpResponseRedirect("/si/listarUsuarioAdmin/")    

        else:
            return HttpResponseRedirect("/logueo/")
    except Exception, e:
        print e
        print "error en sesiones"
        return HttpResponseRedirect("/logueo/")

def cargaNombreEstudiante(request, template):
    #pais=Pais.objects.all()
    estudiante = Estudiantes.objects.get(id=request.session["estudiante"]["id"])
    usuario = Usuario.objects.get(id=estudiante.usuario_id)    
    return render(request, template,{
                 "nombre_usuario": usuario.usuario,
                 "mostrar":"no"
        })

def datos_personales(request):
    if request.POST:
        return HttpResponseRedirect("")
    else:
        return render(request,"datos_personales.html",{"nombre_usuario": request.session["estudiante"]["nombre"]})

def convertDate(strDate):
    if len(str(strDate)) == 0:
        return time.strftime("%Y-%m-%d")
    day, month, year = map(int, str(strDate).split("/"))
    return date(year, month, day).strftime("%Y-%m-%d")


def crearDireccion(calle_p,calle_s,num_casa,parroquia):
    crear_D=Direccion(
        calle_principal = calle_p,
        calle_secundaria = calle_s,
        numero_casa = num_casa,
        parroquia_id=int(parroquia),
        )
    crear_D.save()
    return crear_D.id

def editar_Direccion(id_d,calle_p,calle_s,num_casa,parroquia):
    edit=Direccion.objects.get(id=id_d)
    edit.calle_principal=calle_p
    edit.calle_secundaria=calle_s
    edit.numero_casa=num_casa
    edit.parroquia_id=int(parroquia)
    return edit.id

def crearRepresentante(calle_principal,parroquia,nivel_educacion,profesion_r,ocupacion_r,vive_estudiante_r,nombres_r,apellidos_r,cedula_r,telefono_r,movil_r,parentezco_r):
    addressR  = crearDireccion(calle_principal,"",99,parroquia)

    representante = Representante(
                    nombres = nombres_r,
                    apellidos = apellidos_r,
                    cedula = cedula_r,
                    telefono_convencional = telefono_r,
                    telefono_celular = movil_r,
                    pariente_id = int(parentezco_r),
                    nivel_educacion=nivel_educacion,
                    profesion = profesion_r,
                    ocupacion = ocupacion_r,
                    vive_estudiante = vive_estudiante_r ,
                    direccion_id = addressR
                )
    representante.save()
    return  representante.id

def editar_Representante(id_r,id_dir,calle_pr,parroquia_r,nombres_r,apellidos_r,cedula_r,telefono_r,movil_r,parentezco_r,nivel_educacion,profesion_r,ocupacion_r,vive_estudiante_r):
    addressR=editar_Direccion(id_dir,calle_pr,"",99,parroquia_r)
    edit=Representante.objects.get(id=id_r)
    edit.nombres = nombres_r,
    edit.apellidos = apellidos_r,
    edit.cedula = cedula_r,
    edit.telefono_convencional = telefono_r,
    edit.telefono_celular = movil_r,
    edit.pariente_id = int(parentezco_r),
    edit.nivel_educacion=nivel_educacion,
    edit.profesion = profesion_r,
    edit.ocupacion = ocupacion_r,
    edit.vive_estudiante = vive_estudiante_r ,
    edit.direccion_id = addressR
    return edit.id

def crearProgenitor(nombres_pro,apellidos_pro,cedula_pro,sexo_pro,convencional_pro,celular_pro,nivel_edu_pro,profesion_pro,ocupacion_pro, vive_es_pro,retirar_carpeta_pro):
    progenitor=Progenitores(
        nombres = nombres_pro,
        apellidos = apellidos_pro,
        cedula = cedula_pro,
        sexo = sexo_pro,
        telefono_convencional = convencional_pro,
        telefono_celular = celular_pro,
        nivel_educacion = nivel_edu_pro,
        profesion = profesion_pro,
        ocupacion = ocupacion_pro

    )
    progenitor.save()
    return progenitor.id

def editar_progenitor(nombres_pro,apellidos_pro,cedula_pro,sexo_pro,convencional_pro,celular_pro,nivel_edu_pro,profesion_pro,ocupacion_pro, vive_es_pro,retirar_carpeta_pro):
    progenitor_e=Progenitores.objects.get(cedula=cedula_pro)
    progenitor_e.nombres=nombres_pro
    progenitor_e.apellidos=apellidos_pro
    progenitor_e.sexo=sexo_pro
    progenitor_e.telefono_convencional=convencional_pro
    progenitor_e.telefono_celular=celular_pro
    progenitor_e.nivel_educacion=nivel_edu_pro
    progenitor_e.profesion=profesion_pro
    progenitor_e.ocupacion=ocupacion_pro
    progenitor_e.save()
    return progenitor_e.id

def editar_estudiante(id_user,nombre_e,apellidos_e,cedula_e,direccion,fecha_nac_e,nacionalidad,n_emergencia,p_id,r_id,sexo_e,convencional_e,movil_e,convencional_e_e,movil_e_e,observaciones_e):
    try:
        est=Estudiantes.objects.get(id=id_user)
        est.nombres=nombre_e
        est.apellidos=apellidos_e
        est.cedula=cedula_e
        est.direccion_id=direccion
        est.fecha_nacimiento=fecha_nac_e
        est.nacionalidad=nacionalidad
        est.nombres_persona_emergencia=n_emergencia
        est.progenitor_id=p_id
        est.representante_id=r_id
        est.sexo=sexo_e
        est.telefono_celular=movil_e
        est.telefono_convencional=convencional_e
        est.telefono_celular_e=movil_e_e
        est.telefono_convencional_e=convencional_e_e
        est.observaciones=observaciones_e
        est.primer_acceso=False
        print "*************************"
        est.save()
        print "*************************"
        return est.id

    except Exception, e:
        print e
    
def crearDetalleProgenitor(id_progenitor,id_estudiante,sexo_p,es_repre,es_huer,vive_est,retira_carp):
    crear=DetalleEstudiantesProgenitores(
        progenitores_id=id_progenitor,
        estudiantes_id=id_estudiante,
        sexo=sexo_p,
        es_representante=es_repre,
        es_huerfano=es_huer,
        vive_estudiante = vive_est,
        retira_carpeta_estudiantil = retira_carp
    )
    crear.save()

def editarDetalleProgenitor(id_estudiante):
    buscar=DetalleEstudiantesProgenitores.objects.filter(estudiantes_id=id_estudiante)
    for i in buscar:
        i.es_representante=False
        i.save()

def editarDetalleProgenitorRepresenta(id_estudiante,id_representante):
    buscar_progenitor=DetalleEstudiantesProgenitores.objects.filter(estudiantes_id=id_estudiante)
    for a in buscar_progenitor:
        if a.progenitores_id==id_representante:
            a.es_representante=True
            a.save()
        else:
            a.es_representante=False
            a.save()
def editar_detalles_bools(id_estudiante,id_progenitor,es_huerf,vive_est,retira_c):
    edit=DetalleEstudiantesProgenitores.objects.get(estudiantes_id=id_estudiante,progenitores_id=id_progenitor)
    edit.es_huerfano=es_huerf
    edit.vive_estudiante=vive_est
    edit.retira_carpeta_estudiantil=retira_c
    edit.save()

def registroAlumno(request):
        #parientes=Pariente.objects.all()
        #paises=Pais.objects.all().order_by('nombre')        
        estudiante_a=Estudiantes.objects.get(id=request.session["estudiante"]["id"])
        if request.is_ajax():
            if 'rdRetirarCarpetaP' in request.POST and request.POST['rdRetirarCarpetaP']=='Si':
                respuesta_carpeta_P=True
            else:
                respuesta_carpeta_P=False

            if 'rdRetirarCarpetaM' in request.POST and request.POST['rdRetirarCarpetaM']=='Si':
                respuesta_carpeta_M=True
            else:
                respuesta_carpeta_M=False

            if 'rdViveMadre' in request.POST and request.POST['rdViveMadre']=='Si':
                respuesta_vive_M=True
            else:
                respuesta_vive_M=False

            if 'rdVivePadre' in request.POST and request.POST['rdVivePadre']=='Si':
                respuesta_vive_P=True
            else:
                respuesta_vive_P=False            
            

            if 'chkHuerfanoPadre' in request.POST:
                huerfano_padre=True
                print "ES HUERFANO DE PADRE"
            else:
                huerfano_padre=False

            if 'chkHuerfanoMadre' in request.POST:
                huerfano_madre=True
                print "ES HUERFANO DE MADRE"
            else:
                huerfano_madre=False
          
            if request.POST and estudiante_a.primer_acceso:
                print "ES PRIMER ACCESO"
                addressE=crearDireccion(
                    request.POST['txtCallePrincipalE'],
                    request.POST['txtCalleSecundariaE'],
                    request.POST['txtNumeroCasaE'],
                    request.POST['cmbParroquiaE']
                )

                padre_b=Progenitores.objects.filter(cedula=request.POST['txtCedulaP'])

                if padre_b.count()==0:
                    id_padre = crearProgenitor(
                        request.POST['txtNombresP'],
                        request.POST['txtApellidosP'],
                        request.POST['txtCedulaP'],
                        "M",
                        request.POST['txtTelefonoConvencionalP'],
                        request.POST['txtTelefonoCelularP'],
                        request.POST['cmbNivelEducacionP'],
                        request.POST['txtProfesionP'],
                        request.POST['txtOcupacionP'],
                        respuesta_vive_P,
                        respuesta_carpeta_P
                    )


                else:
                    id_padre=editar_progenitor(
                        request.POST['txtNombresP'],
                        request.POST['txtApellidosP'],
                        request.POST['txtCedulaP'],
                        "M",
                        request.POST['txtTelefonoConvencionalP'],
                        request.POST['txtTelefonoCelularP'],
                        request.POST['cmbNivelEducacionP'],
                        request.POST['txtProfesionP'],
                        request.POST['txtOcupacionP'],
                        respuesta_vive_P,
                        respuesta_carpeta_P
                    )
                madre_b=Progenitores.objects.filter(cedula=request.POST['txtCedulaM'])
                if madre_b.count()==0:
                    id_madre = crearProgenitor(
                        request.POST['txtNombresM'],
                        request.POST['txtApellidosM'],
                        request.POST['txtCedulaM'],
                        "F",
                        request.POST['txtTelefonoConvencionalM'],
                        request.POST['txtTelefonoCelularM'],
                        request.POST.get('cmbNivelEducacionM',''),
                        request.POST['txtProfesionM'],
                        request.POST['txtOcupacionM'],
                        respuesta_vive_M,
                        respuesta_carpeta_M
                    )

                else:

                    id_madre=editar_progenitor(
                        request.POST['txtNombresM'],
                        request.POST['txtApellidosM'],
                        request.POST['txtCedulaM'],
                        "F",
                        request.POST['txtTelefonoConvencionalM'],
                        request.POST['txtTelefonoCelularM'],
                        request.POST.get('cmbNivelEducacionM',''),
                        request.POST['txtProfesionM'],
                        request.POST['txtOcupacionM'],
                        respuesta_vive_M,
                        respuesta_carpeta_M

                    )

                estudiante = Estudiantes.objects.get(id=request.session["estudiante"]["id"])

                if 'rdRepresentante' in request.POST:

                    if request.POST['rdRepresentante']=="Papi":
                        es_repre_papi=True
                        id_repre=id_padre
                    else:
                        es_repre_papi=False


                    if request.POST['rdRepresentante']=="Mami":
                        es_repre_mami=True
                        id_repre=id_madre
                    else:
                        es_repre_mami=False


                    if request.POST['rdRepresentante'] == 'Otros':

                        if request.POST['rdViveRepresentante']=="Si":
                            respuesta_vive_R=True
                        else:
                            respuesta_vive_R=False
                        representantes=Representante.objects.filter(cedula=request.POST['txtCedulaRepresentante'])
                       
                        if representantes.count()==0:
                            nuevo_representante=crearRepresentante(
                                request.POST['txtDireccionRepresentante'],
                                request.POST['cmbParroquiaE'],
                                request.POST['cmbNivelEducacionRepresentante'],
                                request.POST['txtProfesionRepresentante'],
                                request.POST['txtOcupacionRepresentante'],
                                respuesta_vive_R,
                                request.POST['txtNombresRepresentante'],
                                request.POST['txtApellidosRepresentante'],
                                request.POST['txtCedulaRepresentante'],
                                request.POST['txtTelefonoConvencionalR'],
                                request.POST['txtTelefonoMovilR'],
                                request.POST['cmbParentezcoRepresentante']
                            )
                        else:
                            nuevo_representante=editar_Representante(
                                representantes[0].id,
                                representantes[0].direccion_id,
                                request.POST['txtDireccionRepresentante'],
                                request.POST['cmbParroquiaE'],
                                request.POST['txtNombresRepresentante'],
                                request.POST['txtApellidosRepresentante'],
                                request.POST['txtCedulaRepresentante'],
                                request.POST['txtTelefonoConvencionalR'],
                                request.POST['txtTelefonoMovilR'],
                                request.POST['cmbParentezcoRepresentante'],
                                request.POST['cmbNivelEducacionRepresentante'],
                                request.POST['txtProfesionRepresentante'],
                                request.POST['txtOcupacionRepresentante'],
                                respuesta_vive_R
                            )
                     
                        print "==================================$$$$"
                        editar_estudiante(
                            request.session["estudiante"]["id"],
                            request.POST['txtNombresE'],
                            request.POST['txtApellidosE'],
                            request.POST['txtCedulaE'],
                            addressE,
                            convertDate(request.POST['txtFechaNacimientoE']),
                            request.POST.get('txtLugarNacimiento',''),
                            request.POST['txtNombresApellidosEmergenciaE'],
                            '',
                            nuevo_representante,
                            "",
                            request.POST['txtTelefonoConvencionalE'],
                            request.POST['txtTelefonoMovilE'],
                            request.POST['txtTelefonoConvencionalEmergenciaE'],
                            request.POST['txtTelefonoMovilEmergenciaE'],
                            "xyz"
                        )
                        print "==================================$$$$"

                        #return render(request,"datos_personales.html",{"nombre_usuario": request.session["user_name"],"mostrar":"ok","parientes":parientes})
                    else:
                        print "==========Esta Editando Estudiante porque no fue Representante Otros========="

                        editar_estudiante(
                            request.session["estudiante"]["id"],
                            request.POST['txtNombresE'],
                            request.POST['txtApellidosE'],
                            request.POST['txtCedulaE'],
                            addressE,
                            convertDate(request.POST.get('txtFechaNacimientoE','')),
                            request.POST.get('txtLugarNacimiento',''),
                            request.POST['txtNombresApellidosEmergenciaE'],
                            id_repre,
                            '',
                            "M",
                            request.POST['txtTelefonoConvencionalE'],
                            request.POST['txtTelefonoMovilE'],
                            request.POST['txtTelefonoConvencionalEmergenciaE'],
                            request.POST['txtTelefonoMovilEmergenciaE'],
                            "xyz"
                        )

                crearDetalleProgenitor(id_padre,estudiante.id,"M",es_repre_papi,huerfano_padre,respuesta_vive_P,respuesta_carpeta_P)
                crearDetalleProgenitor(id_madre,estudiante.id,"F",es_repre_mami,huerfano_madre,respuesta_vive_M,respuesta_carpeta_M)
                
                """return render(request,"datos_personales.html",{
                        "nombre_usuario": request.session["estudiante"]["nombre"],
                        "mostrar":"ok","parientes":parientes,
                        "paises":paises
                        })"""
                return HttpResponse(
                            json.dumps({'ok':True}),
                            content_type = "application/json; charset=utf8"
                        )

            else:
                if request.POST and not estudiante_a.primer_acceso:
                    
                    print "YA NO ES PRIMER ACCESO"
                    dir=editar_Direccion(
                        estudiante_a.direccion_id,
                        request.POST['txtCallePrincipalE'],
                        request.POST['txtCalleSecundariaE'],
                        request.POST['txtNumeroCasaE'],
                        request.POST['cmbParroquiaE']
                    )

                    progenitor_e=DetalleEstudiantesProgenitores.objects.filter(estudiantes_id=estudiante_a.id)
                    
                    for b in progenitor_e:
                        print "respuesta:::::"+str(respuesta_vive_P)
                        if str(b.sexo).upper()=='M':
                            request.session['proge_padre']=editar_progenitor(
                                request.POST['txtNombresP'],
                                request.POST['txtApellidosP'],
                                request.POST['txtCedulaP'],
                                "M",
                                request.POST['txtTelefonoConvencionalP'],
                                request.POST['txtTelefonoCelularP'],
                                request.POST['cmbNivelEducacionP'],
                                request.POST['txtProfesionP'],
                                request.POST['txtOcupacionP'],
                                respuesta_vive_P,
                                respuesta_carpeta_P
                            )
                            #print(estudiante_a.id,request.session['proge_padre'],huerfano_padre,respuesta_vive_P,respuesta_carpeta_P)
                            editar_detalles_bools(estudiante_a.id,request.session['proge_padre'],huerfano_padre,respuesta_vive_P,respuesta_carpeta_P)
                            
                        elif str(b.sexo).upper()=='F':
                            request.session['proge_madre']=editar_progenitor(
                                request.POST['txtNombresM'],
                                request.POST['txtApellidosM'],
                                request.POST['txtCedulaM'],
                                "F",
                                request.POST['txtTelefonoConvencionalM'],
                                request.POST['txtTelefonoCelularM'],
                                request.POST['cmbNivelEducacionM'],
                                request.POST['txtProfesionM'],
                                request.POST['txtOcupacionM'],
                                respuesta_vive_M,
                                respuesta_carpeta_M
                            )             
                            print respuesta_vive_M           
                            editar_detalles_bools(estudiante_a.id,request.session['proge_madre'],huerfano_madre,respuesta_vive_M,respuesta_carpeta_M)

                    print "###############################"
                    print request.POST['rdRepresentante']
                    
                    if 'rdRepresentante' in request.POST:
                        if request.POST['rdRepresentante']=='Otros':
                            ### crear un nuevo representante

                            editarDetalleProgenitor(estudiante_a.id)

                            if request.POST['rdViveRepresentante']=="Si":
                                respuesta_vive_R=True
                            else:
                                respuesta_vive_R=False

                            representante_veri=Representante.objects.filter(cedula=request.POST['txtCedulaRepresentante'])


                            if representante_veri.count()>0:
                                 nuevo_representante=editar_Representante(
                                    representante_veri[0].id,
                                    representante_veri[0].direccion_id,
                                    request.POST['txtDireccionRepresentante'],
                                    request.POST['cmbParroquiaE'],
                                    request.POST['txtNombresRepresentante'],
                                    request.POST['txtApellidosRepresentante'],
                                    request.POST['txtCedulaRepresentante'],
                                    request.POST['txtTelefonoConvencionalR'],
                                    request.POST['txtTelefonoMovilR'],
                                    request.POST['cmbParentezcoRepresentante'],
                                    request.POST['cmbNivelEducacionRepresentante'],
                                    request.POST['txtProfesionRepresentante'],
                                    request.POST['txtOcupacionRepresentante'],
                                    respuesta_vive_R
                                )

                            else:
                                nuevo_representante=crearRepresentante(
                                    request.POST['txtDireccionRepresentante'],request.POST['cmbParroquiaE'],request.POST['cmbNivelEducacionRepresentante'],
                                    request.POST['txtProfesionRepresentante'],request.POST['txtOcupacionRepresentante'],respuesta_vive_R,request.POST['txtNombresRepresentante'],
                                    request.POST['txtApellidosRepresentante'],request.POST['txtCedulaRepresentante'],request.POST['txtTelefonoConvencionalR'],request.POST['txtTelefonoMovilR'],
                                    request.POST['cmbParentezcoRepresentante']

                                )

                            editar_estudiante(
                                request.session["estudiante"]["id"],
                                request.POST['txtNombresE'],
                                request.POST['txtApellidosE'],
                                request.POST['txtCedulaE'],
                                dir,
                                convertDate(request.POST['txtFechaNacimientoE']),
                                request.POST['txtLugarNacimiento'],
                                request.POST['txtNombresApellidosEmergenciaE'],
                                '',
                                nuevo_representante,
                                "M",
                                request.POST['txtTelefonoConvencionalE'],
                                request.POST['txtTelefonoMovilE'],
                                request.POST['txtTelefonoConvencionalEmergenciaE'],
                                request.POST['txtTelefonoMovilEmergenciaE'],
                                "xyz"
                            )

                        else:

                            if request.POST['rdRepresentante']=='Papi':

                                progenitor_id=int(request.session['proge_padre'])

                            if request.POST['rdRepresentante']=='Mami':

                                progenitor_id=request.session['proge_madre']
                            
                            editar_estudiante(
                                request.session["estudiante"]["id"],
                                request.POST['txtNombresE'],
                                request.POST['txtApellidosE'],
                                request.POST['txtCedulaE'],
                                dir,
                                convertDate(request.POST['txtFechaNacimientoE']),
                                request.POST.get('txtLugarNacimiento',''),
                                request.POST['txtNombresApellidosEmergenciaE'],
                                progenitor_id,
                                '',
                                "M",
                                request.POST['txtTelefonoConvencionalE'],
                                request.POST['txtTelefonoMovilE'],
                                request.POST['txtTelefonoConvencionalEmergenciaE'],
                                request.POST['txtTelefonoMovilEmergenciaE'],
                                "xyz"
                            )
                            editarDetalleProgenitorRepresenta(estudiante_a.id,progenitor_id)



                        """return render(request,
                            "datos_personales.html",
                            {
                                "nombre_usuario": request.session["estudiante"]["nombre"],
                                "mostrar":"ok",
                                "parientes":parientes,
                                "paises":paises
                            })"""
                        return HttpResponse(
                            json.dumps({'ok':True}),
                            content_type = "application/json; charset=utf8"
                        )
                else:
                    """return render(request,
                            "datos_personales.html",
                            {
                                "nombre_usuario": request.session["estudiante"]["nombre"],
                                "mostrar":"no","parientes":parientes,
                                "paises":paises
                            })"""
                    return HttpResponse(
                            json.dumps({'ok':True}),
                            content_type = "application/json; charset=utf8"
                        )
        else: raise Http404
def generarMatricula(request):
    if request.POST:
        if 'cmbEspecialidad' in request.POST:
            det_cur_par_es = DetalleCursoParaleloEspecialidad.objects.get(
                cursos_id=request.POST['cmbCurso'], 
                paralelos_id=request.POST['cmbParalelo'], 
                especialidad_id=request.POST['cmbEspecialidad']
            )
        else:
            esp = Especialidad.objects.get(nombre='NINGUNA')       
            det_cur_par_es = DetalleCursoParaleloEspecialidad.objects.get(
                cursos_id=request.POST['cmbCurso'], 
                paralelos_id=request.POST['cmbParalelo'],
                especialidad=esp                   
            )

        mt = Matricula.objects.count()
        matricula = Matricula(
            det_cur_par_es = det_cur_par_es,
            estudiantes_id = request.session["estudiante"]["id"],
            fecha_matricula = convertDate(''),
            numero_matricula = int(mt)+1,
            modalidad = 'Presencial',
            seccion = request.POST['cmbSeccion'] 
        )
        matricula.save()
        return HttpResponse(
                json.dumps({"mensaje":"Su Matricula ha sido generada"}),
                content_type = "application/json; charset=utf8"
            )
    else:
        parametros = Parametros.objects.all().order_by('-id')      
        cargaForm = False
        parametros = parametros.values()
        fecha_inicio = parametros[0]['fecha_inicio_matriculas']
        fecha_fin = parametros[0]['fecha_fin_matriculas']
        fecha_actual = date.today()
        
        matricula = Matricula.objects.filter(estudiantes_id=request.session["estudiante"]["id"]).exists()
        
        if fecha_actual <= fecha_fin and fecha_actual >= fecha_inicio and not matricula:
            cargaForm = True
        return render(request,"generarMatricula.html",{
                   "nombre_usuario": request.session["estudiante"]["nombre"],
                   "cargaForm":cargaForm
            })

def cargarTablaHojaMatriculas(request):
    if request.is_ajax():
        cursor = connection.cursor()
        cursor.execute("SELECT periodo, curso, '--'||seccion||' '||paralelo, id_estudiante  FROM hoja_matricula_view WHERE id_estudiante=%s",(request.session['estudiante']['id'],))
        cur = cursor.fetchall()
        print cur
        cursor.close()
        return HttpResponse(
                json.dumps(cur,cls=DjangoJSONEncoder),
                content_type = "application/json; charset=utf8"
            )
    else: raise Http404

def cargar_datos(request, admin=False):
    
    if request.is_ajax():
        if request.method == 'POST':
            if admin :
                estudiantes = Estudiantes.objects.get(cedula=request.POST['cedula'])
            else:    
                estudiantes = Estudiantes.objects.get(id=request.session["estudiante"]["id"])
            
            if estudiantes.primer_acceso:
                estudiantes = estudiantes.__dict__
                del estudiantes['_state']
                return HttpResponse(json.dumps({"estudiantes":estudiantes,"origen":"Si"},cls = DjangoJSONEncoder),content_type = "application/json; charset=utf8")
            else:

                detalle=DetalleEstudiantesProgenitores.objects.filter(estudiantes_id=estudiantes.id)
                #id_representante=""
                print estudiantes.progenitor_id
                if estudiantes.progenitor_id!=None:
                    print "el repreentante es progenitor"
                    detalle_i=DetalleEstudiantesProgenitores.objects.filter(estudiantes_id=estudiantes.id,progenitores_id=estudiantes.progenitor_id)
                    detalle_i=detalle_i.values('sexo')
                elif estudiantes.representante_id!='':
                    print """========AQUI ESTA ==="""
                    #id_representante=estudiantes.representante_id 

                    request.session["estudiante"]["id_representante"]=estudiantes.representante_id                                       
                   
                direccion=Direccion.objects.filter(id=estudiantes.direccion_id)
                
                if direccion.count()>0:
                    parroquia=Parroquia.objects.filter(id=direccion[0].parroquia_id)
                    ciudad=Canton.objects.filter(id=parroquia[0].ciudad_id)
                    provincia=Provincia.objects.filter(id=ciudad[0].provincia_id)
                bandera=0
                for a in detalle:
                    if a.sexo=="M":
                        buscar_progenitor_padre=Progenitores.objects.filter(id=a.progenitores_id)
                        datos_papa=DetalleEstudiantesProgenitores.objects.filter(progenitores_id=a.progenitores_id,estudiantes_id=estudiantes.id)
                    else:
                        buscar_progenitor_madre=Progenitores.objects.filter(id=a.progenitores_id)
                        datos_mama=DetalleEstudiantesProgenitores.objects.filter(progenitores_id=a.progenitores_id,estudiantes_id=estudiantes.id)
                    if a.es_representante==True:
                        bandera+=1
                estudiantes = estudiantes.__dict__
                del estudiantes['_state']
                
                if bandera==0:

                    print "IF"                                   
                    representantes=Representante.objects.filter(id=int(request.session["estudiante"]["id_representante"]))
                    dir_rep = Direccion.objects.filter(id=representantes[0].direccion_id).values("calle_principal")
                    representantes=representantes.values()
                    
                    return HttpResponse(json.dumps({
                        "estudiantes":estudiantes,
                        "padre": list(buscar_progenitor_padre.values()),
                        "madre": list(buscar_progenitor_madre.values()),
                        "datos_papa": list(datos_papa.values()),
                        "datos_mama":list(datos_mama.values()),
                        "direccion": list(direccion.values()),
                        "representante":list(representantes),
                        "parroquia":list(parroquia.values('id')),
                        "ciudad":list(ciudad.values('id')),
                        "provincia": list(provincia.values('id')),
                        "dir_rep":list(dir_rep)},
                        cls = DjangoJSONEncoder
                        ),content_type = "application/json; charset=utf8"
                    )

                else:
                    print "ELSE"
                    return HttpResponse(
                        json.dumps({
                            "estudiantes":estudiantes,
                            "padre":list(buscar_progenitor_padre.values()),
                            "madre":list(buscar_progenitor_madre.values()),
                            "datos_papa":list(datos_papa.values()),
                            "datos_mama":list(datos_mama.values()),
                            "direccion":list(direccion.values()),
                            "representante":"No",
                            "parroquia":list(parroquia.values('id')),
                            "ciudad":list(ciudad.values('id')),
                            "provincia":list(provincia.values('id')),
                            "representante_p": list(detalle_i.values()) },
                            cls = DjangoJSONEncoder
                        ),content_type = "application/json; charset=utf8"
                    )
    else: raise Http404

def cerrarSesion(request, admin=False):
    if admin :
        del request.session["empleados"]
    else:
        del request.session["estudiante"]
    return HttpResponseRedirect("/logueo/")
    del request._cookies
    



