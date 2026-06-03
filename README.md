📈 Stock Indicators — Análise Fundamentalista Automatizada
Coleta diária de indicadores financeiros via GitHub Actions, salva em JSON e expõe os dados para o Google Sheets via Apps Script.

📁 Estrutura do repositório
├── .github/
│   └── workflows/
│       └── update_stocks.yml   # Agendamento e automação (GitHub Actions)
├── stock_indicators.py         # Script principal de coleta
├── tickers.txt                 # Lista de ativos monitorados ← edite aqui
├── analise_acoes.json          # JSON gerado automaticamente (não editar)
├── google_apps_script.gs       # Código para o Google Sheets
└── README.md

🚀 Setup em 3 passos
1 — Configure o repositório
bashgit clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
# Edite tickers.txt com os ativos que deseja monitorar
git add tickers.txt
git commit -m "feat: configura lista de tickers"
git push
2 — Ative o GitHub Actions

Vá em Settings → Actions → General
Em Workflow permissions, selecione Read and write permissions
O workflow será executado todo dia às 08:00 BRT automaticamente
Para testar agora: Actions → Atualizar Indicadores de Ações → Run workflow

3 — Configure o Google Sheets

Abra sua planilha → Extensões → Apps Script
Cole o conteúdo de google_apps_script.gs
Em JSON_URL, substitua pelo link raw do seu repositório:

   https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/analise_acoes.json

Salve e autorize as permissões quando solicitado


📋 Editando tickers.txt
# Ações brasileiras (sufixo .SA obrigatório)
PETR4.SA
VALE3.SA, ITUB4.SA    ← múltiplos por linha também funcionam

# Ações americanas
AAPL
MSFT

📊 Usando no Google Sheets
FórmulaResultado=INDICADORES("AAPL"; "pe_ratio_trailing;roe_pct;profit_margin_pct")Tabela com os 3 indicadores=INDICADORES("PETR4.SA"; "dividend_yield_ttm_pct;ev_ebitda")DY e EV/EBITDA da Petrobras=INDICADORES("VALE3.SA"; "TODOS")Todos os indicadores disponíveis=HISTORICO_ANUAL("AAPL")Histórico anual de receita e lucro=LISTAR_TICKERS()Lista todos os tickers no JSON=ULTIMA_ATUALIZACAO()Data/hora da última coleta

⚙️ Execução local
bashpip install yfinance pandas
python stock_indicators.py              # modo interativo (digita os tickers)
python stock_indicators.py --ci         # modo CI (lê tickers.txt)
