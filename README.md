# 📈 Stock Indicators — Análise Fundamentalista Automatizada

Sistema de coleta diária de indicadores financeiros para ações brasileiras e internacionais, com atualização automática via GitHub Actions, armazenamento em JSON e integração direta com Google Sheets através de Google Apps Script.

---

## ✨ Funcionalidades

- Coleta automática de indicadores fundamentalistas e financeiros
- Atualização diária utilizando GitHub Actions
- Geração automática de arquivo JSON estruturado
- Integração com Google Sheets via função personalizada
- Suporte a ações da B3 e mercados internacionais
- Hospedagem gratuita utilizando GitHub Pages ou Raw GitHub
- Fácil manutenção através de lista de tickers configurável

---

## 📁 Estrutura do Repositório

```text
.
├── .github/
│   └── workflows/
│       └── update_stocks.yml
├── stock_indicators.py
├── tickers.txt
├── analise_acoes.json
├── google_apps_script.gs
├── requirements.txt
└── README.md
```

| Arquivo | Descrição |
|----------|------------|
| `update_stocks.yml` | Automação diária via GitHub Actions |
| `stock_indicators.py` | Script principal de coleta |
| `tickers.txt` | Lista de ativos monitorados |
| `analise_acoes.json` | JSON gerado automaticamente |
| `google_apps_script.gs` | Integração com Google Sheets |
| `requirements.txt` | Dependências do projeto |

---

# 🚀 Configuração em 3 Passos

## 1️⃣ Configure o Repositório

Clone o projeto:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Edite o arquivo `tickers.txt` com os ativos que deseja monitorar:

```text
PETR4.SA
VALE3.SA
ITUB4.SA
AAPL
MSFT
```

Salve as alterações:

```bash
git add tickers.txt
git commit -m "feat: configura lista de tickers"
git push
```

---

## 2️⃣ Ative o GitHub Actions

No GitHub:

1. Acesse **Settings → Actions → General**
2. Em **Workflow permissions**, selecione:
   - ✅ Read and write permissions
3. Clique em **Save**

O workflow será executado automaticamente todos os dias.

Para executar manualmente:

```text
Actions
└── Atualizar Indicadores de Ações
    └── Run workflow
```

---

## 3️⃣ Configure o Google Sheets

1. Abra sua planilha
2. Vá em **Extensões → Apps Script**
3. Cole o conteúdo de `google_apps_script.gs`
4. Localize a constante `JSON_URL`
5. Substitua pelo endereço do seu JSON:

```javascript
const JSON_URL =
  "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/analise_acoes.json";
```

6. Salve o projeto
7. Autorize as permissões quando solicitado

---

# 📝 Configurando os Tickers

O arquivo `tickers.txt` define quais ativos serão monitorados.

## 🇧🇷 Ações Brasileiras

Utilize obrigatoriamente o sufixo `.SA`.

```text
PETR4.SA
VALE3.SA
ITUB4.SA
```

## 🇺🇸 Ações Americanas

```text
AAPL
MSFT
GOOGL
AMZN
```

Também é possível informar múltiplos ativos por linha:

```text
PETR4.SA, VALE3.SA, ITUB4.SA
AAPL, MSFT, GOOGL
```

---

# 📊 Utilização no Google Sheets

## Consultar Indicadores Específicos

```excel
=INDICADORES("AAPL"; "pe_ratio_trailing;roe_pct;profit_margin_pct")
```

Retorna:

- P/L
- ROE
- Margem Líquida

---

## Dividend Yield e EV/EBITDA

```excel
=INDICADORES("PETR4.SA"; "dividend_yield_ttm_pct;ev_ebitda")
```

---

## Todos os Indicadores Disponíveis

```excel
=INDICADORES("VALE3.SA"; "TODOS")
```

---

## Histórico Anual

```excel
=HISTORICO_ANUAL("AAPL")
```

Retorna:

- Receita
- Lucro Líquido
- Crescimento Anual

---

## Listar Ativos Monitorados

```excel
=LISTAR_TICKERS()
```

---

## Última Atualização

```excel
=ULTIMA_ATUALIZACAO()
```

---

# ⚙️ Execução Local

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Modo Interativo

```bash
python stock_indicators.py
```

O script solicitará os tickers via terminal.

## Modo Automático (CI/CD)

```bash
python stock_indicators.py --ci
```

Neste modo, os tickers serão lidos automaticamente do arquivo `tickers.txt`.

---

# 📦 Principais Indicadores Disponíveis

- Preço Atual
- Market Cap
- P/L (Trailing e Forward)
- P/VP
- Dividend Yield
- EV/EBITDA
- ROE
- ROIC
- ROA
- Margem Bruta
- Margem Operacional
- Margem Líquida
- Receita
- Lucro Líquido
- Fluxo de Caixa Livre
- Dívida Líquida
- Crescimento de Receita
- Crescimento de Lucro

---

# 📄 Licença

Este projeto está licenciado sob a Licença MIT.

Consulte o arquivo `LICENSE` para mais informações.
