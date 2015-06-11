from django.db import models
#from django.contrib.auth.models import User

class Persona(models.Model):
    nombres   = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cedula    = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1)
    telefono_convencional = models.CharField(max_length=10,null=True)
    telefono_celular      = models.CharField(max_length=10,null=True)
    email = models.EmailField()
    class Meta:
        abstract = True

class Pais(models.Model):
    nombre = models.CharField(max_length=255)

class Provincia(models.Model):
    nombre = models.CharField(max_length=255)
    pais   = models.ForeignKey(Pais)   

class Canton(models.Model):
    nombre    = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia)

class Parroquia(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Canton)

class Direccion(models.Model):
    calle_principal = models.CharField(max_length=255)
    calle_secundaria = models.CharField(max_length=255)
    numero_casa = models.IntegerField()
    parroquia=models.ForeignKey(Parroquia)

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(models.Model):
    usuario   = models.CharField(max_length=25)
    clave     = models.CharField(max_length=16)
    tipo_usuario = models.ForeignKey(TipoUsuario)

class Empleados(Persona):
    direccion = models.ForeignKey(Direccion, null=True)
    usuario = models.ForeignKey(Usuario)

class Progenitores(Persona):
    nivel_educacion = models.CharField(max_length=50)
    profesion = models.CharField(max_length=150, null=True)
    ocupacion = models.CharField(max_length=150)

class Pariente(models.Model):
    nombre = models.CharField(max_length=100)

class Representante(Persona):
    ocupacion = models.CharField(max_length=255)
    pariente = models.ForeignKey(Pariente, null=True)
    nivel_educacion = models.CharField(max_length=50)
    profesion = models.CharField(max_length=150, null=True)
    ocupacion = models.CharField(max_length=150)
    vive_estudiante = models.BooleanField(default=False)
    direccion = models.ForeignKey(Direccion)

class Cursos(models.Model):
    descripcion = models.CharField(max_length=255)
    estado      = models.BooleanField(default=True)


class Paralelos(models.Model):
    descripcion = models.CharField(max_length=1)
    estado      = models.BooleanField(default=True)

class Especialidad(models.Model):
    nombre      = models.CharField(max_length=150)
    estado      = models.BooleanField(default=True)

class DetalleCursoParaleloEspecialidad(models.Model):
    cursos       = models.ForeignKey(Cursos)
    especialidad = models.ForeignKey(Especialidad, null=True)
    paralelos    = models.ForeignKey(Paralelos)
    cupos_disponibles = models.IntegerField()
    maximo_cupos = models.IntegerField()

class Estudiantes(Persona):
    direccion = models.ForeignKey(Direccion, null=True) 
    fecha_nacimiento   = models.DateField(null=True)
    nacionalidad = models.CharField(max_length=250, default="Ecuador")
    nombres_persona_emergencia = models.CharField(max_length=255, null=True)
    observaciones = models.CharField(max_length=10, null=True)
    progenitor = models.ForeignKey(Progenitores , null=True)
    primer_acceso=models.BooleanField(default=True)
    representante = models.ForeignKey(Representante, null=True)
    telefono_convencional_e = models.CharField(max_length=10, null=True)
    telefono_celular_e = models.CharField(max_length=10, null=True)
    usuario=models.ForeignKey(Usuario)

class DetalleEstudiantesProgenitores(models.Model):
    progenitores = models.ForeignKey(Progenitores)
    estudiantes = models.ForeignKey(Estudiantes)
    sexo = models.CharField(max_length=1)
    es_representante=models.BooleanField(default=False)
    es_huerfano=models.BooleanField(default=False)
    vive_estudiante = models.BooleanField(default=False)
    retira_carpeta_estudiantil = models.BooleanField(default=False)

class Matricula(models.Model):
    det_cur_par_es = models.ForeignKey(DetalleCursoParaleloEspecialidad)
    estudiantes = models.ForeignKey(Estudiantes)
    fecha_matricula = models.DateField()
    numero_matricula = models.IntegerField()
    modalidad = models.CharField(max_length=155)
    seccion = models.CharField(max_length=50)
    folio = models.IntegerField(null=True)
    tipo_matricula = models.CharField(max_length=50,default='Ordinaria')

class Institucion(models.Model):
    nombre       = models.CharField(max_length=255)
    email        = models.EmailField()
    mision       = models.TextField()
    vision       = models.TextField()
    convencional = models.CharField(max_length=10)
    celular      = models.CharField(max_length=10)
    direccion    = models.ForeignKey(Direccion)

class Parametros(models.Model):
    fecha_inicio_matriculas = models.DateField()
    fecha_fin_matriculas = models.DateField()

class EncuestasGraduados(models.Model):
    tema = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    #estudiante = models.ForeignKey(Estudiantes)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

class TipoPregunta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

class Preguntas(models.Model):
    descripcion = models.CharField(max_length=450)
    encuestas_graduados = models.ForeignKey(EncuestasGraduados)
    tipo_pregunta = models.ForeignKey(TipoPregunta)

class OpcionesPreguntas(models.Model):
    descripcion = models.TextField(null=True)
    another_option = models.BooleanField(default=False) #para saber si la respuesta es de tipo texto

class DetallePreguntasOpciones(models.Model):
    preguntas = models.ForeignKey(Preguntas)
    opciones = models.ForeignKey(OpcionesPreguntas)
    descripcion = models.TextField(null=True)
    respuesta = models.BooleanField(default=False)

class DetalleEstudianteEncuesta(models.Model):
    estudiante = models.ForeignKey(Estudiantes)
    encuesta = models.ForeignKey(EncuestasGraduados)


    




