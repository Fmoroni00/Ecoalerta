from flask import Flask, render_template, request
from datetime import datetime
import os  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reportes = []
    
    if request.method == "POST":
        ubicacion = request.form.get("ubicacion")
        descripcion = request.form.get("descripcion")
        
        if ubicacion and descripcion:
            fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            reporte = {
                "ubicacion": ubicacion,
                "descripcion": descripcion,
                "fecha": fecha_reporte
            }
            reportes.append(reporte)
            
            return render_template("index.html", mensaje="Reporte agregado correctamente", reportes=reportes)
        else:
            return render_template("index.html", error="Por favor, completa todos los campos.", reportes=reportes)

    return render_template("index.html", reportes=reportes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
