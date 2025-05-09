from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate
from forms import LibroForm

app = Flask(__name__)


USER_DB = 'duss02_n5pc_user'
USER_PASSWORD = 'Ud3Fge3HxTPmiQsBP9I17kxjN7wnnlqX'
SERVER_DB = 'dpg-d0cneg2dbo4c73fl11s0-a.oregon-postgres.render.com'
NAME_DB = 'Prueba'
FULL_URL_DB = f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SECRET_KEY'] = 'llave_secreta'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Libro(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True)
    autor: Mapped[str]
    editorial: Mapped[str]

    def __str__(self):
        return (
            f'ID: {self.id} '
            f'Título: {self.titulo} '
            f'Autor: {self.autor} '
            f'Editorial: {self.editorial}'
        )

@app.route('/')
def inicio():
    libros = Libro.query.all()
    total_libros = Libro.query.count()
    libroForm = LibroForm()  
    libroFormEditar = LibroForm()  
    return render_template('index.html', total=total_libros, datos=libros, 
                         formulario=libroForm, formulario_editar=libroFormEditar)

@app.route('/libro/<int:id>')
def ver_libro(id):
    libro = Libro.query.get(id)
    return render_template('libro.html', dato=libro)

@app.route('/insertar-libro', methods=['GET', 'POST'])
def insertar_libro():
    libro = Libro()
    libroForm = LibroForm(obj=libro)
    
    if libroForm.validate_on_submit():
        libroForm.populate_obj(libro)
        db.session.add(libro)
        db.session.commit()
        return redirect(url_for('inicio'))
    
    libros = Libro.query.all()
    total_libros = Libro.query.count()
    return render_template('index.html', total=total_libros, datos=libros, formulario=libroForm)

@app.route('/eliminar-libro/<int:id>')
def eliminar_libro(id):
    libro = Libro.query.get(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('inicio'))

@app.route('/editar-libro/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    libro = Libro.query.get_or_404(id)
    libroForm = LibroForm(obj=libro)

    if libroForm.validate_on_submit():
        libroForm.populate_obj(libro)
        db.session.commit()
        return redirect(url_for('inicio'))
    
    libros = Libro.query.all()
    total_libros = Libro.query.count()
    return render_template('index.html', total=total_libros, datos=libros, 
                         formulario=LibroForm(), formulario_editar=libroForm)