# Insight 📊 — Pipeline de Datos & Informes Automatizados

[English](README.md) · [Português](README.pt.md) · **Español**

Un **pipeline de datos** pequeño pero completo que convierte registros en bruto en un **informe de insights automatizado**: ingiere un CSV (o una API pública en vivo), limpia y agrega los datos, detecta tendencias y anomalías, y genera un informe en HTML/Markdown con gráficos, todo desde un único comando.

> Ingesta → Transformación → Análisis → Informe, en Python limpio y probado.

![CI](https://github.com/geoggrigori/insight-pipeline/actions/workflows/ci.yml/badge.svg)

---

## ✨ Qué hace

- **Ingesta** — carga un CSV (con esquema validado) o consulta tipos de cambio en vivo desde una API pública gratuita (sin clave).
- **Transformación** — convierte tipos, descarta filas inválidas, rellena huecos de fechas, agrega en una serie diaria y en totales por categoría (pandas).
- **Análisis** —
  - tendencia por **media móvil** de 7 días
  - **crecimiento período a período** (últimos *N* días vs. los *N* anteriores)
  - **detección de anomalías** mediante z-scores (señala picos/caídas inusuales)
  - ranking de **crecimiento por categoría** (mayores variaciones)
  - mejor/peor día, composición por categoría
  - un conjunto de **insights en lenguaje natural** generados a partir de las cifras
- **Informe** — gráficos con matplotlib y un **panel HTML** autónomo, además de un informe en **Markdown**.

## 🚀 Uso

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run on the bundled sample dataset
python -m insight run

# Options
python -m insight run --input data/sample_sales.csv --out report --window 30 --z 2.5

# Or pull a live public dataset (FX rates, no API key)
python -m insight run --source frankfurter
```

Abre `report/index.html` para ver el panel.

### Ejemplo de salida

```
• Total revenue of $7,027,351 across 180 days (2025-01-01 → 2025-06-29).
• Revenue is up 10.0% over the last 30 days vs the previous 30.
• Top category is Electronics ($3,217,331, 46% of revenue).
• Fastest-growing category: Sports (+12.8%).
• Best day: 2025-01-31 ($59,594); slowest day: 2025-01-02 ($25,158).
• Detected 2 anomalous day(s); biggest is a spike on 2025-01-31 (z=+2.8).
```

### Gráficos generados

El pipeline genera estos gráficos automáticamente (salida real del conjunto de datos incluido):

| Ingresos diarios & tendencia de 7 días (anomalías en rojo) |
|:----------------------------------------------:|
| ![Daily revenue](docs/revenue.png) |

| Ingresos por categoría | Crecimiento por categoría |
|:-------------------:|:---------------:|
| ![By category](docs/category.png) | ![Growth](docs/growth.png) |

## 🏗️ Arquitectura

![Architecture](docs/architecture.svg)

| Módulo | Responsabilidad |
|--------|----------------|
| `insight/ingest.py`    | Carga + valida el CSV de entrada |
| `insight/transform.py` | Limpia, convierte tipos, agrega (serie diaria, por categoría) |
| `insight/analyze.py`   | Media móvil, crecimiento, anomalías por z-score, variaciones por categoría, insights |
| `insight/report.py`    | Genera los gráficos y el informe en HTML/Markdown |
| `insight/sources.py`   | Fuente en vivo opcional (API de divisas Frankfurter) |
| `insight/cli.py`       | Interfaz de línea de comandos `python -m insight run` |
| `scripts/make_sample.py` | Regenera el conjunto de datos de ejemplo determinista |

## 🧪 Pruebas

```bash
pytest -q
```

El núcleo de análisis está cubierto por pruebas unitarias deterministas — media móvil, cálculo de crecimiento, detección de anomalías y ranking por categoría sobre entradas conocidas, además de una verificación de extremo a extremo de `analyze()`.

## ⏱️ Automatización

`.github/workflows/report.yml` regenera el informe **cada lunes** (y bajo demanda) y lo publica como un artefacto descargable — una configuración sencilla de "analítica programada", sin infraestructura. `ci.yml` ejecuta la suite de pruebas en cada push.

## 🛠️ Stack tecnológico

- **Python** (3.13+), **pandas**, **matplotlib**
- **Pruebas:** pytest
- **Automatización:** GitHub Actions (CI + informe programado)

## 📝 Notas

- El conjunto de datos incluido es **sintético pero realista** (tendencia + estacionalidad semanal + anomalías inyectadas), generado de forma determinista por `scripts/make_sample.py`.
- El pipeline es **agnóstico respecto a la métrica**: apúntalo a cualquier CSV con formato `date, category, units, revenue`, o adapta `sources.py` a otra fuente.

---

Creado como proyecto de portafolio para demostrar un flujo de datos de extremo a extremo: ingesta, limpieza, análisis, visualización y automatización.
