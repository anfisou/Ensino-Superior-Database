import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
#import flask
from flask import abort, render_template,Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS universidades FROM UNIVERSIDADE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS faculdades FROM FACULDADE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS cursos FROM CURSO').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS reitores FROM REITOR').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS distritos FROM DISTRITO').fetchone()
    stats.update(x)
    logging.info(stats)
    return render_template('index.html',stats=stats)


# Universidades
@APP.route('/universidades/')
def list_universidades():
    universidade = db.execute(
      '''
      SELECT UniversidadeId, UniversidadeNome , Email, Telefone, Morada 
      FROM UNIVERSIDADE
      ORDER BY UniversidadeNome
      ''').fetchall()
    return render_template('universidade-list.html', universidades=universidade)

@APP.route('/universidades/<int:id>/')
def get_universidade(id):
  universidade = db.execute(
      '''
      SELECT UniversidadeId, UniversidadeNome , Email, Telefone, Morada 
      FROM UNIVERSIDADE
      WHERE UniversidadeId = %s
      ''', id).fetchone()

  if universidade is None:
     abort(404, 'Universidade id {} does not exist.'.format(id))

  reitor = db.execute(
      '''
      SELECT ReitorId, ReitorNome 
      FROM UNIVERSIDADE NATURAL JOIN REITOR
      WHERE UniversidadeId = %s 
      ''', id).fetchall()

  distrito = db.execute(
      '''
      SELECT DistritoId, DistritoNome
      FROM UNIVERSIDADE NATURAL JOIN DISTRITO
      WHERE UniversidadeId = %s
      ''', id).fetchall()

  faculdades = db.execute(
      '''
      SELECT FaculdadeId, FaculdadeNome
      FROM UNIVERSIDADE NATURAL JOIN FACULDADE
      WHERE UniversidadeId = %s
      ''', id).fetchall()

  return render_template('universidade.html', 
           universidade=universidade, reitor=reitor, distrito=distrito,faculdades = faculdades)

@APP.route('/universidades/search/<expr>/')
def search_universidade(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  universidades = db.execute(
      ''' 
      SELECT UniversidadeId, UniversidadeNome
      FROM UNIVERSIDADE
      WHERE UniversidadeNome LIKE %s
      ORDER BY UniversidadeNome
      ''', expr).fetchall()
  if len(universidades)==0:
    expr = expr[1:-1]
    abort(404, 'Faculdade {} does not exist.'.format(expr))

  return render_template('universidade-search.html',
           search=search,universidades=universidades)


@APP.route('/faculdades/')
def list_faculdades():
    faculdades = db.execute(
      '''
      SELECT FaculdadeId,FaculdadeNome, TipoEnsino , Natureza, UniversidadeNome
      FROM FACULDADE NATURAL JOIN UNIVERSIDADE
      ORDER BY FaculdadeNome
      ''').fetchall()
    return render_template('faculdade-list.html', faculdades=faculdades)

@APP.route('/faculdades/<int:id>/')
def get_faculdade(id):
  faculdade = db.execute(
      '''
      SELECT FaculdadeId, FaculdadeNome , TipoEnsino, Natureza
      FROM FACULDADE
      WHERE FaculdadeId = %s
      ''', id).fetchone()

  if faculdade is None:
     abort(404, 'Faculdade id {} does not exist.'.format(id))

  universidade = db.execute(
      '''
      SELECT UniversidadeId, UniversidadeNome 
      FROM UNIVERSIDADE NATURAL JOIN FACULDADE
      WHERE FaculdadeId = %s 
      ''', id).fetchall()

  cursos = db.execute(
      '''
      SELECT CursoId, CursoNome,Grau,CursoFaculdadeId
      FROM CURSO NATURAL JOIN CURSO_FACULDADE NATURAL JOIN FACULDADE
      WHERE FaculdadeId = %s
      ORDER BY Grau, CursoNome
      ''', id).fetchall()

  return render_template('faculdade.html', 
           faculdade = faculdade,universidade=universidade, cursos=cursos)

@APP.route('/faculdades/search/<expr>/')
def search_faculdade(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  faculdades = db.execute(
      ''' 
      SELECT FaculdadeId, FaculdadeNome, UniversidadeNome
      FROM UNIVERSIDADE NATURAL JOIN FACULDADE
      WHERE FaculdadeNome LIKE %s
      ORDER BY FaculdadeNome
      ''', expr).fetchall()

  if len(faculdades)==0:
    expr = expr[1:-1]
    abort(404, 'Faculdade {} does not exist.'.format(expr))

  return render_template('faculdade-search.html',
           search=search,faculdades=faculdades)


@APP.route('/cursos/')
def list_cursos():
    cursos = db.execute(
      '''
      SELECT CursoId,CursoNome,Grau
      FROM CURSO
      ORDER BY CursoNome
      ''').fetchall()
    return render_template('curso-list.html', cursos=cursos)

@APP.route('/cursos/<int:id>/')
def get_curso(id):
  curso = db.execute(
      '''
      SELECT CursoId, CursoNome , Grau
      FROM CURSO
      WHERE CursoId = %s
      ''', id).fetchone()

  if curso is None:
     abort(404, 'Curso id {} does not exist.'.format(id))

  faculdade = db.execute(
      '''
      SELECT FaculdadeId, FaculdadeNome, UniversidadeNome, CursoFaculdadeId
      FROM UNIVERSIDADE NATURAL JOIN FACULDADE NATURAL JOIN CURSO_FACULDADE NATURAL JOIN CURSO
      WHERE CursoId = %s 
      ''', id).fetchall()

  return render_template('curso.html', 
           curso=curso,faculdade = faculdade)

@APP.route('/cursos/search/<expr>/')
def search_curso(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  cursos = db.execute(
      ''' 
      SELECT CursoId, CursoNome, Grau
      FROM CURSO
      WHERE CursoNome LIKE %s
      ORDER BY CursoNome
      ''', expr).fetchall()
  if len(cursos)==0:
    expr = expr[1:-1]
    abort(404, 'Faculdade {} does not exist.'.format(expr))

  return render_template('curso-search.html',
           search=search,cursos=cursos)

@APP.route('/distritos/<int:id>/')
def get_distrito(id):
  distrito = db.execute(
      '''
      SELECT DistritoId, DistritoNome , Regiao
      FROM DISTRITO
      WHERE DistritoId = %s
      ''', id).fetchone()

  if distrito is None:
     abort(404, 'Distrito id {} does not exist.'.format(id))

  universidades = db.execute(
      '''
      SELECT UniversidadeId, UniversidadeNome
      FROM UNIVERSIDADE NATURAL JOIN DISTRITO
      WHERE DistritoId = %s 
      ''', id).fetchall()
  size = len(universidades)
  return render_template('distrito.html', 
           distrito=distrito,universidades=universidades,size = size)


@APP.route('/distritos/')
def list_distritos():
    distritos = db.execute(
      '''
      SELECT DistritoId,DistritoNome,Regiao
      FROM DISTRITO
      ORDER BY DistritoNome
      ''').fetchall()
    return render_template('distrito-list.html', distritos=distritos)

@APP.route('/distritos/search/<expr>/')
def search_distrito(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  distritos = db.execute(
      ''' 
      SELECT DistritoId,DistritoNome
      FROM DISTRITO
      WHERE DistritoNome LIKE %s
      ORDER BY DistritoNome
      ''', expr).fetchall()
  if len(distritos)==0:
    expr = expr[1:-1]
    abort(404, 'Faculdade {} does not exist.'.format(expr))

  return render_template('distrito-search.html',
           search=search,distritos=distritos)

@APP.route('/reitor/<int:id>/')
def get_reitor(id):
  reitor = db.execute(
      '''
      SELECT ReitorId, ReitorNome , Sexo
      FROM REITOR
      WHERE ReitorId = %s
      ''', id).fetchone()

  universidade = db.execute(
      '''
      SELECT UniversidadeId,UniversidadeNome
      FROM REITOR NATURAL JOIN UNIVERSIDADE
      WHERE ReitorId = %s
      ''', id).fetchone()

  if reitor is None:
     abort(404, 'Reitor id {} does not exist.'.format(id))

  return render_template('reitor.html', 
           reitor=reitor,universidade=universidade)

@APP.route('/reitor/')
def list_reitores():
    reitores = db.execute(
      '''
      SELECT ReitorId,ReitorNome,Sexo
      FROM REITOR
      ORDER BY ReitorNome
      ''').fetchall()
    return render_template('reitor-list.html', reitores=reitores)

@APP.route('/reitor/search/<expr>/')
def search_reitor(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  reitores = db.execute(
      ''' 
      SELECT ReitorId,ReitorNome
      FROM REITOR
      WHERE ReitorNome LIKE %s
      ORDER BY ReitorNome
      ''', expr).fetchall()
  if len(reitores)==0:
    expr = expr[1:-1]
    abort(404, 'Faculdade {} does not exist.'.format(expr))

  return render_template('reitor-search.html',
           search=search,reitores=reitores)

@APP.route('/cursofaculdade/<int:id>')
def get_curso_faculdade(id):
  curso_faculdade = db.execute(
      '''
      SELECT NumeroTotalInscritos,MediaFinal,Idade24Menos,Idade25Mais,NumeroHomens,NumeroMulheres
      FROM CURSO_FACULDADE
      WHERE CursoFaculdadeId = %s 
      ''', id).fetchone()

  if curso_faculdade is None:
     abort(404, 'Reitor id {} does not exist.'.format(id))

  faculdade = db.execute(
      '''
      SELECT FaculdadeId,FaculdadeNome
      FROM CURSO_FACULDADE NATURAL JOIN FACULDADE
      WHERE CursoFaculdadeId = %s 
      ''', id).fetchone()

  curso = db.execute(
      '''
      SELECT CursoId,CursoNome
      FROM CURSO_FACULDADE NATURAL JOIN CURSO
      WHERE CursoFaculdadeId = %s
      ''', id).fetchone()

  if curso_faculdade is None:
     abort(404, 'Reitor id {} does not exist.'.format(id))

  return render_template('curso_faculdade.html', 
     curso_faculdade = curso_faculdade,faculdade=faculdade,curso=curso)