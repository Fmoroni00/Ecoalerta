from flask import Flask, render_template, request
from datetime import datetime
import os  # Importamos el módulo os para acceder a las variables de entorno

# Configuración de la aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    reportes = []
    
    if request.method == "POST":
        # Obtener los datos del formulario
        ubicacion = request.form.get("ubicacion")
        descripcion = request.form.get("descripcion")
        
        # Validación de que ambos campos estén llenos
        if ubicacion and descripcion:
            # Fecha y hora actual para el reporte
            fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Simulamos el reporte (sin base de datos)
            reporte = {
                "ubicacion": ubicacion,
                "descripcion": descripcion,
                "fecha": fecha_reporte
            }
            reportes.append(reporte)
            
            # Después de agregar el reporte, redirigimos a la misma página para ver los nuevos datos
            return render_template("index.html", mensaje="Reporte agregado correctamente", reportes=reportes)
        else:
            # Si hay campos vacíos, mostrar un mensaje de error
            return render_template("index.html", error="Por favor, completa todos los campos.", reportes=reportes)

    return render_template("index.html", reportes=reportes)

# Ejecutar la aplicación
if __name__ == "__main__":
    # Configuramos el puerto a partir de la variable de entorno 'PORT' (para plataformas como Render) o 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
