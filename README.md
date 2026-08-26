<!-- ══════════════════════════ TÍTULO ══════════════════════════ -->
<div align="center">
  <img src="docs/title-banner.svg" width="100%" alt="Insight"/>
</div>

<!-- ══════════════════════ IDIOMAS / LANGUAGES ══════════════════════ -->
<div align="center">
<a href="README.md"><img src="https://img.shields.io/badge/Português-1987F0?style=for-the-badge" alt="Português"/></a>
<a href="README.en.md"><img src="https://img.shields.io/badge/English-555555?style=for-the-badge" alt="English"/></a>
<a href="README.es.md"><img src="https://img.shields.io/badge/Español-555555?style=for-the-badge" alt="Español"/></a>
</div>

<h1 align="center">Insight — Pipeline de Dados & Relatórios Automáticos</h1>
<p align="center"><em>Transforma registros brutos em um relatório de insights automático, com um único comando</em></p>
<p align="center"><strong>Ingestão → transformação → análise (tendência, anomalias) → relatório HTML/Markdown</strong></p>

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
<a href="#sobre"><img src="https://img.shields.io/badge/▸_SOBRE-1987F0?style=for-the-badge" alt="sobre"/></a>
<a href="#o-que-faz"><img src="https://img.shields.io/badge/▸_O_QUE_FAZ-000000?style=for-the-badge" alt="oquefaz"/></a>
<a href="#arquitetura"><img src="https://img.shields.io/badge/▸_ARQUITETURA-1987F0?style=for-the-badge" alt="arquitetura"/></a>
<a href="#uso"><img src="https://img.shields.io/badge/▸_USO-000000?style=for-the-badge" alt="uso"/></a>
<a href="#automação"><img src="https://img.shields.io/badge/▸_AUTOMAÇÃO-1987F0?style=for-the-badge" alt="automacao"/></a>
</div>

<br/>

> 💡 **Um comando, do CSV ao relatório.** `python -m insight run` já gera o dashboard HTML com o dataset de exemplo incluso.

<div align="center">
  <img src="docs/revenue.png" width="100%" alt="Insight — receita diária e tendência de 7 dias, com anomalias em vermelho"/>
</div>

## Sobre

**Insight** é um pipeline de dados pequeno, mas completo: ele ingere um CSV (ou consome uma API pública ao vivo), limpa e agrega os dados, detecta tendências e anomalias, e renderiza um relatório em HTML/Markdown com gráficos — tudo a partir de um único comando.

## O que faz

- **Ingestão** — carrega um CSV (com schema validado) ou busca cotações de câmbio ao vivo de uma API pública gratuita (sem chave).
- **Transformação** — corrige tipos, descarta linhas ruins, preenche lacunas de data, agrega em série diária e totais por categoria (pandas).
- **Análise** — média móvel de 7 dias, crescimento período-a-período, detecção de anomalias via z-score, ranking de categorias que mais cresceram, melhor/pior dia, e insights gerados em texto simples a partir dos números.
- **Relatório** — gráficos matplotlib + dashboard HTML autocontido + relatório Markdown.

**Exemplo de saída:**
```
• Total revenue of $7,027,351 across 180 days (2025-01-01 → 2025-06-29).
• Revenue is up 10.0% over the last 30 days vs the previous 30.
• Top category is Electronics ($3,217,331, 46% of revenue).
• Fastest-growing category: Sports (+12.8%).
• Detected 2 anomalous day(s); biggest is a spike on 2025-01-31 (z=+2.8).
```

| Receita por categoria | Crescimento por categoria |
|:---:|:---:|
| ![Por categoria](docs/category.png) | ![Crescimento](docs/growth.png) |

## Arquitetura

<div align="center">
  <img src="docs/architecture.svg" width="100%" alt="Arquitetura"/>
</div>

| Módulo | Responsabilidade |
|---|---|
| `insight/ingest.py` | Carrega e valida o CSV de entrada |
| `insight/transform.py` | Limpa, corrige tipos, agrega (série diária, por categoria) |
| `insight/analyze.py` | Média móvel, crescimento, anomalias por z-score, ranking, insights |
| `insight/report.py` | Renderiza gráficos e o relatório HTML/Markdown |
| `insight/sources.py` | Fonte ao vivo opcional (API de câmbio Frankfurter) |
| `insight/cli.py` | Interface de linha de comando `python -m insight run` |

## Uso

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m insight run
python -m insight run --input data/sample_sales.csv --out report --window 30 --z 2.5
python -m insight run --source frankfurter   # dataset público ao vivo
```

Abra `report/index.html` para ver o dashboard.

**Testes:**
```bash
pytest -q
```

## Automação

`.github/workflows/report.yml` regenera o relatório **toda segunda-feira** (e sob demanda), disponibilizando-o como artefato para download — analytics agendado sem nenhuma infraestrutura. `ci.yml` roda a suíte de testes a cada push.

## Licença

[MIT](LICENSE).

<div align="center">
  <img src="https://file.loading.io/color/feature/thumb/Blues-8.png?" width="100%" height="10px" alt="divider"/>
</div>

<p align="center"><sub>Desenvolvido por <strong><a href="https://github.com/geoggrigori">Grigori</a></strong> · 2026</sub></p>
