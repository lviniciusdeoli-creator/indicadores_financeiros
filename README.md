📈 Stock Indicators — Análise Fundamentalista Automatizada

Sistema de coleta diária de indicadores financeiros para ações brasileiras e internacionais, com atualização automática via GitHub Actions, armazenamento em JSON e integração direta com Google Sheets através de Google Apps Script.

✨ Funcionalidades
Coleta automática de indicadores fundamentalistas e financeiros
Atualização diária utilizando GitHub Actions
Geração automática de arquivo JSON estruturado
Integração com Google Sheets via função personalizada
Suporte a ações da B3 e mercados internacionais
Hospedagem gratuita utilizando GitHub Pages ou Raw GitHub
Fácil manutenção através de lista de tickers configurável

📁 Estrutura do Repositório
.
├── .github/
│   └── workflows/
│       └── update_stocks.yml      # Automação diária (GitHub Actions)
├── stock_indicators.py            # Script principal de coleta
├── tickers.txt                    # Lista de ativos monitorados
├── analise_acoes.json             # JSON gerado automaticamente
├── google_apps_script.gs          # Integração com Google Sheets
├── requirements.txt               # Dependências do projeto
└── README.md
🚀 Configuração em 3 Passos
1. Configure o Repositório

Clone o projeto:

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

Edite o arquivo tickers.txt com os ativos que deseja monitorar:

PETR4.SA
VALE3.SA
ITUB4.SA
AAPL
MSFT

Salve as alterações:

git add tickers.txt
git commit -m "feat: configura lista de tickers"
git push
2. Ative o GitHub Actions

No GitHub:

Acesse Settings → Actions → General
Em Workflow permissions, selecione:
✅ Read and write permissions
Salve as alterações

O workflow será executado automaticamente todos os dias.

Para executar manualmente:

Actions
└── Atualizar Indicadores de Ações
    └── Run workflow
3. Configure o Google Sheets
Abra sua planilha
Vá em Extensões → Apps Script
Cole o conteúdo do arquivo google_apps_script.gs
Localize a constante JSON_URL
Substitua pelo endereço do seu JSON:
const JSON_URL =
  "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/analise_acoes.json";
Salve o projeto
Autorize as permissões quando solicitado
📝 Configurando os Tickers

O arquivo tickers.txt define quais ativos serão monitorados.

Ações Brasileiras

Utilize o sufixo .SA

PETR4.SA
VALE3.SA
ITUB4.SA
Ações Americanas
AAPL
MSFT
GOOGL
AMZN

Também é possível informar múltiplos ativos por linha:

PETR4.SA, VALE3.SA, ITUB4.SA
AAPL, MSFT, GOOGL
📊 Utilização no Google Sheets
Consultar Indicadores Específicos
=INDICADORES("AAPL"; "pe_ratio_trailing;roe_pct;profit_margin_pct")

Retorna:

P/L
ROE
Margem Líquida
Dividend Yield e EV/EBITDA
=INDICADORES("PETR4.SA"; "dividend_yield_ttm_pct;ev_ebitda")
Todos os Indicadores Disponíveis
=INDICADORES("VALE3.SA"; "TODOS")
Histórico Anual
=HISTORICO_ANUAL("AAPL")

Retorna:

Receita
Lucro Líquido
Crescimento anual
Listar Ativos Monitorados
=LISTAR_TICKERS()
Última Atualização
=ULTIMA_ATUALIZACAO()
⚙️ Execução Local

Instale as dependências:

pip install -r requirements.txt
Modo Interativo
python stock_indicators.py

O script solicitará os tickers via terminal.

Modo Automático (CI/CD)
python stock_indicators.py --ci

Neste modo, os tickers serão lidos automaticamente do arquivo tickers.txt.

📦 Principais Indicadores Disponíveis
Preço Atual
Market Cap
P/L (Trailing e Forward)
P/VP
Dividend Yield
EV/EBITDA
ROE
ROIC
ROA
Margem Bruta
Margem Operacional
Margem Líquida
Receita
Lucro Líquido
Fluxo de Caixa Livre
Dívida Líquida
Crescimento de Receita
Crescimento de Lucro
📄 Licença

Este projeto é distribuído sob a licença MIT.

MIT License

Copyright (c) 2026 Lucas Oliveira

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
