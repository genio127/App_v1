import http.server
import socketserver
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_filename = os.path.join(BASE_DIR, "posicion.png")
img_base64 = ""

if os.path.exists(img_filename):
    with open(img_filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        img_base64 = f"data:image/png;base64,{encoded_string}"
    print(f"[*] Imagen cargada e incrustada correctamente.")
else:
    print(f"[!] ADVERTENCIA: No se encontró la imagen '{img_filename}'.")

HTML_CONTENT = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluación de Calidad - Clinchados</title>
    <style>
        /* Colorimetría Volkswagen Aplicada */
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #A8A8A8; margin: 0; padding: 20px; color: #1F2F57; }}
        .container {{ max-width: 950px; margin: auto; background: #FDFAF9; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border-top: 8px solid #1F2F57; }}
        h1, h2, h3 {{ color: #1F2F57; text-align: center; }}
        .section {{ margin-bottom: 25px; padding: 15px; border: 1px solid #A8A8A8; border-radius: 8px; background-color: #FDFAF9; }}
        .visual-panel {{ background-color: #FDFAF9; border: 2px solid #6091C3; }} 
        label {{ display: block; margin-top: 10px; font-weight: bold; font-size: 0.85em; color: #1F2F57; }}
        input[type="text"], input[type="number"], input[type="email"], input[type="password"], input[type="date"], select {{ 
            width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #A8A8A8; border-radius: 5px; box-sizing: border-box; font-size: 0.85em; background-color: #FDFAF9; color: #1F2F57;
        }}
        .instructions {{ background-color: #FDFAF9; border-left: 4px solid #6091C3; border-top: 1px solid #A8A8A8; border-right: 1px solid #A8A8A8; border-bottom: 1px solid #A8A8A8; padding: 10px; font-size: 0.9em; margin-bottom: 15px; color: #1F2F57; }}
        .flex-row {{ display: flex; gap: 15px; flex-wrap: wrap; align-items: flex-start; }}
        .flex-col {{ flex: 1; min-width: 300px; }}
        .calc-box {{ background: #A8A8A8; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; margin-top: 15px; border: 1px solid #1F2F57; color: #1F2F57; }}
        .btn {{ background-color: #6091C3; color: #FDFAF9; border: none; padding: 12px 20px; font-size: 1em; cursor: pointer; border-radius: 5px; width: 100%; margin-top: 20px; font-weight: bold; transition: 0.3s; }}
        .btn:hover {{ background-color: #1F2F57; color: #FDFAF9; }}
        .nok-panel {{ border: 1px solid #6091C3; background-color: #FDFAF9; padding: 15px; border-radius: 5px; margin-top: 10px; }}
        .advice {{ color: #1F2F57; font-weight: bold; text-align: center; font-size: 1.2em; padding: 20px; border: 3px solid #1F2F57; margin-top: 20px; background: #A8A8A8; display: none; text-transform: uppercase; }}
        .ref-img {{ max-width: 150px; display: block; margin-top: 8px; margin-bottom: 8px; border: 1px solid #A8A8A8; border-radius: 4px; background: #FDFAF9; padding: 4px; box-shadow: 1px 1px 4px rgba(0,0,0,0.2); }}
        .subsection-title {{ color: #6091C3; font-size: 1em; margin-top: 20px; margin-bottom: 5px; border-bottom: 1px solid #A8A8A8; padding-bottom: 5px; }}
        .help-text {{ font-weight: normal; font-size: 0.9em; color: #1F2F57; display: block; margin-top: 3px; line-height: 1.2; }}
    </style>
</head>
<body>

<div class="container">
    <h1>Inspección de Matriz de Clinchado</h1>
    
    <form id="clinchadoForm">
        <!-- SECCIÓN 1 -->
        <div class="section">
            <h2>1. Credenciales de Envío</h2>
            <div class="instructions">
                <strong>Notas sobre la Contraseña de Aplicación:</strong><br>
                • <strong>Institucional (@gob.com.mx, Office 365):</strong> Generar contraseña desde el portal corporativo.<br>
                • <strong>Gmail / Hotmail / Yahoo:</strong> Configúralo desde "Seguridad en 2 pasos".
            </div>
            <div class="flex-row">
                <div class="flex-col">
                    <label>Tu Correo Electrónico:</label>
                    <input type="email" id="userEmail" required placeholder="ejemplo@dominio.com">
                </div>
                <div class="flex-col">
                    <label>Contraseña de Aplicación:</label>
                    <input type="password" id="userPassword" required>
                </div>
            </div>
            <label>Correo del Supervisor (Destinatario):</label>
            <input type="email" id="supervisorEmail" required>
        </div>

        <!-- SECCIÓN 2 -->
        <div class="section">
            <h2>2. Información del Ensamble</h2>
            <div class="flex-row">
                <div class="flex-col"><label>Inspector / Operador:</label><input type="text" id="inspector" required></div>
                <div class="flex-col"><label>Fecha de Envío:</label><input type="date" id="fecha" required></div>
            </div>
            <div class="flex-row">
                <div class="flex-col"><label>Automóvil Evaluado:</label><input type="text" id="auto" required placeholder="Ej. Jetta A7"></div>
                <div class="flex-col"><label>Parte de la Carrocería:</label><input type="text" id="parte" required placeholder="Ej. Ensamble Tapa Trasera Interior"></div>
            </div>
            <div class="flex-row">
                <div class="flex-col"><label>Veces que han regresado el informe:</label><input type="number" id="vecesRegresado" required min="0" value="0"></div>
            </div>
        </div>

        <!-- SECCIÓN 3 -->
        <div class="section">
            <h2>3. Resumen de Puntos de Clinchado</h2>
            <div class="flex-row">
                <div class="flex-col"><label>Total de Clinchados Evaluados:</label><input type="number" id="totalClinchados" required min="1" value="10" oninput="calcularOK()"></div>
                <div class="flex-col"><label>Clinchados NOK (Mal):</label><input type="number" id="nokCount" required min="0" value="0" oninput="calcularOK()"></div>
                <div class="flex-col"><label>Clinchados COK (Condicionales):</label><input type="number" id="cokCount" required min="0" value="0" oninput="calcularOK()"></div>
            </div>

            <div class="calc-box">
                <p>Clinchados OK (Sin errores): <span id="okVal" style="font-size:1.5em; color:#1F2F57;">10</span></p>
                <p>Total de veces cortado el ensamble: <span id="totalCortesVal" style="font-size:1.2em; color:#1F2F57;">0</span></p>
                <p>Porcentaje de Efectividad: <span id="porcentajeVal" style="font-size:1.2em; color:#1F2F57;">100.0%</span></p>
            </div>
        </div>

        <!-- SECCIÓN 4 -->
        <div class="section" id="sec4Container" style="display: none;">
            <h2>4. Verificado de Clinchados</h2>
            <div id="nokContainer"></div>
        </div>

        <!-- SECCIÓN 5 -->
        <div class="section visual-panel">
            <h2>5. Verificación visual de clinchados</h2>
            <div class="flex-row">
                <div class="flex-col">
                    <label>1. Punto de unión existente:</label>
                    <select id="v_punto_union">
                        <option>Inexistente (NOK)</option>
                        <option selected>Existente (OK)</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>2. Posición: 
                        {f'<img src="{img_base64}" class="ref-img">' if img_base64 else '<small style="color:#1F2F57;">[Falta imagen]</small>'}
                    </label>
                    <select id="v_posicion">
                        <option>Desviación de posición mayor que la especificación (NOK)</option>
                        <option selected>Según dibujo (OK)</option>
                    </select>
                </div>
            </div>
            <div class="flex-row">
                <div class="flex-col">
                    <label>3. Cuello agrietado:</label>
                    <select id="v_cuello">
                        <option>Existente (NOK)</option>
                        <option selected>Inexistente (OK)</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>4. Ruptura de materiales:</label>
                    <select id="v_ruptura">
                        <option>Existente (NOK)</option>
                        <option selected>Inexistente (OK)</option>
                    </select>
                </div>
            </div>
            <div class="flex-row">
                <div class="flex-col">
                    <label>5. Grietas en el Cuello (Interior):</label>
                    <select id="v_grietas_int">
                        <option>Existente (NOK)</option>
                        <option selected>Inexistente (OK)</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>6. Muescas:</label>
                    <select id="v_muescas">
                        <option>La muesca se encuentra descentrada y tiene forma irregular (NOK)</option>
                        <option selected>La muesca está centrada y es distinguible (OK)</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- SECCIÓN 6 -->
        <div class="section">
            <h2>6. Módulos</h2>
            <div class="flex-row">
                <div class="flex-col">
                    <label>¿El punzón cumple con sus funciones?</label>
                    <select id="mod_punzon">
                        <option value="Si" selected>Sí</option>
                        <option value="No">No</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>¿La matriz cumple con sus funciones?</label>
                    <select id="mod_matriz">
                        <option value="Si" selected>Sí</option>
                        <option value="No">No</option>
                    </select>
                </div>
            </div>
        </div>

        <button type="submit" class="btn" id="btnSubmit">ENVIAR INFORME AL SUPERVISOR</button>
        <div id="feedbackContainer" class="advice"></div>
    </form>
</div>

<script>
    document.getElementById('fecha').valueAsDate = new Date();

    function calcularOK() {{
        const total = parseInt(document.getElementById('totalClinchados').value) || 0;
        const nok = parseInt(document.getElementById('nokCount').value) || 0;
        const cok = parseInt(document.getElementById('cokCount').value) || 0;
        const regresos = parseInt(document.getElementById('vecesRegresado').value) || 0;
        
        const ok = total - nok - cok;
        document.getElementById('okVal').innerText = ok;
        document.getElementById('totalCortesVal').innerText = regresos;

        let porcentaje = 100;
        if (total > 0) {{
            porcentaje = (ok / total) * 100;
        }} else {{
            porcentaje = 0;
        }}
        
        document.getElementById('porcentajeVal').innerText = porcentaje.toFixed(1) + '%';
        generarPanelesNOK(nok);
        document.getElementById('feedbackContainer').style.display = 'none';
    }}

    document.getElementById('vecesRegresado').addEventListener('input', calcularOK);

    function generarPanelesNOK(cantidad) {{
        const sec4 = document.getElementById('sec4Container');
        const container = document.getElementById('nokContainer');
        container.innerHTML = '';
        
        if(cantidad > 0) {{
            sec4.style.display = 'block';
            for(let i = 1; i <= cantidad; i++) {{
                const panel = document.createElement('div');
                panel.className = 'nok-panel flex-row';
                panel.innerHTML = `
                    <div class="flex-col">
                        <label>Pieza Errónea #${{i}} (Nombre/No. de Parte):</label>
                        <input type="text" class="nok-parte" placeholder="Ej. ZSB Refuerzo bisagra" required>
                    </div>
                    <div class="flex-col">
                        <label>Estado:</label>
                        <select class="nok-estado" style="background-color: #FDFAF9; color: #1F2F57; border-color: #A8A8A8;">
                            <option>Mal (NOK)</option>
                        </select>
                    </div>
                `;
                container.appendChild(panel);
            }}
        }} else {{
            sec4.style.display = 'none';
        }}
    }}

    document.getElementById('clinchadoForm').addEventListener('submit', async function(e) {{
        e.preventDefault();
        const btn = document.getElementById('btnSubmit');
        btn.innerText = 'EVALUANDO...';
        btn.disabled = true;

        const data = {{
            userEmail: document.getElementById('userEmail').value,
            userPass: document.getElementById('userPassword').value,
            supervisor: document.getElementById('supervisorEmail').value,
            inspector: document.getElementById('inspector').value,
            fecha: document.getElementById('fecha').value,
            auto: document.getElementById('auto').value,
            parte: document.getElementById('parte').value,
            vecesRegresado: document.getElementById('vecesRegresado').value,
            totalClinchados: document.getElementById('totalClinchados').value,
            nokCount: document.getElementById('nokCount').value,
            cokCount: document.getElementById('cokCount').value,
            okCount: document.getElementById('okVal').innerText,
            totalCortes: document.getElementById('totalCortesVal').innerText,
            porcentaje: document.getElementById('porcentajeVal').innerText,
            
            piezasMalas: [],
            
            v_punto_union: document.getElementById('v_punto_union').value,
            v_posicion: document.getElementById('v_posicion').value,
            v_cuello: document.getElementById('v_cuello').value,
            v_ruptura: document.getElementById('v_ruptura').value,
            v_grietas_int: document.getElementById('v_grietas_int').value,
            v_muescas: document.getElementById('v_muescas').value,
            
            mod_punzon: document.getElementById('mod_punzon').value,
            mod_matriz: document.getElementById('mod_matriz').value
        }};

        const nokPanels = document.querySelectorAll('.nok-panel');
        nokPanels.forEach(panel => {{
            data.piezasMalas.push({{
                nombre: panel.querySelector('.nok-parte').value,
                estado: panel.querySelector('.nok-estado').value
            }});
        }});

        try {{
            const response = await fetch('/enviar_correo', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(data) }});
            const result = await response.json();
            if(response.ok) {{
                const fbDiv = document.getElementById('feedbackContainer');
                fbDiv.style.display = 'block';
                fbDiv.innerHTML = result.feedback;
                fbDiv.scrollIntoView({{ behavior: 'smooth' }});
                alert('✅ Reporte enviado exitosamente.');
            }} else {{ alert('❌ Error: ' + result.error); }}
        }} catch (error) {{ alert('❌ Error de conexión.'); }}
        btn.innerText = 'ENVIAR INFORME AL SUPERVISOR';
        btn.disabled = false;
    }});
</script>
</body>
</html>
'''

class ClinchadoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/enviar_correo':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))

            fallo_modulo = data['mod_punzon'] == 'No' or data['mod_matriz'] == 'No'
            fallo_visual = ('NOK' in data['v_punto_union'] or 
                            'NOK' in data['v_posicion'] or 
                            'NOK' in data['v_cuello'] or 
                            'NOK' in data['v_ruptura'] or 
                            'NOK' in data['v_grietas_int'] or
                            'NOK' in data['v_muescas'])
                            
            nok_count = int(data.get('nokCount', 0))

            if fallo_modulo or fallo_visual:
                dictamen = "DESGASTE CRÍTICO / FUERA DE TOLERANCIA (CAMBIAR MATRIZ)"
                bg_color = "#A8A8A8" # Gris neutral
            elif nok_count > 0:
                dictamen = "DESGASTE INICIAL / PRECAUCIÓN (Aumentar frecuencia de inspección)"
                bg_color = "#A8A8A8" # Gris neutral
            else:
                dictamen = "CONDICIÓN ÓPTIMA / ACEPTABLE (Continuar Proceso)"
                bg_color = "#A8A8A8" # Gris neutral

            try:
                self.enviar_email(data, dictamen, bg_color)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok", 
                    "feedback": dictamen,
                    "bg_color": bg_color
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def enviar_email(self, data, dictamen, bg_color):
        
        user_email = data['userEmail'].lower()
        if 'gmail.com' in user_email:
            smtp_host = 'smtp.gmail.com'
        elif 'hotmail.' in user_email or 'outlook.' in user_email or 'live.' in user_email:
            smtp_host = 'smtp-mail.outlook.com'
        elif 'yahoo.' in user_email:
            smtp_host = 'smtp.mail.yahoo.com'
        elif 'gob.com.mx' in user_email or 'gob.mx' in user_email:
            smtp_host = 'smtp.office365.com'
        else:
            smtp_host = 'smtp.office365.com'

        msg = MIMEMultipart()
        msg['From'], msg['To'] = data['userEmail'], data['supervisor']
        msg['Subject'] = f"Reporte de Clinchados: {data['parte']} - {data['auto']}"

        piezas_html = ""
        if len(data['piezasMalas']) > 0:
            piezas_html = "<ul>"
            for p in data['piezasMalas']:
                piezas_html += f"<li><strong>{p['nombre']}</strong> - Estado: <span style='color:#1F2F57;'>{p['estado']}</span></li>"
            piezas_html += "</ul>"
        else:
            piezas_html = "<p style='color:#1F2F57; font-weight:bold;'>No se reportaron piezas erróneas.</p>"

        html = f'''<html><body style="font-family: Arial, sans-serif; color: #1F2F57; background-color: #FDFAF9; padding: 20px;">
            <h2 style="color: #6091C3;">Inspección de Matriz de Clinchado</h2>
            
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #A8A8A8;">
                <tr><td bgcolor="#FDFAF9"><strong>Inspector:</strong></td><td>{data['inspector']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>Fecha:</strong></td><td>{data['fecha']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>Automóvil:</strong></td><td>{data['auto']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>Parte:</strong></td><td>{data['parte']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>Regresos:</strong></td><td>{data['vecesRegresado']}</td></tr>
            </table>
            
            <h3 style="color: #1F2F57; border-bottom: 1px solid #A8A8A8; padding-bottom: 5px;">Resumen de Clinchados</h3>
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #A8A8A8;">
                <tr bgcolor="#1F2F57" style="color: #FDFAF9;">
                    <th>Total Evaluados</th><th>OK</th><th>COK</th><th>NOK</th><th>Veces Cortado</th><th>Efectividad</th>
                </tr>
                <tr style="text-align: center; background-color: #FDFAF9;">
                    <td>{data['totalClinchados']}</td>
                    <td style="color: #1F2F57; font-weight: bold;">{data['okCount']}</td>
                    <td>{data['cokCount']}</td>
                    <td style="color: #1F2F57; font-weight: bold;">{data['nokCount']}</td>
                    <td>{data['totalCortes']}</td>
                    <td><strong>{data['porcentaje']}</strong></td>
                </tr>
            </table>

            <h3 style="color: #1F2F57; border-bottom: 1px solid #A8A8A8; padding-bottom: 5px;">4. Verificado de Clinchados</h3>
            {piezas_html}

            <h3 style="color: #1F2F57; border-bottom: 1px solid #A8A8A8; padding-bottom: 5px;">5. Verificación Visual de Clinchados</h3>
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #A8A8A8;">
                <tr><td bgcolor="#FDFAF9" width="40%"><strong>1. Punto de unión existente:</strong></td><td>{data['v_punto_union']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>2. Posición:</strong></td><td>{data['v_posicion']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>3. Cuello agrietado:</strong></td><td>{data['v_cuello']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>4. Ruptura de materiales:</strong></td><td>{data['v_ruptura']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>5. Grietas en el Cuello (Interior):</strong></td><td>{data['v_grietas_int']}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>6. Muescas:</strong></td><td>{data['v_muescas']}</td></tr>
            </table>

            <h3 style="color: #1F2F57; border-bottom: 1px solid #A8A8A8; padding-bottom: 5px;">6. Módulos</h3>
            <ul>
                <li>¿El punzón cumple con sus funciones? <strong style="color: #1F2F57;">{data['mod_punzon']}</strong></li>
                <li>¿La matriz cumple con sus funciones? <strong style="color: #1F2F57;">{data['mod_matriz']}</strong></li>
            </ul>
            
            <br>
            <div style="border: 3px solid #1F2F57; padding: 20px; text-align: center; background-color: {bg_color};">
                <span style="color: #1F2F57; font-weight: bold; font-size: 1.5em; text-transform: uppercase;">
                    {dictamen}
                </span>
            </div>
        </body></html>'''
        msg.attach(MIMEText(html, 'html'))
        
        server = smtplib.SMTP(smtp_host, 587)
        server.starttls()
        server.login(data['userEmail'], data['userPass'])
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))
    print(f"Servidor iniciado en el puerto {PORT}")
    
    # Esta es la instrucción clave que evita el error [Errno 98] Address already in use
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), ClinchadoHandler) as httpd:
        httpd.serve_forever()