"""Prepara `fichas_vencidas.csv` a partir de la versión pública del RUTS (folio PNT 130213100101626).

Uso:
    python -I preparar_datos.py <carpeta_salida_pnt>

Lee `01_catalogo_tramites.csv` y `04b_consultas_mensuales.csv`, se queda con las fichas publicadas cuya
última actualización ya excedió el periodo de actualización declarado a la fecha de corte de la base
(2026-08-12) y escribe un CSV con columnas estructurales del catálogo: ningún dato de personas.
"""
import csv
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path

CORTE = dt.date(2026, 8, 12)                      # último registro que obra en la base entregada
PERIODO_DIAS = {"Trimestral": 91, "Semestral": 182, "Anual": 365}
VENTANA_CONSULTAS = ("2025-08", "2026-07")        # doce meses completos anteriores al corte
TOLERANCIA_DIAS = 60                              # plazo de regularización supuesto, en días naturales
HORAS_POR_DIA, DIAS_HABILES = 1.0, 5 / 7          # hora diaria que la mesa dedica al rezago y conversión a días hábiles
HORAS_BASE, HORAS_POR_DOCUMENTO, CARACTERES_POR_HORA, HORAS_MAXIMAS = 1.0, 0.25, 800.0, 16.0

csv.field_size_limit(10 ** 9)


def fecha(texto: str):
    try:
        return dt.datetime.fromisoformat(texto[:10]).date()
    except ValueError:
        return None


def sin_html(texto: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", texto or "")).strip()


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()


def redondear_media_hora(x: float) -> float:
    return round(x * 2) / 2


def main(carpeta: Path) -> None:
    consultas = {}
    with open(carpeta / "04b_consultas_mensuales.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if VENTANA_CONSULTAS[0] <= r["periodo"] <= VENTANA_CONSULTAS[1]:
                consultas[r["idtram"]] = consultas.get(r["idtram"], 0) + int(float(r["consultas_ficha"] or 0))

    filas = []
    with open(carpeta / "01_catalogo_tramites.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["estatus"] != "Publicado":
                continue
            ultima = fecha(r["fecha_ultima_actualizacion"])
            if ultima is None:
                continue
            periodo = PERIODO_DIAS.get(r["periodo_actualizacion"], PERIODO_DIAS["Trimestral"])
            dias_vencida = (CORTE - ultima).days - periodo
            if dias_vencida <= 0:
                continue
            caracteres = sum(len(sin_html(r[c])) for c in ("descripcion", "requisitos", "documentos", "fundamento_juridico"))
            n_documentos = len([x for x in r["documentos"].split(" | ") if x.strip()])
            p = min(HORAS_MAXIMAS, HORAS_BASE + HORAS_POR_DOCUMENTO * n_documentos + caracteres / CARACTERES_POR_HORA)
            # Plazo en horas de mesa desde el corte; una ficha que ya rebasó la tolerancia es exigible de inmediato (d = 0).
            d = max(0.0, (TOLERANCIA_DIAS - dias_vencida) * DIAS_HABILES * HORAS_POR_DIA)
            filas.append({
                "idtram": r["idtram"], "nombre": sin_html(r["nombre"]), "nombre_normalizado": normalizar(sin_html(r["nombre"])),
                "tipo": r["tipo"], "nivel": r["nivel"], "modalidad": r["modalidad"], "orden_gobierno": r["orden_gobierno"],
                "secretaria_u_organismo": r["secretaria_u_organismo"], "dependencia": r["dependencia"],
                "periodo_actualizacion": r["periodo_actualizacion"], "fecha_registro": (fecha(r["fecha_registro"]) or "").isoformat()
                if fecha(r["fecha_registro"]) else "", "fecha_ultima_actualizacion": ultima.isoformat(),
                "dias_vencida": dias_vencida, "caracteres": caracteres, "n_documentos": n_documentos,
                "consultas_12m": consultas.get(r["idtram"], 0), "p_horas": redondear_media_hora(p), "d_horas": round(d, 1),
            })

    # Peso de tardanza por cuartil de consultas en el conjunto completo de fichas vencidas: 1 (menos consultadas) a 4.
    valores = sorted(f_["consultas_12m"] for f_ in filas)
    cortes = [valores[int(q * len(valores))] for q in (0.25, 0.50, 0.75)]
    for f_ in filas:
        f_["w"] = 1 + sum(f_["consultas_12m"] > c for c in cortes)

    filas.sort(key=lambda f_: (f_["orden_gobierno"], f_["secretaria_u_organismo"], f_["dependencia"], f_["idtram"]))
    destino = Path(__file__).resolve().parent / "fichas_vencidas.csv"
    with open(destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} fichas vencidas al {CORTE} → {destino.name}; cuartiles de consultas: {cortes}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
