import http.server
import socketserver
import json
import urllib.request
import urllib.error
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
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #A8A8A8; margin: 0; padding: 15px; color: #1F2F57; overflow-x: hidden; }}
        .container {{ width: 100%; max-width: 950px; margin: auto; background: #FDFAF9; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border-top: 8px solid #1F2F57; }}
        h1, h2, h3 {{ color: #1F2F57; text-align: center; }}
        .section {{ margin-bottom: 25px; padding: 15px; border: 1px solid #A8A8A8; border-radius: 8px; background-color: #FDFAF9; width: 100%; }}
        .visual-panel {{ background-color: #FDFAF9; border: 2px solid #6091C3; }} 
        label {{ display: block; margin-top: 10px; font-weight: bold; font-size: 0.85em; color: #1F2F57; }}
        input[type="text"], input[type="number"], input[type="email"], input[type="password"], input[type="date"], select {{ 
            width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #A8A8A8; border-radius: 5px; font-size: 0.85em; background-color: #FDFAF9; color: #1F2F57;
        }}
        .instructions {{ background-color: #FDFAF9; border-left: 4px solid #1F2F57; border-top: 1px solid #A8A8A8; border-right: 1px solid #A8A8A8; border-bottom: 1px solid #A8A8A8; padding: 10px; font-size: 0.9em; margin-bottom: 15px; color: #1F2F57; }}
        .flex-row {{ display: flex; gap: 15px; flex-wrap: wrap; align-items: flex-start; width: 100%; }}
        .flex-col {{ flex: 1 1 250px; min-width: 0; }}
        .calc-box {{ background: #A8A8A8; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; margin-top: 15px; border: 1px solid #1F2F57; color: #1F2F57; }}
        .btn {{ background-color: #6091C3; color: #FDFAF9; border: none; padding: 12px 20px; font-size: 1em; cursor: pointer; border-radius: 5px; width: 100%; margin-top: 20px; font-weight: bold; transition: 0.3s; }}
        .btn:hover {{ background-color: #1F2F57; color: #FDFAF9; }}
        .nok-panel {{ border: 1px solid #6091C3; background-color: #FDFAF9; padding: 15px; border-radius: 5px; margin-top: 10px; width: 100%; }}
        .advice {{ color: #1F2F57; font-weight: bold; text-align: center; font-size: 1.2em; padding: 20px; border: 3px solid #1F2F57; margin-top: 20px; background: #A8A8A8; display: none; text-transform: uppercase; }}
        .ref-img {{ max-width: 100%; height: auto; display: block; margin-top: 8px; margin-bottom: 8px; border: 1px solid #A8A8A8; border-radius: 4px; background: #FDFAF9; padding: 4px; box-shadow: 1px 1px 4px rgba(0,0,0,0.2); }}
        
        .checkbox-group {{ display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }}
        .checkbox-item {{ display: flex; align-items: center; gap: 8px; }}
        .checkbox-item input[type="checkbox"] {{ width: auto; margin: 0; transform: scale(1.2); accent-color: #1F2F57; }}
        .checkbox-item label {{ margin: 0; font-weight: normal; font-size: 0.9em; }}

        @media (max-width: 600px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 15px; }}
            .section {{ padding: 10px; }}
            .flex-col {{ flex: 1 1 100%; }}
            h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>

<div class="container">
    <h1>Inspección de Matriz de Clinchado</h1>
    
    <form id="clinchadoForm">
        <!-- SECCIÓN 1: Modificada para Selección Múltiple -->
        <div class="section">
            <h2>1. Destinatarios del Reporte</h2>
            <div class="instructions">
                Selecciona las áreas a las que deseas enviar este informe. Puedes elegir varias opciones o ingresar un correo específico si lo prefieres.
            </div>
            <div class="flex-row">
                <div class="flex-col">
                    <label>Áreas predefinidas:</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="area_lab" value="laboratorio@vw.com" class="dest-checkbox">
                            <label for="area_lab">Laboratorio</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="area_sol" value="soldadura@vw.com" class="dest-checkbox">
                            <label for="area_sol">Soldadura</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="area_oja" value="ojalateria@vw.com" class="dest-checkbox">
                            <label for="area_oja">Ojalatería</label>
                        </div>
                    </div>
                </div>
                <div class="flex-col">
                    <label>Correo adicional / único (Opcional):</label>
                    <input type="email" id="customEmail" placeholder="ejemplo@vw.com">
                </div>
            </div>
        </div>

        <!-- SECCIÓN 2 -->
        <div class="section">
            <h2>2. Información del Ensamble</h2>
            <div class="flex-row">
                <div class="flex-col"><label>Inspector / Operador:</label><input type="text" id="inspector" required placeholder="Ej. Juan Pérez"></div>
                <div class="flex-col"><label>Fecha de Envío:</label><input type="date" id="fecha" required></div>
            </div>
            <div class="flex-row">
                <div class="flex-col">
                    <label>Automóvil Evaluado:</label>
                    <select id="auto" required>
                        <option value="" disabled selected>Selecciona un vehículo</option>
                        <option value="Jetta">Jetta</option>
                        <option value="Taos">Taos</option>
                        <option value="Tiguan">Tiguan</option>
                        <option value="Golf">Golf</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>Parte de la Carrocería:</label>
                    <select id="parte" required>
                        <option value="" disabled selected>Primero selecciona un vehículo</option>
                    </select>
                </div>
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

    const partesPorVehiculo = {{
        "Jetta": ["Tapa trasera", "Tapa delantera"],
        "Taos": ["Tapa trasera", "Tapa delantera"],
        "Tiguan": ["Tapa trasera", "Tapa delantera", "Salpicadera izquierda", "Salpicadera derecha"],
        "Golf": ["Tapa trasera", "Tapa delantera"]
    }};

    const subpartesTiguanTapaTrasera = {{
        "Refuerzo de bisagra derecha": ["P0002-B-1330-300", "P0002-B-1330-400", "P0002-B-1330-600", "P0002-B-1330-700", "P0002-B-1330-100"],
        "Refuerzo de bisagra izquierda": ["P0001-A-1330-300", "P0001-A-1330-400", "P0001-A-1330-600", "P0001-A-1330-700", "P0001-A-1330-100", "P0001-A-1330-500", "P0001-A-1330-200"],
        "Chapa de cierre": ["P0005-E-1330-1300", "P0005-E-1330-1200", "P0005-E-1330-200", "P0005-E-1330-100", "P0005-E-1330-900", "P0005-E-1330-700", "P0005-E-1330-1000", "P0005-E-1330-1100", "P0005-E-1330-800", "P0005-E-1330-300", "P0005-E-1330-400", "P0005-E-1330-1400", "P0005-E-1330-500"],
        "Refuerzo lateral derecho": ["P0004-D-1330-100", "P0004-D-1330-800", "P0004-D-1330-300", "P0004-D-1330-200", "P0004-D-1330-1100", "P0004-D-1330-400", "P0004-D-1330-1000", "P0004-D-1330-600", "P0004-D-1330-900", "P0004-D-1330-700"],
        "Refuerzo lateral izquierdo": ["P0003-C-1330-100", "P0003-C-1330-800", "P0003-C-1330-300", "P0003-C-1330-200", "P0003-C-1330-1000", "P0003-C-1330-1100", "P0003-C-1330-400", "P0003-C-1330-600", "P0003-C-1330-900", "P0003-C-1330-700"],
        "Calavera izquierda": ["P001-A-1330-400", "P001-A-1330-200", "P001-A-1330-300", "P001-A-1330-800", "P001-A-1330-100", "P001-A-1330-700", "P001-A-1330-900", "P001-A-1330-600", "P001-A-1330-500"],
        "Calavera derecha": ["P002-B-1330-400", "P002-B-1330-200", "P002-B-1330-300", "P002-B-1330-900", "P002-B-1330-100", "P002-B-1330-700", "P002-B-1330-800", "P002-B-1330-600", "P002-B-1330-500"]
    }};

    document.getElementById('auto').addEventListener('change', function() {{
        const parteSelect = document.getElementById('parte');
        parteSelect.innerHTML = '<option value="" disabled selected>Selecciona la parte de carrocería</option>';
        
        const auto = this.value;
        if(partesPorVehiculo[auto]) {{
            partesPorVehiculo[auto].forEach(parte => {{
                const opt = document.createElement('option');
                opt.value = parte;
                opt.innerText = parte;
                parteSelect.appendChild(opt);
            }});
        }}
        calcularOK();
    }});

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
        
        generarPanelesErrores(nok, cok);
        
        document.getElementById('feedbackContainer').style.display = 'none';
    }}

    document.getElementById('vecesRegresado').addEventListener('input', calcularOK);
    document.getElementById('cokCount').addEventListener('input', calcularOK);
    document.getElementById('parte').addEventListener('change', calcularOK);

    function generarPanelesErrores(cantidadNOK, cantidadCOK) {{
        const sec4 = document.getElementById('sec4Container');
        const container = document.getElementById('nokContainer');
        container.innerHTML = '';
        
        const totalPaneles = cantidadNOK + cantidadCOK;
        
        if(totalPaneles > 0) {{
            sec4.style.display = 'block';
            
            const autoSeleccionado = document.getElementById('auto').value || "";
            const parteSeleccionada = document.getElementById('parte').value || "";
            
            let optionsSubpartes = '<option value="" disabled selected>Selecciona la sección</option>';
            if (autoSeleccionado === "Tiguan" && parteSeleccionada === "Tapa trasera") {{
                Object.keys(subpartesTiguanTapaTrasera).forEach(sub => {{
                    optionsSubpartes += `<option value="${{sub}}">${{sub}}</option>`;
                }});
            }} else {{
                optionsSubpartes += '<option value="General">Panel General</option>';
            }}

            const generarHTMLPanel = (titulo, idLabel, bgColor, borderColor, tipoEstado) => {{
                const panel = document.createElement('div');
                panel.className = 'nok-panel flex-row';
                panel.style.backgroundColor = bgColor; 
                panel.style.borderColor = borderColor;
                panel.innerHTML = `
                    <div class="flex-col" style="flex: 1.5;">
                        <label style="color:#1F2F57;">${{titulo}}</label>
                        <select class="nok-subparte" required>${{optionsSubpartes}}</select>
                    </div>
                    <div class="flex-col" style="flex: 1.5;">
                        <label style="color:#1F2F57;">ID del Clinchado:</label>
                        <select class="nok-parte" required>
                            <option value="" disabled selected>Primero selecciona sección</option>
                        </select>
                    </div>
                    <div class="flex-col" style="flex: 1;">
                        <label style="color:#1F2F57;">Estado:</label>
                        <input type="text" class="nok-estado" value="${{tipoEstado}}" readonly style="background-color: transparent; border: none; font-weight: bold; color: #1F2F57; padding-left: 0;">
                    </div>
                `;
                
                const selectSub = panel.querySelector('.nok-subparte');
                const selectId = panel.querySelector('.nok-parte');
                
                selectSub.addEventListener('change', function() {{
                    selectId.innerHTML = '<option value="" disabled selected>Selecciona el ID</option>';
                    const val = this.value;
                    
                    if (subpartesTiguanTapaTrasera[val]) {{
                        subpartesTiguanTapaTrasera[val].forEach(id => {{
                            selectId.innerHTML += `<option value="${{id}}">${{id}}</option>`;
                        }});
                    }} else {{
                        selectId.innerHTML += `
                            <option value="EJEMPLO-${{autoSeleccionado.toUpperCase()}}-001">EJEMPLO-001</option>
                            <option value="EJEMPLO-${{autoSeleccionado.toUpperCase()}}-002">EJEMPLO-002</option>
                            <option value="Otro">Otro (Especificar en notas)</option>
                        `;
                    }}
                }});
                
                container.appendChild(panel);
            }};

            for(let i = 1; i <= cantidadNOK; i++) {{
                generarHTMLPanel(`Pieza Evaluada #${{i}} (Mal - NOK):`, 'ID del Clinchado:', '#A8A8A8', '#1F2F57', 'Mal (NOK)');
            }}

            for(let i = 1; i <= cantidadCOK; i++) {{
                generarHTMLPanel(`Pieza Evaluada #${{cantidadNOK + i}} (Condicionado - COK):`, 'ID del Clinchado:', '#FDFAF9', '#6091C3', 'Condicionado (COK)');
            }}

        }} else {{
            sec4.style.display = 'none';
        }}
    }}

    document.getElementById('clinchadoForm').addEventListener('submit', async function(e) {{
        e.preventDefault();
        
        // 1. Recolección de Correos Destino
        const checkboxes = document.querySelectorAll('.dest-checkbox:checked');
        let supervisores = [];
        checkboxes.forEach(cb => supervisores.push(cb.value));
        
        const customEmail = document.getElementById('customEmail').value.trim();
        if (customEmail) {{
            supervisores.push(customEmail);
        }}
        
        if (supervisores.length === 0) {{
            alert("⚠️ Por favor, selecciona al menos un área de envío o ingresa un correo en el campo adicional.");
            return;
        }}

        const btn = document.getElementById('btnSubmit');
        btn.innerText = 'EVALUANDO...';
        btn.disabled = true;

        const data = {{
            supervisores: supervisores, // Ahora es un arreglo de correos
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
            const subparte = panel.querySelector('.nok-subparte').value;
            const idParte = panel.querySelector('.nok-parte').value;
            data.piezasMalas.push({{
                nombre: `${{subparte}} (${{idParte}})`,
                estado: panel.querySelector('.nok-estado').value
            }});
        }});

        try {{
            const response = await fetch('/enviar_correo', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(data) }});
            const result = await response.json();
            if(response.ok) {{
                const fbDiv = document.getElementById('feedbackContainer');
                fbDiv.style.display = 'block';
                fbDiv.style.backgroundColor = result.bg_color;
                fbDiv.innerHTML = result.feedback;
                fbDiv.scrollIntoView({{ behavior: 'smooth' }});
                alert('✅ Reporte enviado exitosamente a: ' + supervisores.join(', '));
                document.getElementById('clinchadoForm').reset();
                document.getElementById('fecha').valueAsDate = new Date();
                calcularOK();
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
                bg_color = "#A8A8A8" 
            elif nok_count > 0:
                dictamen = "DESGASTE INICIAL / PRECAUCIÓN (Aumentar frecuencia de inspección)"
                bg_color = "#A8A8A8" 
            else:
                dictamen = "CONDICIÓN ÓPTIMA / ACEPTABLE (Continuar Proceso)"
                bg_color = "#A8A8A8" 

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
        
        API_KEY = os.environ.get("BREVO_API_KEY")
        SENDER_EMAIL = "codeenvi399@gmail.com"
        
        # Mapeo de destinatarios múltiples para la API
        lista_supervisores = data.get('supervisores', [])
        if not lista_supervisores:
            raise Exception("No se especificaron destinatarios.")
            
        to_payload = [{"email": email} for email in lista_supervisores]
        nombres_destinos = ", ".join(lista_supervisores)
        
        piezas_html = ""
        if len(data['piezasMalas']) > 0:
            piezas_html = "<ul>"
            for p in data['piezasMalas']:
                piezas_html += f"<li><strong>{p['nombre']}</strong> - Estado: <span style='color:#1F2F57; font-weight:bold;'>{p['estado']}</span></li>"
            piezas_html += "</ul>"
        else:
            piezas_html = "<p style='color:#1F2F57; font-weight:bold;'>No se reportaron piezas erróneas o condicionadas.</p>"

        html = f'''<html><body style="font-family: Arial, sans-serif; color: #1F2F57; background-color: #FDFAF9; padding: 20px;">
            <h2 style="color: #6091C3;">Inspección de Matriz de Clinchado</h2>
            
            <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #A8A8A8;">
                <tr><td bgcolor="#FDFAF9"><strong>Enviado a:</strong></td><td>{nombres_destinos}</td></tr>
                <tr><td bgcolor="#FDFAF9"><strong>Inspector (Operador):</strong></td><td>{data['inspector']}</td></tr>
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

        payload = {
            "sender": {"email": SENDER_EMAIL, "name": "Sistema de Inspección VW"},
            "to": to_payload,
            "subject": f"Reporte de Calidad: {data['parte']} - {data['auto']} (Insp: {data['inspector']})",
            "htmlContent": html
        }

        req = urllib.request.Request('https://api.brevo.com/v3/smtp/email')
        
        if not API_KEY:
            raise Exception("No se encontró la variable BREVO_API_KEY en Render. Revisa la pestaña 'Environment'.")
            
        req.add_header('api-key', API_KEY)
        req.add_header('accept', 'application/json')
        req.add_header('content-type', 'application/json')

        try:
            urllib.request.urlopen(req, json.dumps(payload).encode('utf-8'))
        except urllib.error.URLError as e:
            error_info = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            raise Exception(f"Fallo en API Brevo: {error_info}")

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))
    print(f"Servidor iniciado en el puerto {PORT}")
    
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), ClinchadoHandler) as httpd:
        httpd.serve_forever()