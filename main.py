from flask import Flask, render_template_string, request
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

STYLE = '''
<style>
body {
    background: url('https://forhumancapital.mx/wp-content/uploads/2025/04/8.png') no-repeat center center fixed;
    background-size: cover;
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.container {
    max-width: 450px;
    margin: 80px auto;
    background-color: #1F1F1F;
    padding: 40px 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.container-wide {
    max-width: 90%;
    margin: 50px auto;
    background-color: #1F1F1F;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    overflow-x: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
table th {
    background-color: #1E90FF;
    color: #fff;
}
table tr:hover {
    background-color: #2A2A2A;
    transition: background-color 0.3s;
}
table th, td {
    vertical-align: middle;
    padding: 8px;
    border: 1px solid #444;
}
table button {
    padding: 6px 10px;
    background-color: #1E90FF;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}
table button:hover {
    background-color: #00BFFF;
    transform: scale(1.05);
}
.btn-ver {
    display: inline-block;
    padding: 6px 12px;
    background-color: #1E90FF;
    color: #fff;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s, transform 0.2s;
}
.btn-ver:hover {
    background-color: #00BFFF;
    transform: scale(1.05);
}
h1 {
    text-transform: uppercase;
    color: #00BFFF;
    text-align: center;
    margin-bottom: 30px;
}
h2 {
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}
.form-group label {
    margin-bottom: 4px;
    font-weight: bold;
}
.form-group input {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background-color: #2A2A2A;
    color: #fff;
}
label {
    margin-bottom: 6px;
    font-weight: bold;
}
input[type="text"], input[type="email"], input[type="password"] {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #444;
    background-color: #2A2A2A;
    color: #FFF;
    margin-bottom: 20px;
    transition: border 0.3s, background-color 0.3s;
    font-size: 14px;
}
input[type="text"]:focus, input[type="email"]:focus, input[type="password"]:focus {
    border-color: #00BFFF;
    background-color: #333;
    outline: none;
}
button {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background-color: #1E90FF;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}
button:hover {
    background-color: #00BFFF;
    transform: scale(1.02);
}
a {
    display: block;
    margin-top: 20px;
    text-align: center;
    color: #1E90FF;
    text-decoration: none;
    transition: color 0.3s;
}
a:hover {
    color: #00BFFF;
}
.file-upload {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}
.file-upload input[type="file"] {
    border: 1px solid #FFFFFF;
    border-radius: 10px;
    padding: 6px 10px;
    background-color: #2A2A2A;
    color: #FFFFFF;
    cursor: pointer;
}
.file-upload input[type="file"]::-webkit-file-upload-button {
    border: none;
    background: #1E90FF;
    color: #fff;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
}
.file-upload input[type="file"]::-webkit-file-upload-button:hover {
    background-color: #00BFFF;
}
</style>
'''

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Enviar WhatsApp - FOR Human Capital</title>
    {{ style|safe }}
</head>
<body>
    <div class="container-wide">
        <h1>Enviar WhatsApps desde Excel</h1>
        <form method="post" enctype="multipart/form-data">
            <div class="file-upload">
                <input type="file" name="file" accept=".xlsx,.csv" required>
                <button type="submit">Subir y Procesar</button>
            </div>
        </form>
        {% if columnas %}
            <form method="post">
                <input type="hidden" name="filepath" value="{{ filepath }}">
                <div class="form-group">
                    <label for="columna">Selecciona la columna con los números:</label>
                    <select name="columna" required>
                        {% for col in columnas %}
                        <option value="{{ col }}">{{ col }}</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit">Mostrar contactos</button>
            </form>
        {% endif %}
        {% if contactos %}
            <table>
                <thead>
                    <tr>
                        {% for col in contactos[0].keys() %}<th>{{ col }}</th>{% endfor %}
                        <th>WhatsApp</th>
                    </tr>
                </thead>
                <tbody>
                    {% for fila in contactos %}
                        <tr>
                            {% for val in fila.values() %}<td>{{ val }}</td>{% endfor %}
                            <td>
                                <a class="btn-ver" target="_blank" href="https://wa.me/{{ fila[columna] }}">Chat</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    columnas, contactos, columna = None, None, None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            ext = filename.rsplit('.', 1)[-1].lower()
            df = pd.read_excel(filepath) if ext == 'xlsx' else pd.read_csv(filepath)
            columnas = df.columns.tolist()
            return render_template_string(HTML_TEMPLATE, columnas=columnas, filepath=filepath, style=STYLE)

        elif 'filepath' in request.form and 'columna' in request.form:
            filepath = request.form['filepath']
            columna = request.form['columna']
            ext = filepath.rsplit('.', 1)[-1].lower()
            df = pd.read_excel(filepath) if ext == 'xlsx' else pd.read_csv(filepath)
            contactos = df.fillna('').to_dict(orient='records')
            columnas = df.columns.tolist()
            return render_template_string(HTML_TEMPLATE, contactos=contactos, columna=columna, columnas=columnas, style=STYLE)

    return render_template_string(HTML_TEMPLATE, style=STYLE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
