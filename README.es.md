<!-- ══════════════════════════ PORTADA ══════════════════════════ -->
<div align="center">
  <img src="docs/title-banner.svg" width="100%" alt="Insight"/>
</div>

<br/>

<!-- ══════════════════════ IDIOMAS / LANGUAGES ══════════════════════ -->
<div align="center">
<a href="README.md"><img src="https://img.shields.io/badge/Português-555555?style=for-the-badge" alt="Português"/></a>
<a href="README.en.md"><img src="https://img.shields.io/badge/English-555555?style=for-the-badge" alt="English"/></a>
<a href="README.es.md"><img src="https://img.shields.io/badge/Español-1987F0?style=for-the-badge" alt="Español"/></a>
</div>

<br/>

<div align="center">
<img src="https://github.com/geoggrigori/insight-pipeline/actions/workflows/ci.yml/badge.svg" alt="CI"/>
<br/>
<img src="https://img.shields.io/badge/Python_3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="python"/>
<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas"/>
<img src="https://img.shields.io/badge/matplotlib-11557C?style=flat-square" alt="matplotlib"/>
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest"/>
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="actions"/>
</div>

<div align="center">
<a href="#acerca-de"><img src="https://img.shields.io/badge/▸_ACERCA_DE-1987F0?style=for-the-badge" alt="acerca"/></a>
<a href="#qué-hace"><img src="https://img.shields.io/badge/▸_QUÉ_HACE-000000?style=for-the-badge" alt="quehace"/></a>
<a href="#arquitectura"><img src="https://img.shields.io/badge/▸_ARQUITECTURA-1987F0?style=for-the-badge" alt="arquitectura"/></a>
<a href="#uso"><img src="https://img.shields.io/badge/▸_USO-000000?style=for-the-badge" alt="uso"/></a>
<a href="#automatización"><img src="https://img.shields.io/badge/▸_AUTOMATIZACIÓN-1987F0?style=for-the-badge" alt="automatizacion"/></a>
</div>

<br/>

> 💡 **Un comando, del CSV al reporte.** `python -m insight run` ya genera el dashboard HTML con el dataset de ejemplo incluido.

<div align="center">
  <img src="docs/revenue.png" width="100%" alt="Insight — ingreso diario y tendencia de 7 días, anomalías en rojo"/>
</div>

## Acerca de

**Insight** es un pipeline de datos pequeño pero completo: ingiere un CSV (o consume una API pública en vivo), limpia y agrega los datos, detecta tendencias y anomalías, y renderiza un reporte en HTML/Markdown con gráficos — todo desde un solo comando.

## Qué hace

- **Ingesta** — carga un CSV (con schema validado) o trae tasas de cambio en vivo de una API pública gratuita (sin clave).
- **Transformación** — corrige tipos, descarta filas malas, rellena huecos de fecha, agrega en serie diaria y totales por categoría (pandas).
- **Análisis** — media móvil de 7 días, crecimiento periodo a periodo, detección de anomalías vía z-score, ranking de categorías con más crecimiento, mejor/peor día, e insights en texto simple generados a partir de los números.
- **Reporte** — gráficos matplotlib + dashboard HTML autocontenido + reporte Markdown.

**Ejemplo de salida:**
```
• Total revenue of $7,027,351 across 180 days (2025-01-01 → 2025-06-29).
• Revenue is up 10.0% over the last 30 days vs the previous 30.
• Top category is Electronics ($3,217,331, 46% of revenue).
• Fastest-growing category: Sports (+12.8%).
• Detected 2 anomalous day(s); biggest is a spike on 2025-01-31 (z=+2.8).
```

| Ingreso por categoría | Crecimiento por categoría |
|:---:|:---:|
| ![Por categoría](docs/category.png) | ![Crecimiento](docs/growth.png) |

## Arquitectura

<div align="center">
  <img src="docs/architecture.svg" width="100%" alt="Arquitectura"/>
</div>

| Módulo | Responsabilidad |
|---|---|
| `insight/ingest.py` | Carga y valida el CSV de entrada |
| `insight/transform.py` | Limpia, corrige tipos, agrega (serie diaria, por categoría) |
| `insight/analyze.py` | Media móvil, crecimiento, anomalías por z-score, ranking, insights |
| `insight/report.py` | Renderiza gráficos y el reporte HTML/Markdown |
| `insight/sources.py` | Fuente en vivo opcional (API de cambio Frankfurter) |
| `insight/cli.py` | Interfaz de línea de comandos `python -m insight run` |

## Uso

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m insight run
python -m insight run --input data/sample_sales.csv --out report --window 30 --z 2.5
python -m insight run --source frankfurter   # dataset público en vivo
```

Abre `report/index.html` para ver el dashboard.

**Pruebas:**
```bash
pytest -q
```

## Automatización

`.github/workflows/report.yml` regenera el reporte **cada lunes** (y bajo demanda), subiéndolo como artefacto descargable — analytics programado sin ninguna infraestructura. `ci.yml` corre la suite de pruebas en cada push.

## Licencia

[MIT](LICENSE).

<div align="center">
  <img src="https://file.loading.io/color/feature/thumb/Blues-8.png?" width="100%" height="10px" alt="divider"/>
</div>

<p align="center"><sub>Desarrollado por <strong><a href="https://github.com/geoggrigori">Grigori</a></strong> · 2026</sub></p>
