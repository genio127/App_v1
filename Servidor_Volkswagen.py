import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import base64
from io import BytesIO
from xhtml2pdf import pisa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image_b64(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded_string}"
    print(f"[!] ADVERTENCIA: No se encontró la imagen '{filename}'.")
    return ""

img_web_base64 = load_image_b64("logo_web.png")
img_pdf_base64 = load_image_b64("logo_pdf.png")
img_email_base64 = load_image_b64("logo_email.png")

# ==============================================================================
# CATÁLOGO COMPLETO DE VEHÍCULOS, PARTES Y PUNTOS DE CLINCHADO
# ==============================================================================
MATRICES_POR_VEHICULO = {
    "Tiguan": {
        "Tapa Trasera": {
            "Refuerzo de bisagra izquierda": [
                "P0001-A-1330-100", "P0001-A-1330-200", "P0001-A-1330-300",
                "P0001-A-1330-400", "P0001-A-1330-500", "P0001-A-1330-600",
                "P0001-A-1330-700"
            ],
            "Refuerzo de bisagra derecha": [
                "P0002-B-1330-100", "P0002-B-1330-200", "P0002-B-1330-300",
                "P0002-B-1330-400", "P0002-B-1330-500", "P0002-B-1330-600",
                "P0002-B-1330-700"
            ],
            "Refuerzo lateral izquierdo": [
                "P0003-C-1330-100", "P0003-C-1330-200", "P0003-C-1330-300",
                "P0003-C-1330-400", "P0003-C-1330-600", "P0003-C-1330-700",
                "P0003-C-1330-800", "P0003-C-1330-900", "P0003-C-1330-1000",
                "P0003-C-1330-1100"
            ],
            "Refuerzo lateral derecho": [
                "P0004-D-1330-100", "P0004-D-1330-200", "P0004-D-1330-300",
                "P0004-D-1330-400", "P0004-D-1330-600", "P0004-D-1330-700",
                "P0004-D-1330-800", "P0004-D-1330-900", "P0004-D-1330-1000",
                "P0004-D-1330-1100"
            ],
            "Chapa de cierre": [
                "P0005-E-1330-100", "P0005-E-1330-200", "P0005-E-1330-300",
                "P0005-E-1330-400", "P0005-E-1330-500", "P0005-E-1330-700",
                "P0005-E-1330-800", "P0005-E-1330-900", "P0005-E-1330-1000",
                "P0005-E-1330-1100", "P0005-E-1330-1200", "P0005-E-1330-1300",
                "P0005-E-1330-1400"
            ],
            "Calavera izquierda": [
                "P001-A-1330-100", "P001-A-1330-200", "P001-A-1330-300",
                "P001-A-1330-400", "P001-A-1330-500", "P001-A-1330-600",
                "P001-A-1330-700", "P001-A-1330-800", "P001-A-1330-900"
            ],
            "Calavera derecha": [
                "P002-B-1330-100", "P002-B-1330-200", "P002-B-1330-300",
                "P002-B-1330-400", "P002-B-1330-500", "P002-B-1330-600",
                "P002-B-1330-700", "P002-B-1330-800", "P002-B-1330-900"
            ]
        },
        "Tapa Delantera": {
            "Sección P0001A": [
                "P0001A_1330_000100", "P0001A_1330_000200", "P0001A_1330_000400",
                "P0001A_1330_000500", "P0001A_1330_000600"
            ],
            "Sección P0002B": [
                "P0002B_1330_000100", "P0002B_1330_000200", "P0002B_1330_000400",
                "P0002B_1330_000500", "P0002B_1330_000600"
            ],
            "Sección P0003C": [
                "P0003C_1330_000100", "P0003C_1330_000200", "P0003C_1330_000300"
            ],
            "Sección P0004D": [
                "P0004D_1330_000400", "P0004D_1330_000500", "P0004D_1330_000600"
            ],
            "Sección P0005E": [
                "P0005E_1330_000700", "P0005E_1330_000800", "P0005E_1330_000900",
                "P0005E_1330_001000", "P0005E_1330_001100"
            ]
        },
        "Salpicadera Derecha": {
            "Sección P0001_A": [
                "P0001_A_1330_000200", "P0001_A_1330_000300", "P0001_A_1330_000400",
                "P0001_A_1330_001100", "P0001_A_1330_001100"
            ],
            "Sección P0002_B": [
                "P0002_B_1330_000100", "P0002_B_1330_000200", "P0002_B_1330_000300",
                "P0002_B_1330_000400"
            ]
        },
        "Salpicadera Izquierda": {
            "Sección P0001_A": [
                "P0001_A_1330_000100", "P0001_A_1330_000200", "P0001_A_1330_000300",
                "P0001_A_1330_000400", "P0001_A_1330_001100"
            ],
            "Sección P0002_B": [
                "P0002_B_1330_000100", "P0002_B_1330_000200", "P0002_B_1330_000300",
                "P0002_B_1330_000400"
            ]
        }
    },
    "Golf": {
        "Tapa Trasera": {
            "Sección P0001-A (L)": [
                "P0001-A-1330-001500 L", "P0001-A-1330-001600 L", "P0001-A-1330-001700 L",
                "P0001-A-1330-001800 L", "P0001-A-1330-001900 L", "P0001-A-1330-002000 L",
                "P0001-A-1330-002100 L"
            ],
            "Sección P0001-A (R)": [
                "P0001-A-1330-001500 R", "P0001-A-1330-001600 R", "P0001-A-1330-001700 R",
                "P0001-A-1330-001800 R", "P0001-A-1330-001900 R", "P0001-A-1330-002000 R",
                "P0001-A-1330-002100 R"
            ],
            "Sección P0002-D (L)": [
                "P0002-D-1330-00300 L", "P0002-D-1330-00400 L", "P0002-D-1330-00500 L",
                "P0002-D-1330-00600 L", "P0002-D-1330-00700 L", "P0002-D-1330-00800 L",
                "P0002-D-1330-00900 L", "P0002-D-1330-01000 L"
            ],
            "Sección P0002-D (R)": [
                "P0002-D-1330-00300 R", "P0002-D-1330-00400 R", "P0002-D-1330-00500 R",
                "P0002-D-1330-00600 R", "P0002-D-1330-00700 R", "P0002-D-1330-00800 R",
                "P0002-D-1330-01000 R"
            ],
            "Sección P0003-C": [
                "P0003-C-1330-001100", "P0003-C-1330-001200", "P0003-C-1330-001300",
                "P0003-C-1330-001500 L", "P0003-C-1330-001600 R"
            ]
        },
        "Tapa Delantera": {
            "Sección P001-A": [
                "P001-A-1330-0100", "P001-A-1330-0200", "P001-A-1330-1300",
                "P001-A-1330-1400"
            ],
            "Sección P002-B": [
                "P002-B-1330-0300", "P002-B-1330-0400", "P002-B-1330-1500",
                "P002-B-1330-1600"
            ],
            "Sección P003-C": [
                "P003-C-1330-0500", "P003-C-1330-0600", "P003-C-1330-1700"
            ],
            "Sección P004-D": [
                "P004-D-1330-0700", "P004-D-1330-0800", "P004-D-1330-1800"
            ]
        },
        "Salpicadera Derecha": {
            "Sección P0001-A": [
                "P0001-A-1330-00400", "P0001-A-1330-00500", "P0001-A-1330-00600"
            ]
        },
        "Salpicadera Izquierda": {
            "Sección P0001-A": [
                "P0001-A-1330-00400", "P0001-A-1330-00500", "P0001-A-1330-00600"
            ]
        }
    },
    "Taos": {
        "Tapa Trasera": {
            "Sección P001-A": [
                "P001-A-1330-1110", "P001-A-1330-1610", "P001-A-1330-2110",
                "P001-A-1330-2210", "P001-A-1330-2610", "P001-A-1330-2810"
            ],
            "Sección P001-I": [
                "P001-I-1330-1110", "P001-I-1330-1610", "P001-I-1330-2110",
                "P001-I-1330-2210", "P001-I-1330-2610", "P001-I-1330-2810"
            ],
            "Sección P002-C": [
                "P002-C-1330-110", "P002-C-1330-210", "P002-C-1330-310",
                "P002-C-1330-610", "P002-C-1330-710", "P002-C-1330-810",
                "P002-C-1330-910", "P002-C-1330-1010", "P002-C-1330-1110"
            ],
            "Sección P002-N": [
                "P002-N-1330-110", "P002-N-1330-210", "P002-N-1330-310",
                "P002-N-1330-610", "P002-N-1330-710", "P002-N-1330-810",
                "P002-N-1330-910", "P002-N-1330-1010", "P002-N-1330-1110"
            ],
            "Sección P003-E": [
                "P003-E-1330-110", "P003-E-1330-210", "P003-E-1330-310",
                "P003-E-1330-410", "P003-E-1330-510"
            ],
            "Sección P004-F": [
                "P004-F-1330-110", "P004-F-1330-210", "P004-F-1330-310",
                "P004-F-1330-410", "P004-F-1330-510"
            ]
        }
    },
    "Jetta": {
        "Tapa Trasera": {
            "Sección P0001-A (Bloque 1)": [
                "P0001-A-1330-000100", "P0001-A-1330-000200", "P0001-A-1330-000300",
                "P0001-A-1330-000400", "P0001-A-1330-000500", "P0001-A-1330-000600"
            ],
            "Sección P0002-B (Bloque 1)": [
                "P0002-B-1330-000100", "P0002-B-1330-000200", "P0002-B-1330-000300",
                "P0002-B-1330-000400", "P0002-B-1330-000500"
            ],
            "Sección P0003-C": [
                "P0003-C-1330-000100", "P0003-C-1330-000200", "P0003-C-1330-000300",
                "P0003-C-1330-000400", "P0003-C-1330-000500"
            ],
            "Sección P0004-D": [
                "P0004-D-1330-000100", "P0004-D-1330-000200", "P0004-D-1330-000300",
                "P0004-D-1330-000400"
            ],
            "Sección P0005-E": [
                "P0005-E-1330-000100", "P0005-E-1330-000200", "P0005-E-1330-000300",
                "P0005-E-1330-000400"
            ],
            "Sección P0006-F": [
                "P0006-F-1330-000100", "P0006-F-1330-000200", "P0006-F-1330-000300",
                "P0006-F-1330-000400"
            ],
            "Sección P0007-G": [
                "P0007-G-1330-000100", "P0007-G-1330-000200", "P0007-G-1330-000300",
                "P0007-G-1330-000400"
            ],
            "Sección P0008-H": [
                "P0008-H-1330-000100", "P0008-H-1330-000200"
            ],
            "Sección P0009-I": [
                "P0009-I-1330-000100", "P0009-I-1330-000200"
            ],
            "Sección P0001-A (Serie 000100-002500)": [
                "P0001-A-1330-000100", "P0001-A-1330-000200", "P0001-A-1330-000300",
                "P0001-A-1330-000400", "P0001-A-1330-000500", "P0001-A-1330-000600",
                "P0001-A-1330-000700", "P0001-A-1330-000800", "P0001-A-1330-000900",
                "P0001-A-1330-001000", "P0001-A-1330-001100", "P0001-A-1330-001200",
                "P0001-A-1330-001300", "P0001-A-1330-001400", "P0001-A-1330-001500",
                "P0001-A-1330-001600", "P0001-A-1330-001700", "P0001-A-1330-001800",
                "P0001-A-1330-001900", "P0001-A-1330-002000", "P0001-A-1330-002100",
                "P0001-A-1330-002200", "P0001-A-1330-002300", "P0001-A-1330-002400",
                "P0001-A-1330-002500"
            ],
            "Sección P0002-B (Serie 000100-001600)": [
                "P0002-B-1330-000100", "P0002-B-1330-000200", "P0002-B-1330-000300",
                "P0002-B-1330-000400", "P0002-B-1330-000500", "P0002-B-1330-000600",
                "P0002-B-1330-000700", "P0002-B-1330-000800", "P0002-B-1330-000900",
                "P0002-B-1330-001000", "P0002-B-1330-001100", "P0002-B-1330-001200",
                "P0002-B-1330-001300", "P0002-B-1330-001400", "P0002-B-1330-001500",
                "P0002-B-1330-001600"
            ],
            "Sección P-P001-A": [
                "P-P001-A-1330-001100", "P-P001-A-1330-001200", "P-P001-A-1330-001300",
                "P-P001-A-1330-001400", "P-P001-A-1330-001500", "P-P001-A-1330-001600",
                "P-P001-A-1330-001700", "P-P001-A-1330-001800", "P-P001-A-1330-001900",
                "P-P001-A-1330-002000"
            ],
            "Sección P-P002-B": [
                "P-P002-B-1330-001100", "P-P002-B-1330-001200", "P-P002-B-1330-001300"
            ]
        },
        "Tapa Delantera": {
            "Sección P001-A": [
                "P001-A-1330-0100", "P001-A-1330-0200", "P001-A-1330-0300",
                "P001-A-1330-0400", "P001-A-1330-0500"
            ],
            "Sección P002-B": [
                "P002-B-1330-0100", "P002-B-1330-0200", "P002-B-1330-0300",
                "P002-B-1330-0400", "P002-B-1330-0500"
            ],
            "Sección P003-C": [
                "P003-C-1330-0100", "P003-C-1330-0200", "P003-C-1330-0300",
                "P003-C-1330-0400", "P003-C-1330-0500", "P003-C-1330-0600",
                "P003-C-1330-0700", "P003-C-1330-0800"
            ],
            "Sección P004-D": [
                "P004-D-1330-0100", "P004-D-1330-0200", "P004-D-1330-0300"
            ],
            "Sección P005-E": [
                "P005-E-1330-0100", "P005-E-1330-0200", "P005-E-1330-0300"
            ],
            "Sección P006-F": [
                "P006-F-1330-0100", "P006-F-1330-0200"
            ]
        }
    }
}

MATRICES_JSON = json.dumps(MATRICES_POR_VEHICULO, ensure_ascii=False)

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
        .header-logo {{ text-align: center; margin-bottom: 20px; }}
        .header-logo img {{ max-width: 250px; height: auto; }}
        h1, h2, h3 {{ color: #1F2F57; text-align: center; }}
        .section {{ margin-bottom: 25px; padding: 15px; border: 1px solid #A8A8A8; border-radius: 8px; background-color: #FDFAF9; width: 100%; }}
        label {{ display: block; margin-top: 10px; font-weight: bold; font-size: 0.85em; color: #1F2F57; }}
        input[type="text"], input[type="number"], input[type="email"], input[type="date"], select {{ 
            width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #A8A8A8; border-radius: 5px; font-size: 0.85em; background-color: #FDFAF9; color: #1F2F57;
        }}
        .instructions {{ background-color: #FDFAF9; border-left: 4px solid #1F2F57; border-top: 1px solid #A8A8A8; border-right: 1px solid #A8A8A8; border-bottom: 1px solid #A8A8A8; padding: 10px; font-size: 0.9em; margin-bottom: 15px; color: #1F2F57; }}
        .flex-row {{ display: flex; gap: 15px; flex-wrap: wrap; align-items: flex-start; width: 100%; }}
        .flex-col {{ flex: 1 1 250px; min-width: 0; }}
        .btn {{ background-color: #6091C3; color: #FDFAF9; border: none; padding: 12px 20px; font-size: 1em; cursor: pointer; border-radius: 5px; width: 100%; margin-top: 20px; font-weight: bold; transition: 0.3s; }}
        .btn:hover {{ background-color: #1F2F57; color: #FDFAF9; }}
        .advice {{ color: #1F2F57; font-weight: bold; text-align: center; font-size: 1.2em; padding: 20px; border: 3px solid #1F2F57; margin-top: 20px; background: #A8A8A8; display: none; text-transform: uppercase; }}
        
        .checkbox-group {{ display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }}
        .checkbox-item {{ display: flex; align-items: center; gap: 8px; }}
        .checkbox-item input[type="checkbox"] {{ width: auto; margin: 0; transform: scale(1.2); accent-color: #1F2F57; }}
        .checkbox-item label {{ margin: 0; font-weight: normal; font-size: 0.9em; }}

        .matriz-wrapper {{ margin-top: 18px; display: none; }}
        .status-bar {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; background-color: #E0E0E0; padding: 10px 14px; border-radius: 6px; border: 1px solid #1F2F57; margin-bottom: 12px; font-size: 0.85em; font-weight: bold; color: #1F2F57; }}
        .grid-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .grid-table th, .grid-table td {{ border: 1px solid #A8A8A8; padding: 10px; }}
        .grid-table th {{ background-color: #1F2F57; color: #FDFAF9; text-align: center; font-size: 0.9em; }}
        .part-name {{ font-weight: bold; background-color: #E0E0E0; width: 25%; color: #1F2F57; font-size: 0.85em; }}
        .id-container {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
        
        .id-btn {{ 
            border-radius: 20px; padding: 6px 12px; cursor: pointer;
            font-size: 0.75em; font-weight: bold;
            transition: all 0.2s ease-in-out;
            user-select: none;
        }}
        .id-btn.selected {{ 
            background-color: #1F2F57; color: #FDFAF9; border: 2px solid #1F2F57;
        }}
        .id-btn.selected:hover {{ 
            background-color: #6091C3; border-color: #6091C3;
        }}
        .id-btn.deselected {{ 
            background-color: #FDFAF9; color: #7A7A7A; border: 2px dashed #A8A8A8;
            text-decoration: line-through;
        }}
        .id-btn.deselected:hover {{ 
            border-color: #1F2F57; color: #1F2F57;
        }}

        @media (max-width: 600px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 15px; }}
            .section {{ padding: 10px; }}
            .flex-col {{ flex: 1 1 100%; }}
            h1 {{ font-size: 1.5em; }}
            .part-name {{ width: 100%; display: block; border-bottom: none; }}
            .grid-table td {{ display: block; width: 100%; }}
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header-logo">
        {f'<img src="{img_web_base64}">' if img_web_base64 else ''}
    </div>

    <h1>Inspección de Matriz de Clinchado</h1>
    
    <form id="clinchadoForm">
        <!-- SECCIÓN 1: Destinatarios -->
        <div class="section">
            <h2>1. Destinatarios del Reporte</h2>
            <div class="instructions">
                Selecciona las áreas a las que deseas enviar este informe (PDF).
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
                            <input type="checkbox" id="area_oja" value="israel.villarce@vw.com.mx" class="dest-checkbox">
                            <label for="area_oja">Hojalatería</label>
                        </div>
                    </div>
                </div>
                <div class="flex-col">
                    <label>Correo adicional / único (Opcional):</label>
                    <input type="email" id="customEmail" placeholder="ejemplo@vw.com">
                </div>
            </div>
        </div>

        <!-- SECCIÓN 2: Información del Ensamble -->
        <div class="section">
            <h2>2. Información del Ensamble</h2>
            <div class="flex-row">
                <div class="flex-col"><label>Inspector / Operador:</label><input type="text" id="inspector" required placeholder="Ej. Juan Pérez"></div>
                <div class="flex-col"><label>Fecha de Envío:</label><input type="date" id="fecha" required></div>
            </div>
            <div class="flex-row">
                <div class="flex-col"><label>Veces que han regresado el informe:</label><input type="number" id="vecesRegresado" required min="0" value="0"></div>
            </div>
        </div>

        <!-- SECCIÓN 3: Vehículo y Verificación de Clinchados -->
        <div class="section">
            <h2>3. Vehículo y Verificación de Clinchados</h2>
            <div class="flex-row">
                <div class="flex-col">
                    <label>Automóvil Evaluado:</label>
                    <select id="auto" required>
                        <option value="" disabled selected>Selecciona un vehículo</option>
                        <option value="Tiguan">Tiguan</option>
                        <option value="Golf">Golf</option>
                        <option value="Taos">Taos</option>
                        <option value="Jetta">Jetta</option>
                    </select>
                </div>
                <div class="flex-col">
                    <label>Parte de la Carrocería:</label>
                    <select id="parte" required>
                        <option value="" disabled selected>Primero selecciona un vehículo</option>
                    </select>
                </div>
            </div>

            <div id="matrizWrapper" class="matriz-wrapper">
                <div class="instructions">
                    <strong>Instrucciones:</strong> Todos los clinchados inician <strong>seleccionados (OK)</strong>. Toca únicamente los que presenten falla para <strong>deseleccionarlos (NOK)</strong>.
                    <div style="margin-top: 8px;">
                        <span style="display:inline-block; padding: 2px 10px; background: #1F2F57; color: #FDFAF9; border-radius: 12px; font-size: 0.85em;">✓ Seleccionado (OK)</span>
                        <span style="display:inline-block; padding: 2px 10px; margin-left: 8px; background: #FDFAF9; color: #7A7A7A; border: 2px dashed #A8A8A8; border-radius: 12px; font-size: 0.85em; text-decoration: line-through;">✕ Deseleccionado (NOK)</span>
                    </div>
                </div>
                <div class="status-bar" id="resumenMatriz"></div>
                <div id="nokContainer"></div>
            </div>
        </div>

        <!-- SECCIÓN 4: Módulos -->
        <div class="section">
            <h2>4. Módulos</h2>
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

        <button type="submit" class="btn" id="btnSubmit">GENERAR Y ENVIAR REPORTE PDF</button>
        <div id="feedbackContainer" class="advice"></div>
    </form>
</div>

<script>
    document.getElementById('fecha').valueAsDate = new Date();

    const matricesPorVehiculo = {MATRICES_JSON};

    document.getElementById('auto').addEventListener('change', function() {{
        const parteSelect = document.getElementById('parte');
        parteSelect.innerHTML = '';
        const auto = this.value;
        
        if (matricesPorVehiculo[auto]) {{
            Object.keys(matricesPorVehiculo[auto]).forEach(parte => {{
                parteSelect.appendChild(new Option(parte, parte));
            }});
            parteSelect.selectedIndex = 0;
            renderizarMatriz();
        }} else {{
            parteSelect.innerHTML = '<option value="" disabled selected>Primero selecciona un vehículo</option>';
            document.getElementById('matrizWrapper').style.display = 'none';
            document.getElementById('nokContainer').innerHTML = '';
        }}
    }});

    document.getElementById('parte').addEventListener('change', renderizarMatriz);

    function renderizarMatriz() {{
        const auto = document.getElementById('auto').value;
        const parte = document.getElementById('parte').value;
        const wrapper = document.getElementById('matrizWrapper');
        const container = document.getElementById('nokContainer');

        if (!auto || !parte || !matricesPorVehiculo[auto] || !matricesPorVehiculo[auto][parte]) {{
            wrapper.style.display = 'none';
            container.innerHTML = '';
            return;
        }}

        const estructura = matricesPorVehiculo[auto][parte];
        wrapper.style.display = 'block';

        let htmlMatriz = `
            <table class="grid-table">
                <thead>
                    <tr>
                        <th>Sección (Partes)</th>
                        <th>Identificadores de Clinchado (IDs)</th>
                    </tr>
                </thead>
                <tbody>
        `;

        for (const [subparte, ids] of Object.entries(estructura)) {{
            const botones = ids.map(id => `
                <button type="button" class="id-btn selected" data-subparte="${{subparte}}" data-id="${{id}}">✓ ${{id}}</button>
            `).join('');

            htmlMatriz += `
                <tr>
                    <td class="part-name">${{subparte}}</td>
                    <td><div class="id-container">${{botones}}</div></td>
                </tr>
            `;
        }}

        htmlMatriz += `</tbody></table>`;
        container.innerHTML = htmlMatriz;

        container.querySelectorAll('.id-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                const idText = this.getAttribute('data-id');
                if (this.classList.contains('selected')) {{
                    this.classList.remove('selected');
                    this.classList.add('deselected');
                    this.textContent = `✕ ${{idText}}`;
                }} else {{
                    this.classList.remove('deselected');
                    this.classList.add('selected');
                    this.textContent = `✓ ${{idText}}`;
                }}
                actualizarContador();
            }});
        }});

        actualizarContador();
        document.getElementById('feedbackContainer').style.display = 'none';
    }}

    function actualizarContador() {{
        const ok = document.querySelectorAll('.id-btn.selected').length;
        const nok = document.querySelectorAll('.id-btn.deselected').length;
        const total = ok + nok;
        const efectividad = total > 0 ? ((ok / total) * 100).toFixed(1) : '0.0';

        document.getElementById('resumenMatriz').innerHTML = `
            <span>Total evaluados: ${{total}}</span>
            <span>OK (Seleccionados): ${{ok}}</span>
            <span>NOK (Deseleccionados): ${{nok}}</span>
            <span>Efectividad: ${{efectividad}}%</span>
        `;
    }}

    document.getElementById('clinchadoForm').addEventListener('submit', async function(e) {{
        e.preventDefault();
        
        const checkboxes = document.querySelectorAll('.dest-checkbox:checked');
        let supervisores = [];
        checkboxes.forEach(cb => supervisores.push(cb.value));
        
        const customEmail = document.getElementById('customEmail').value.trim();
        if (customEmail) {{ supervisores.push(customEmail); }}
        
        if (supervisores.length === 0) {{
            alert("⚠️ Por favor, selecciona al menos un área de envío o ingresa un correo adicional.");
            return;
        }}

        const okBtns = document.querySelectorAll('.id-btn.selected');
        const nokBtns = document.querySelectorAll('.id-btn.deselected');
        const totalClinchados = okBtns.length + nokBtns.length;

        if (totalClinchados === 0) {{
            alert("⚠️ Por favor, selecciona un vehículo y parte de carrocería.");
            return;
        }}

        const piezasMalas = [];
        nokBtns.forEach(btn => {{
            piezasMalas.push({{
                nombre: `${{btn.getAttribute('data-subparte')}} (${{btn.getAttribute('data-id')}})`,
                estado: "Mal (NOK)"
            }});
        }});

        const porcentaje = ((okBtns.length / totalClinchados) * 100).toFixed(1) + '%';

        const btn = document.getElementById('btnSubmit');
        btn.innerText = 'GENERANDO PDF Y ENVIANDO...';
        btn.disabled = true;

        const data = {{
            supervisores: supervisores,
            inspector: document.getElementById('inspector').value,
            fecha: document.getElementById('fecha').value,
            auto: document.getElementById('auto').value,
            parte: document.getElementById('parte').value,
            vecesRegresado: document.getElementById('vecesRegresado').value,
            totalClinchados: totalClinchados,
            okCount: okBtns.length,
            nokCount: nokBtns.length,
            porcentaje: porcentaje,
            piezasMalas: piezasMalas,
            mod_punzon: document.getElementById('mod_punzon').value,
            mod_matriz: document.getElementById('mod_matriz').value
        }};

        try {{
            const response = await fetch('/enviar_correo', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(data) }});
            const result = await response.json();
            if(response.ok) {{
                const fbDiv = document.getElementById('feedbackContainer');
                fbDiv.style.display = 'block';
                fbDiv.style.backgroundColor = result.bg_color;
                fbDiv.innerHTML = result.feedback;
                fbDiv.scrollIntoView({{ behavior: 'smooth' }});
                alert('✅ Reporte PDF enviado exitosamente a: ' + supervisores.join(', '));
                
                document.getElementById('clinchadoForm').reset();
                document.getElementById('fecha').valueAsDate = new Date();
                document.getElementById('parte').innerHTML = '<option value="" disabled selected>Primero selecciona un vehículo</option>';
                document.getElementById('matrizWrapper').style.display = 'none';
                document.getElementById('nokContainer').innerHTML = '';
            }} else {{ alert('❌ Error: ' + result.error); }}
        }} catch (error) {{ alert('❌ Error de conexión.'); }}
        btn.innerText = 'GENERAR Y ENVIAR REPORTE PDF';
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
            nok_count = int(data.get('nokCount', 0))

            if fallo_modulo:
                dictamen = "DESGASTE CRÍTICO / FUERA DE TOLERANCIA (CAMBIAR MATRIZ)"
                bg_color = "#D6DCE5"
            elif nok_count > 0:
                dictamen = "DESGASTE INICIAL / PRECAUCIÓN (Aumentar frecuencia de inspección)"
                bg_color = "#E8EEF5"
            else:
                dictamen = "CONDICIÓN ÓPTIMA / ACEPTABLE (Continuar Proceso)"
                bg_color = "#F0F4F8"

            try:
                self.enviar_email(data, dictamen, bg_color)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok", 
                    "feedback": "Reporte PDF Generado y Enviado con éxito.",
                    "bg_color": "#A8A8A8"
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def enviar_email(self, data, dictamen, bg_color):
        API_KEY = os.environ.get("BREVO_API_KEY")
        SENDER_EMAIL = "ulyorther@gmail.com"
        
        lista_supervisores = data.get('supervisores', [])
        if not lista_supervisores:
            raise Exception("No se especificaron destinatarios.")
            
        to_payload = [{"email": email} for email in lista_supervisores]

        medios_vars = [data.get('mod_punzon', ''), data.get('mod_matriz', '')]
        medios_ok = sum(1 for v in medios_vars if v == 'Si')

        piezas_malas = data.get('piezasMalas', [])
        if piezas_malas:
            lista_nok_str = ", ".join([p['nombre'] for p in piezas_malas])
            fila_nok_html = f'<tr><td class="bg-light">Puntos NOK detectados:</td><td>{lista_nok_str}</td></tr>'
        else:
            fila_nok_html = '<tr><td class="bg-light">Puntos NOK detectados:</td><td>Ninguno</td></tr>'

        pdf_logo_html = f'<div style="text-align: center; margin-bottom: 10px;"><img src="{img_pdf_base64}" style="width: 160px; height: auto;" /></div>' if img_pdf_base64 else ''

        pdf_html = f'''
        <html>
        <head>
            <style>
                @page {{ size: letter; margin: 1.5cm; }}
                body {{ font-family: Helvetica, sans-serif; color: #1F2F57; }}
                h2 {{ color: #1F2F57; text-align: center; border-bottom: 2px solid #1F2F57; padding-bottom: 5px; margin-top: 0; margin-bottom: 10px; }}
                h3 {{ color: #1F2F57; font-size: 13px; margin-top: 10px; margin-bottom: 5px; border-bottom: 1px solid #A8A8A8; padding-bottom: 3px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
                th, td {{ border: 1px solid #A8A8A8; padding: 6px; font-size: 11px; text-align: left; }}
                th {{ background-color: #1F2F57; color: white; text-align: center; }}
                .bg-light {{ background-color: #F0F0F0; font-weight: bold; width: 40%; }}
                .dictamen {{ margin-top: 15px; padding: 10px; text-align: center; border: 2px solid #1F2F57; font-weight: bold; font-size: 14px; background-color: {bg_color}; }}
            </style>
        </head>
        <body>
            {pdf_logo_html}
            <h2>Reporte Oficial de Calidad - Clinchados</h2>
            
            <h3>1. Información del Ensamble</h3>
            <table>
                <tr><td class="bg-light">Inspector (Operador):</td><td>{data['inspector']}</td></tr>
                <tr><td class="bg-light">Fecha:</td><td>{data['fecha']}</td></tr>
                <tr><td class="bg-light">Automóvil Evaluado:</td><td>{data['auto']}</td></tr>
                <tr><td class="bg-light">Parte de la Carrocería:</td><td>{data['parte']}</td></tr>
                <tr><td class="bg-light">Veces Regresado:</td><td>{data['vecesRegresado']}</td></tr>
            </table>

            <h3>2. Resumen de Puntos de Clinchados</h3>
            <table>
                <tr>
                    <th>Total Evaluados</th><th>OK</th><th>NOK</th><th>Efectividad</th>
                </tr>
                <tr style="text-align: center;">
                    <td>{data['totalClinchados']}</td>
                    <td>{data['okCount']}</td>
                    <td style="font-weight: bold;">{data['nokCount']}</td>
                    <td>{data['porcentaje']}</td>
                </tr>
            </table>

            <h3>3. Resumen de Inspecciones</h3>
            <table>
                <tr><td class="bg-light">Medición:</td><td>{data['totalClinchados']}</td></tr>
                <tr><td class="bg-light">Inspección de medios:</td><td>{medios_ok} / 2</td></tr>
                {fila_nok_html}
            </table>

            <div class="dictamen">
                {dictamen}
            </div>
        </body>
        </html>
        '''

        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(pdf_html, dest=pdf_buffer)
        if pisa_status.err:
            raise Exception("Error interno al intentar generar el archivo PDF.")
        
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

        email_logo_html = f'<div style="text-align: center; margin-bottom: 20px;"><img src="{img_email_base64}" style="max-width: 150px; height: auto;" /></div>' if img_email_base64 else ''

        email_html = f'''<html><body style="font-family: Arial, sans-serif; color: #1F2F57; padding: 20px; background-color: #FDFAF9;">
            {email_logo_html}
            <h2 style="color: #6091C3; text-align: center;">Sistema de Inspección Volkswagen</h2>
            <p>Estimado equipo,</p>
            <p>Se ha generado un nuevo reporte de calidad oficial para la pieza <strong>{data['parte']}</strong> del vehículo <strong>{data['auto']}</strong>.</p>
            <p>El inspector <strong>{data['inspector']}</strong> ha adjuntado el informe detallado en formato PDF a este correo.</p>
            <br><hr style="border: 0; border-top: 1px solid #A8A8A8;"><br>
            <p style="font-size: 0.85em; color: #A8A8A8; text-align: center;">Este es un correo generado automáticamente por el Laboratorio de Soldadura. Por favor revise el PDF adjunto.</p>
        </body></html>'''

        payload = {
            "sender": {"email": SENDER_EMAIL, "name": "Inspección de Calidad VW"},
            "to": to_payload,
            "subject": f"Reporte PDF: {data['parte']} - {data['auto']} (Insp: {data['inspector']})",
            "htmlContent": email_html,
            "attachment": [
                {
                    "content": pdf_base64,
                    "name": f"Reporte_{data['auto']}_{data['parte']}.pdf"
                }
            ]
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
