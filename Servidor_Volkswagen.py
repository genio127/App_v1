import http.server
import socketserver
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import webbrowser
import os
import base64

os.chdir(os.path.dirname(os.path.abspath(__file__)))

img_base64 = ""
img_filename = "posicion.png"

if os.path.exists(img_filename):
    with open(img_filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        img_base64 = f"data:image/png;base64,{encoded_string}"
    print(f"[*] Imagen '{img_filename}' cargada e incrustada correctamente.")
else:
    print(f"[!] ADVERTENCIA: No se encontró la imagen '{img_filename}' en la misma carpeta.")

HTML_CONTENT = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluación de Calidad - Clinchados</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 950px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        h1, h2, h3 {{ color: #0056b3; text-align: center; }}
        .section {{ margin-bottom: 25px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background-color: #fafafa; }}
        label {{ display: block; margin-top: 10px; font-weight: bold; font-size: 0.85em; color: #555; }}
        input[type="text"], input[type="number"], input[type="email"], input[type="password"], input[type="date"], select {{ 
            width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; font-size: 0.85em;
        }}
        .instructions {{ background-color: #e9f5ff; border-left: 4px solid #0056b3; padding: 10px; font-size: 0.9em; margin-bottom: 15px; }}
        .flex-row {{ display: flex; gap: 15px; flex-wrap: wrap; align-items: flex-start; }}
        .flex-col {{ flex: 1; min-width: 300px; }}
        .calc-box {{ background: #d4edda; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; margin-top: 15px; border: 1px solid #c3e6cb; }}
        .btn {{ background-color: #0056b3; color: white; border: none; padding: 12px 20px; font-size: 1em; cursor: pointer; border-radius: 5px; width: 100%; margin-top: 20px; font-weight: bold; transition: 0.3s; }}
        .btn:hover {{ background-color: #004494; }}
        .nok-panel {{ border: 1px solid #f5c6cb; background-color: #f8d7da; padding: 20px; border-radius: 5px; margin-top: 15px; }}
        .nok-panel h4 {{ margin-top: 0; color: #721c24; border-bottom: 1px solid #f5c6cb; padding-bottom: 10px; }}
        .advice {{ color: black; font-weight: bold; text-align: center; font-size: 1.2em; padding: 20px; border: 3px solid black; margin-top: 20px; background: #fff3cd; display: none; text-transform: uppercase; }}
        .ref-img {{ max-width: 150px; display: block; margin-top: 8px; margin-bottom: 8px; border: 1px solid #aaa; border-radius: 4px; background: white; padding: 4px; box-shadow: 1px 1px 4px rgba(0,0,0,0.2); }}
        .subsection-title {{ color: #0056b3; font-size: 1em; margin-top: 20px; margin-bottom: 5px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
        .help-text {{ font-weight: normal; font-size: 0.9em; color: #666; display: block; margin-top: 3px; line-height: 1.2; }}
    </style>
</head>
<body>

<div class="container">
    <h1>Inspección de Matriz de Clinchado</h1>
    
    <form id="clinchadoForm">
        <div class="section">
            <h2>1. Credenciales de Envío</h2>
            <div class="flex-row">
                <div class="flex-col">
                    <label>Tu Correo Electrónico (Gmail):</label>
                    <input type="email" id="userEmail" required placeholder="ejemplo@gmail.com">
                </div>
                <div class="flex-col">
                    <label>Contraseña de Aplicación:</label>
                    <input type="password" id="userPassword" required>
                </div>
            </div>
            <label>Correo del Supervisor (Destinatario):</label>
            <input type="email" id="supervisorEmail" required>
        </div>

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
                <div class="flex-col"><label>ID de Matriz (Anillo/Punzón):</label><input type="text" id="idMatriz" required></div>
                <div class="flex-col"><label>Espesor total de láminas (t) en mm:</label><input type="number" step="0.01" id="espesor" required></div>
            </div>
            <div class="flex-row">
                <div class="flex-col"><label>Veces que han regresado el informe:</label><input type="number" id="vecesRegresado" required min="0" value="0"></div>
            </div>
        </div>

        <div class="section">
            <h2>3. Resumen de Puntos de Clinchado</h2>
            <div class="flex-row">
                <div class="flex-col"><label>Total de Clinchados Evaluados:</label><input type="number" id="totalClinchados" required min="1" value="10" oninput="calcularOK()"></div>
                <div class="flex-col"><label>Clinchados NOK (Mal):</label><input type="number" id="nokCount" required min="0" value="0" oninput="calcularOK()"></div>
                <div class="flex-col"><label>Clinchados COK (Condicionales):</label><input type="number" id="cokCount" required min="0" value="0" oninput="calcularOK()"></div>
            </div>

            <div class="calc-box">
                <p>Clinchados OK (Sin errores): <span id="okVal" style="font-size:1.5em; color:#155724;">10</span></p>
                <p>Total de veces cortado el ensamble: <span id="totalCortesVal" style="font-size:1.2em;">0</span></p>
                <p>Porcentaje de Efectividad (OK vs Cortes): <span id="porcentajeVal" style="font-size:1.2em;">100%</span></p>
            </div>
        </div>

        <div id="nokContainer"></div>

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
        if (ok + regresos > 0) {{
            porcentaje = (ok / (ok + regresos)) * 100;
        }} else if (regresos > 0 && ok === 0) {{
            porcentaje = 0;
        }}
        document.getElementById('porcentajeVal').innerText = porcentaje.toFixed(1) + '%';
        generarPanelesNOK(nok);
        document.getElementById('feedbackContainer').style.display = 'none';
    }}

    document.getElementById('vecesRegresado').addEventListener('input', calcularOK);

    function generarPanelesNOK(cantidad) {{
        const container = document.getElementById('nokContainer');
        container.innerHTML = '';
        if(cantidad > 0) {{
            const heading = document.createElement('h2');
            heading.innerText = '4. Detalles de Clinchados NOK (Características)';
            container.appendChild(heading);
        }}

        const imagenBase64 = "{img_base64}";
        let imgTag = imagenBase64 !== "" ? `<img src="${{imagenBase64}}" alt="Referencia de Posición" class="ref-img">` : `<small style="color:red;">[Falta imagen]</small>`;

        for(let i = 1; i <= cantidad; i++) {{
            const panel = document.createElement('div');
            panel.className = 'nok-panel';
            panel.innerHTML = `
                <h4>Clinchado NOK #${{i}}</h4>
                <label>Número de parte (Ej. ZSB Refuerzo bisagra izquierda - 57N.827.177):</label>
                <input type="text" class="nok-parte" required>
                
                <div class="subsection-title">Características Externas</div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>1. Punto de unión existente:</label>
                        <select class="nok-q1"><option>Inexistente (NOK)</option><option>Existente (OK)</option></select>
                    </div>
                    <div class="flex-col">
                        <label>2. Posición: ${{imgTag}}</label>
                        <select class="nok-q2">
                            <option>Desviación de posición mayor que la especificación (NOK)</option>
                            <option>Según dibujo (OK)</option>
                        </select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>3. Cuello agrietado:</label>
                        <select class="nok-q3"><option>Existente (NOK)</option><option>Inexistente (OK)</option></select>
                    </div>
                    <div class="flex-col">
                        <label>4. Ruptura de materiales:</label>
                        <select class="nok-q4"><option>Existente (NOK)</option><option>Inexistente (OK)</option></select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>5. Espesor de fondo (tb):</label>
                        <select class="nok-q5">
                            <option>No está dentro de la especificación de tolerancia (NOK)</option>
                            <option>Dentro de la especificación de tolerancia (OK)</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label>6. Diámetro externo (d):</label>
                        <select class="nok-q6">
                            <option>d > d0 +2.0 mm o d < d0 -1.0 mm (NOK)</option>
                            <option>d = d0 +2.0 mm / -1.0 mm (OK)</option>
                        </select>
                    </div>
                </div>

                <div class="subsection-title">Características Internas</div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>7. Muesca (f1, f2) - Matrices Rígidas:
                        <span class="help-text">* f medido desde el pto. más interno del componente preperforado (A) hasta la protuberancia (B); se permiten columnas.</span></label>
                        <select class="nok-q7">
                            <option>NOK: Menor a los límites permitidos según d0</option>
                            <option>OK: ≥0,1mm (d0<4) | ≥0,03mm (d0<6) | ≥0,05mm (d0≥6)</option>
                            <option>No aplica</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label>8. Muesca (f1, f2) - Matrices Segmentos Móviles:
                        <span class="help-text">* f medido desde el pto. más interno del componente preperforado (A) hasta la protuberancia (B); se permiten columnas.</span></label>
                        <select class="nok-q8">
                            <option>NOK: Menor a los límites permitidos según d0</option>
                            <option>OK: ≥0,1mm (d0<4) | f1,f2≥0,03 y Prom≥0,08 (d0<6) | f1,f2≥0,05 y Prom≥0,10 (d0≥6)</option>
                            <option>No aplica</option>
                        </select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>9. Espesor del Cuello (tn1, tn2):</label>
                        <select class="nok-q9">
                            <option>NOK: Menor a los límites permitidos según d0</option>
                            <option>OK: ≥0,15mm (d0<4) | tn≥0,10 y Prom≥0,15 (d0<6) | tn≥0,15 y Prom≥0,20 (d0≥6)</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label>10. Espesor mín. material residual - Lado punzón (tST min):</label>
                        <select class="nok-q10">
                            <option>NOK: tST min < 0,05 mm</option>
                            <option>COK: 0,05 ≤ tST < 0,08 (d0<6) | 0,05 ≤ tST < 0,10 (d0≥6)</option>
                            <option>OK: tST min ≥ 0,08 mm (d0<6) | tST min ≥ 0,10 mm (d0≥6)</option>
                        </select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>11. Espesor mín. material residual - Lado matriz (tM, min):</label>
                        <select class="nok-q11">
                            <option>NOK: tM, min < 0,05 mm</option>
                            <option>COK: 0,05 ≤ tM < 0,08 (d0<6) | 0,05 ≤ tM < 0,10 (d0≥6)</option>
                            <option>OK: tM, min ≥ 0,08 mm (d0<6) | tM, min ≥ 0,10 mm (d0≥6)</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label>12. Grietas en el Cuello (Interior):</label>
                        <select class="nok-q12">
                            <option>Existente (NOK)</option>
                            <option>Inexistente (OK)</option>
                        </select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>13. Grietas lado del troquel (área de estampado XR):</label>
                        <select class="nok-q13">
                            <option>XR > 0,2 mm (NOK)</option>
                            <option>XR ≤ 0,2 mm (OK)</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label>14. Grietas en el lado de la matriz:</label>
                        <select class="nok-q14">
                            <option>NOK: tM, min < 0,05 mm</option>
                            <option>COK: 0,05 ≤ tM < 0,08 (d0<6) | 0,05 ≤ tM < 0,10 (d0≥6)</option>
                            <option>OK: tM, min ≥ 0,08 mm (d0<6) | tM, min ≥ 0,10 mm (d0≥6)</option>
                        </select>
                    </div>
                </div>
                <div class="flex-row">
                    <div class="flex-col">
                        <label>15. Altura de socavado (fy1, fy2) - EXCLUSIVO PARA d0 < 4mm:
                        <span class="help-text">* fy medido verticalmente desde el filo (S) del componente preperforado hasta el soporte máximo de la base del troquel.</span></label>
                        <select class="nok-q15">
                            <option>NOK: fy1, fy2 < 0,1 mm (d0<4)</option>
                            <option>OK: fy1, fy2 ≥ 0,1 mm (d0<4)</option>
                            <option>No aplica (d0 ≥ 4mm)</option>
                        </select>
                    </div>
                </div>

                <div class="subsection-title" style="color: #d35400;">Características de Fuerza (Pruebas Destructivas)</div>
                <div class="flex-row" style="background-color: #fff9e6; padding: 10px; border-radius: 5px; border: 1px solid #f2e2bd;">
                    <div class="flex-col">
                        <label style="color: #b56500;">16. Resistencia a la cizalladura (Fs):</label>
                        <select class="nok-q16">
                            <option>NOK: Fs < Fs, min</option>
                            <option>OK: Fs ≥ Fs, min</option>
                            <option>No evaluado / No aplica</option>
                        </select>
                    </div>
                    <div class="flex-col">
                        <label style="color: #b56500;">17. Fuerza de tracción (Ffuerza):</label>
                        <select class="nok-q17">
                            <option>NOK: Ffuerza < Ffuerza, min</option>
                            <option>OK: Ffuerza ≥ Ffuerza, min</option>
                            <option>No evaluado / No aplica</option>
                        </select>
                    </div>
                </div>
            `;
            container.appendChild(panel);
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
            idMatriz: document.getElementById('idMatriz').value,
            espesor: document.getElementById('espesor').value,
            vecesRegresado: document.getElementById('vecesRegresado').value,
            totalClinchados: document.getElementById('totalClinchados').value,
            nokCount: document.getElementById('nokCount').value,
            cokCount: document.getElementById('cokCount').value,
            okCount: document.getElementById('okVal').innerText,
            totalCortes: document.getElementById('totalCortesVal').innerText,
            porcentaje: document.getElementById('porcentajeVal').innerText,
            nokDetails: []
        }};

        const nokPanels = document.querySelectorAll('.nok-panel');
        nokPanels.forEach(panel => {{
            data.nokDetails.push({{
                parteNum: panel.querySelector('.nok-parte').value,
                union: panel.querySelector('.nok-q1').value,
                posicion: panel.querySelector('.nok-q2').value,
                cuello: panel.querySelector('.nok-q3').value,
                ruptura: panel.querySelector('.nok-q4').value,
                espesorFondo: panel.querySelector('.nok-q5').value,
                diametro: panel.querySelector('.nok-q6').value,
                muescaR: panel.querySelector('.nok-q7').value,
                muescaM: panel.querySelector('.nok-q8').value,
                espesorCuello: panel.querySelector('.nok-q9').value,
                residualP: panel.querySelector('.nok-q10').value,
                residualM: panel.querySelector('.nok-q11').value,
                grietaInt: panel.querySelector('.nok-q12').value,
                grietaTroquel: panel.querySelector('.nok-q13').value,
                grietaMatriz: panel.querySelector('.nok-q14').value,
                socavado: panel.querySelector('.nok-q15').value,
                cizalladura: panel.querySelector('.nok-q16').value,
                traccion: panel.querySelector('.nok-q17').value
            }});
        }});

        try {{
            const response = await fetch('/enviar_correo', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(data) }});
            const result = await response.json();
            if(response.ok) {{
                const fbDiv = document.getElementById('feedbackContainer');
                fbDiv.style.display = 'block';
                fbDiv.innerHTML = `DICTAMEN DEL SISTEMA:<br><br>${{result.feedback}}`;
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

            nok_count, cok_count = int(data.get('nokCount', 0)), int(data.get('cokCount', 0))
            if nok_count > 0:
                dictamen, bg_color = "DESGASTE CRÍTICO / FUERA DE TOLERANCIA (Cambiar Matriz)", "#f8d7da"
            elif cok_count > 0:
                dictamen, bg_color = "DESGASTE INICIAL / PRECAUCIÓN (Aumentar frecuencia de inspección)", "#fff3cd"
            else:
                dictamen, bg_color = "CONDICIÓN ÓPTIMA / ACEPTABLE (Continuar Proceso)", "#d4edda"

            try:
                self.enviar_email(data, dictamen, bg_color)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "feedback": dictamen}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def enviar_email(self, data, dictamen, bg_color):
        msg = MIMEMultipart()
        msg['From'], msg['To'] = data['userEmail'], data['supervisor']
        msg['Subject'] = f"Reporte de Clinchados: {data['parte']} - {data['auto']}"

        nok_html = "".join([f'''
            <div style="background-color: #f8d7da; padding: 15px; margin-bottom: 15px; border: 1px solid #f5c6cb;">
                <strong>NOK #{i+1} - P/N: {nok['parteNum']}</strong><br>
                <h4 style="margin-bottom: 5px; color:#555;">Características Externas</h4>
                <ul style="margin-top: 5px;">
                    <li>Punto de unión: {nok['union']}</li>
                    <li>Posición: {nok['posicion']}</li>
                    <li>Cuello agrietado: {nok['cuello']}</li>
                    <li>Ruptura de materiales: {nok['ruptura']}</li>
                    <li>Espesor de fondo (tb): {nok['espesorFondo']}</li>
                    <li>Diámetro externo (d): {nok['diametro']}</li>
                </ul>
                <h4 style="margin-bottom: 5px; color:#555;">Características Internas</h4>
                <ul style="margin-top: 5px;">
                    <li>Muesca (Rígida): {nok['muescaR']}</li>
                    <li>Muesca (Segmentos Móviles): {nok['muescaM']}</li>
                    <li>Espesor de Cuello (tn1, tn2): {nok['espesorCuello']}</li>
                    <li>Altura de socavado (fy1, fy2): {nok['socavado']}</li>
                    <li>Residual Lado Punzón (tST min): {nok['residualP']}</li>
                    <li>Residual Lado Matriz (tM min): {nok['residualM']}</li>
                    <li>Grietas en Cuello (Int): {nok['grietaInt']}</li>
                    <li>Grietas Troquel (XR): {nok['grietaTroquel']}</li>
                    <li>Grietas Matriz: {nok['grietaMatriz']}</li>
                </ul>
                <h4 style="margin-bottom: 5px; color:#555;">Características de Fuerza</h4>
                <ul style="margin-top: 5px;">
                    <li>Resistencia a la cizalladura: {nok['cizalladura']}</li>
                    <li>Fuerza de tracción: {nok['traccion']}</li>
                </ul>
            </div>''' for i, nok in enumerate(data['nokDetails'])])

        html = f'''<html><body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #0056b3;">Inspección de Matriz de Clinchado</h2>
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
                <tr><td bgcolor="#f4f4f4"><strong>Inspector:</strong></td><td>{data['inspector']}</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>Fecha:</strong></td><td>{data['fecha']}</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>Automóvil:</strong></td><td>{data['auto']}</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>Parte:</strong></td><td>{data['parte']}</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>ID Matriz:</strong></td><td>{data['idMatriz']}</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>Espesor (t):</strong></td><td>{data['espesor']} mm</td></tr>
                <tr><td bgcolor="#f4f4f4"><strong>Regresos:</strong></td><td>{data['vecesRegresado']}</td></tr>
            </table>
            <h3>Resumen de Clinchados</h3>
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
                <tr bgcolor="#0056b3" style="color: white;">
                    <th>Total Evaluados</th><th>OK</th><th>COK</th><th>NOK</th><th>Cortes Totales</th><th>Efectividad</th>
                </tr>
                <tr style="text-align: center;">
                    <td>{data['totalClinchados']}</td>
                    <td style="color: green; font-weight: bold;">{data['okCount']}</td>
                    <td>{data['cokCount']}</td>
                    <td style="color: red; font-weight: bold;">{data['nokCount']}</td>
                    <td>{data['totalCortes']}</td>
                    <td><strong>{data['porcentaje']}</strong></td>
                </tr>
            </table>
            {nok_html}
            <br>
            <div style="border: 3px solid black; padding: 20px; text-align: center; background-color: {bg_color};">
                <span style="color: black; font-weight: bold; font-size: 1.5em; text-transform: uppercase;">
                    {dictamen}
                </span>
            </div>
        </body></html>'''
        msg.attach(MIMEText(html, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(data['userEmail'], data['userPass'])
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    # La nube asignará un puerto dinámico automáticamente
    PORT = int(os.environ.get("PORT", 8000))
    print(f"Servidor iniciado en el puerto {PORT}")
    with socketserver.TCPServer(("", PORT), ClinchadoHandler) as httpd:
        httpd.serve_forever()
