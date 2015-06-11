from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'principal.views.cargaPaginas', {'template':'index.html'}),

    url(r'^logueo/$', 'principal.views.cargaPaginas', {'template':'login.html'}),
    url(r'^login/$', 'principal.views.logueo'),
    
    url(r'^cerrarSesion/$', 'principal.views.cerrarSesion'),
    url(r'^cerrar_sesion/$', 'principal.views.cerrarSesion',{"admin":True}),
    url(r'^si/inicio/$', 'principal.views.cargaPaginas', {'template':'index_user.html'}),
    url(r'^si/datos_personales1/$', 'principal.views.cargaNombreEstudiante',{"template":"datos_personales.html"}),
    url(r'^si/datos_personales/$', 'principal.views.registroAlumno'),

    url(r'^si/datos_personales/cmb_pais/$', 'principal.views.cmbPais'),
    url(r'^si/datos_personales/cmb_provincias/$', 'principal.views.cmbProvincias'),
    url(r'^si/datos_personales/cmb_canton/$', 'principal.views.cmbCanton'),
    url(r'^si/datos_personales/cmb_parroquia/$', 'principal.views.cmbParroquia'),

    url(r'^si/datos_personales/cmb_parentesco/$', 'principal.views.cmbParentescoRepresentante'),


    url(r'^si/registro_matricula/$', 'principal.views.generarMatricula'),
    url(r'^si/registro_matricula/cmb_especialidad/$', 'principal.views.cmbEspecialidad'),
    url(r'^si/registro_matricula/cmb_cursos/$', 'principal.views.cmbCursos'),
    url(r'^si/registro_matricula/cmb_paralelos/$', 'principal.views.cmbParalelos'),
    url(r'^si/registro_matricula/cargar_datos/$', 'principal.views.cargar_datos'),
    
    url(r'^si/registro_matricula/maximo_disponible/$', 'principal.views.dispobiblesMaximos'),

    url(r'^si/generaMatricula/$', 'principal.views.generarMatricula'),

    url(r'^si/cargar_tipo_usuario/$', 'admins.views.cargarTipoUsuario'),
    url(r'^si/crear_usuario_admin/$', 'admins.views.crearUsuario'),
    
    #Filtros Listas Estudiantes
    url(r'^si/usuarios_admins/filtros_estudiantes/$', 'admins.views.filtrosEstudiantes'),
    

    url(r'^si/listarUsuarioAdmin/$', 'admins.views.cargarNombreUsuario',{"template":"listarUsuariosAdmin.html"}),

    #Cargar Acta de MAtricula
    url(r'^si/usuarios_admins/acta_matricula/$', 'admins.views.actaMatricula'),
    url(r'^si/edita_folio/$', 'admins.views.editaFolio'),

    #Cargar Datos Estudiantes lado Administrador
    url(r'^si/registro_matricula/admin_cargar_datos_estudiante/$', 'principal.views.cargar_datos', {"admin":True}),

    #Cargar Listas Estudiantes
    url(r'^si/verMatriculasAdmin/pages/(?P<pagin>\d+)$', 'admins.views.cargar_listas'),
    
    #Cargar Registro Estudiante
    url(r'^si/cargar_crear_usuario_admin/', 'admins.views.cargarNombreUsuario',{"template":"crear_usuario_admin.html"}),

    #Ver Hoja de Matricula
    url(r'^si/hoja_matricula/(?P<periodo>\d+)$','principal.views.to_pdf',name= "to_pdf"), 

    #Template verHojasMatricula.html
    url(r'^si/ver_hojas_matriculas/$','principal.views.cargaNombreEstudiante',{"template":"verHojasMatricula.html"}),
    #cargar Tabla Hojas Matricula
    url(r'^si/cargarTablaHojaMatriculas/$','principal.views.cargarTablaHojaMatriculas'),

    #Cambiar Clave
    url(r'^si/cambioClaveEstudiante/$','principal.views.cambioClave'),

    #Cargar crear Encuesta
    url(r'^si/crearEncuestasAdmin/$','admins.views.cargarNombreUsuario', {'template':'encuestasAdmin.html'}),
    
    
    #Guardar Encuesta
    url(r'^si/guardarEncuestaAdmin/$','admins.views.guardarEncuesta'),

    #Cargar Tipo Preeguntas
    url(r'^si/cargar_cmb_tipo_pregunta/$','admins.views.cmbTipoPregunta'),

    # urls le roi
    url(r'^si/cargar_tipo_usuario/$', 'admins.views.cargarTipoUsuario'),
    url(r'^si/cargar_crear_usuario/$', 'admins.views.cargarNombreUsuario', {'template':'crear_usuario_admin.html'}),
    url(r'^si/crear_usuario_admin/$', 'admins.views.crearUsuario'),


    url(r'^si/crear_cursope/$', 'admins.views.cargarNombreUsuario',{'template':'crear_cur_par_esp.html'}),
    url(r'^si/crear_cursope/cmbCurso/$', 'admins.views.cargarComboCurso'),  
    
        
    url(r'^si/crear_cursope/btnGuardarParroquia/$', 'admins.views.guardarParroquia'),
    
    url(r'^si/crear_cursope/cursos/$', 'admins.views.cargarNombreUsuario',{'template':'cursos.html'}),
    url(r'^si/crear_cursope/cursos/btnGuardarCurso/$', 'admins.views.guardarCurso'),
    url(r'^si/crear_cursope/cursos/btnModificarCurso/$', 'admins.views.modificarCurso'),    
    url(r'^si/crear_cursope/cursos/tablaCursos/$', 'admins.views.cargarComboCurso'),    
    
    url(r'^si/crear_cursope/paralelo/$', 'admins.views.cargarNombreUsuario',{'template':'paralelos.html'}),
    url(r'^si/crear_cursope/paralelo/cmbParalelos/$', 'admins.views.cargarComboParalelos'),
    url(r'^si/crear_cursope/paralelo/btnGuardarParalelo/$', 'admins.views.guardarParalelo'),
    url(r'^si/crear_cursope/paralelo/btnModificarParalelo/$', 'admins.views.modificarParalelo'),

    url(r'^si/crear_cursope/especialidad/$', 'admins.views.cargarNombreUsuario',{'template':'especialidad.html'}),
    url(r'^si/crear_cursope/cmbEspecialidad/$', 'admins.views.cargarEspecialidad'),
    url(r'^si/crear_cursope/especialidad/btnGuardarEspecialidad/$', 'admins.views.guardarEspecialidad'),
    url(r'^si/crear_cursope/especialidad/modificarEspecialidad/$', 'admins.views.modificarEspecialidad'),

    url(r'^si/crear_ppcp/pais/$', 'admins.views.cargarNombreUsuario',{'template':'pais.html'}),
    url(r'^si/crear_ppcp/pais/cargarTablaPais/$', 'admins.views.cargarPais'),
    url(r'^si/crear_ppcp/pais/btnGuardarPais/$', 'admins.views.guardarPais'),
    url(r'^si/crear_ppcp/pais/btnModificarPais/$', 'admins.views.modificarPais'),

    url(r'^si/crear_ppcp/provincia/$', 'admins.views.cargarNombreUsuario',{'template':'provincia.html'}),
    url(r'^si/crear_ppcp/provincia/cargarComboPais/$', 'admins.views.cargarPais'),
    url(r'^si/crear_ppcp/provincia/cargarTablaProvincia/$', 'admins.views.cargarProvincia'),
    url(r'^si/crear_ppcp/provincia/btnModificarProvincia/$', 'admins.views.modificarProvincia'),
    url(r'^si/crear_ppcp/provincia/btnGuardarProvincia/$', 'admins.views.guardarProvincia'),

    url(r'^si/crear_ppcp/canton/$','admins.views.cargarNombreUsuario',{'template':'canton.html'}),
    url(r'^si/crear_ppcp/canton/cargarTablaCanton/$','admins.views.cargarCanton'),
    url(r'^si/crear_ppcp/canton/cargarComboProvincia/$','admins.views.cargarProvincia'),
    url(r'^si/crear_ppcp/canton/guardarCanton/$', 'admins.views.guardarCanton'),
    url(r'^si/crear_ppcp/canton/modificarCanton/$', 'admins.views.modificarCanton'),

    url(r'^si/crear_ppcp/parroquia/$','admins.views.cargarNombreUsuario',{'template':'parroquia.html'}),
    url(r'^si/crear_ppcp/parroquia/cargarParroquia/$','admins.views.cargarParroquia'),
    url(r'^si/crear_ppcp/parroquia/cargarComboCanton/$','admins.views.cargarCanton'),
    url(r'^si/crear_ppcp/parroquia/guardarParroquia/$','admins.views.guardarParroquia'),
    url(r'^si/crear_ppcp/parroquia/modificarParroquia/$','admins.views.modificarParroquia'),

    url(r'^si/asignar_curso/$','admins.views.cargarNombreUsuario',{'template':'asignar.html'}),
    url(r'^si/asignar_curso/cargarParalelos/$','admins.views.cargarParalelosAsignacion'),
    url(r'^si/asignar_curso/cargarCursos/$','admins.views.cargarCursoAsignacion'),
    url(r'^si/asignar_curso/cargarEspecialidad/$','admins.views.cargarEspecialidadAsignacion'),
    url(r'^si/asignar_curso/guardarAsignacion/$','admins.views.guardarAsignar'),
    url(r'^si/asignar_curso/cargarAsignacion/$','admins.views.cargarAsignacion'),
    # end urls leroi

)

