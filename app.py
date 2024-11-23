from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoalerta.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar advertencias de modificaciones
db = SQLAlchemy(app)

# Definición del modelo de la base de datos
class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Reporte {self.id} - {self.ubicacion}>'

# Crear las tablas de la base de datos si no existen
with app.app_context():
    db.create_all()

# Ruta principal
@app.route("/templates", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener los datos del formulario
        ubicacion = request.form.get("ubicacion")
        descripcion = request.form.get("descripcion")
        
        # Validación de que ambos campos estén llenos
        if ubicacion and descripcion:
            # Fecha y hora actual para el reporte
            fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Crear un nuevo reporte en la base de datos
            nuevo_reporte = Reporte(ubicacion=ubicacion, descripcion=descripcion, fecha=fecha_reporte)
            db.session.add(nuevo_reporte)
            db.session.commit()
            # Después de agregar el reporte, redirigimos a la misma página para ver los nuevos datos
            return render_template("index.html", mensaje="Reporte agregado correctamente", reportes=Reporte.query.all())
        else:
            # Si hay campos vacíos, mostrar un mensaje de error
            return render_template("index.html", error="Por favor, completa todos los campos.", reportes=Reporte.query.all())

    # Obtener todos los reportes registrados
    reportes = Reporte.query.all()
    return render_template("index.html", reportes=reportes)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
