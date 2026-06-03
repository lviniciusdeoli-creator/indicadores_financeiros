"""
=============================================================
  SCRIPT DE ANÁLISE FUNDAMENTALISTA DE AÇÕES
  Fonte principal: Yahoo Finance (via yfinance)
  Foco: Indicadores para investimento de longo prazo

  Modo de execução:
    - Local (interativo):  python stock_indicators.py
    - GitHub Actions:      python stock_indicators.py --ci
      Neste modo, os tickers são lidos de "tickers.txt"
      e o JSON é salvo em "analise_acoes.json"
=============================================================
"""

import yfinance as yf
import json
import sys
import os
from datetime import datetime, date

# ─────────────────────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────────────────────

def formatar_percentual(valor):
    """
    Normaliza um valor para percentual arredondado.

    O yfinance é INCONSISTENTE dependendo do ticker e da versão:
      - Alguns campos retornam decimal:    0.0726  → deve virar  7.26
      - Outros já retornam o percentual:   8.44    → deve ficar  8.44

    Heurística adotada:
      • Se |valor| <= 1  → assume decimal  → multiplica por 100
      • Se |valor| >  1  → assume que já está em percentual → apenas arredonda

    Limitação conhecida: ROE/ROA > 100% chegam como decimal > 1 (ex: 1.47 = 147%).
    Para esses casos usa-se formatar_percentual_forcado() que sempre multiplica por 100.
    """
    if valor is None:
        return None
    if abs(valor) > 1:
        # Já está em formato percentual (ex: dividendYield = 8.44)
        return round(valor, 2)
    # Está em formato decimal (ex: profitMargins = 0.0726)
    return round(valor * 100, 2)


def formatar_percentual_forcado(valor):
    """
    Versão que SEMPRE multiplica por 100, independente do valor.
    Usada para campos que o yfinance garante retornar como decimal,
    mesmo quando > 1 (ex: ROE = 1.47 significa 147%, não 1.47%).
    """
    if valor is None:
        return None
    return round(valor * 100, 2)

def formatar_moeda_bilhoes(valor):
    """Converte valor bruto para bilhões"""
    if valor is None:
        return None
    return round(valor / 1_000_000_000, 3)

def formatar_moeda_milhoes(valor):
    """Converte valor bruto para milhões"""
    if valor is None:
        return None
    return round(valor / 1_000_000, 2)

def safe_get(dicionario, chave, padrao=None):
    """Retorna valor do dicionário ou None se ausente/inválido (trata Infinity/NaN)"""
    valor = dicionario.get(chave, padrao)
    if isinstance(valor, float) and (valor != valor or valor == float("inf") or valor == float("-inf")):
        return None
    return valor

def json_serial(obj):
    """Serializador customizado para tipos não suportados pelo json padrão"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Tipo não serializável: {type(obj)}")


# ─────────────────────────────────────────────────────────────
# LEITURA DOS TICKERS
# ─────────────────────────────────────────────────────────────

def ler_tickers_do_arquivo(caminho: str = "tickers.txt") -> list:
    """
    Lê a lista de tickers do arquivo tickers.txt.
    Ignora linhas vazias e comentários (linhas que começam com #).
    Aceita múltiplos tickers por linha separados por vírgula.
    """
    if not os.path.exists(caminho):
        print(f"⚠  Arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    tickers = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            # Ignora comentários e linhas vazias
            if not linha or linha.startswith("#"):
                continue
            # Suporta múltiplos tickers por linha separados por vírgula
            partes = [t.strip().upper() for t in linha.split(",") if t.strip()]
            tickers.extend(partes)

    # Remove duplicatas mantendo a ordem
    vistos = set()
    tickers_unicos = []
    for t in tickers:
        if t not in vistos:
            vistos.add(t)
            tickers_unicos.append(t)

    return tickers_unicos


# ─────────────────────────────────────────────────────────────
# COLETA DE INDICADORES
# ─────────────────────────────────────────────────────────────

def coletar_indicadores(ticker: str) -> dict:
    """
    Coleta todos os indicadores fundamentalistas de um ticker via yfinance.
    Retorna dicionário estruturado com valuation, rentabilidade,
    saúde financeira, dados de mercado e histórico financeiro.
    """
    print(f"  → Buscando dados para: {ticker} ...")

    try:
        ativo = yf.Ticker(ticker)
        info  = ativo.info
    except Exception as e:
        return {"erro": f"Falha ao acessar '{ticker}': {str(e)}"}

    if not info or safe_get(info, "symbol") is None:
        return {"erro": f"Ticker '{ticker}' não encontrado ou sem dados."}

    # ── 1. IDENTIFICAÇÃO ─────────────────────────────────────
    identificacao = {
        "ticker":         safe_get(info, "symbol"),
        "nome":           safe_get(info, "longName") or safe_get(info, "shortName"),
        "setor":          safe_get(info, "sector"),
        "industria":      safe_get(info, "industry"),
        "pais":           safe_get(info, "country"),
        "moeda":          safe_get(info, "currency"),
        "bolsa":          safe_get(info, "exchange"),
        "site":           safe_get(info, "website"),
        "resumo_negocio": safe_get(info, "longBusinessSummary"),
    }

    # ── 2. VALUATION ─────────────────────────────────────────
    valuation = {
        "preco_atual":              safe_get(info, "currentPrice") or safe_get(info, "regularMarketPrice"),
        "pe_ratio_trailing":        safe_get(info, "trailingPE"),          # P/E histórico
        "pe_ratio_forward":         safe_get(info, "forwardPE"),           # P/E estimado
        "pb_ratio":                 safe_get(info, "priceToBook"),         # Preço / Valor Patrimonial
        "ps_ratio":                 safe_get(info, "priceToSalesTrailing12Months"),
        "ev_ebitda":                safe_get(info, "enterpriseToEbitda"),  # EV/EBITDA
        "ev_receita":               safe_get(info, "enterpriseToRevenue"),
        "eps_ttm":                  safe_get(info, "trailingEps"),         # Lucro/ação (12m)
        "eps_forward":              safe_get(info, "forwardEps"),          # Lucro/ação estimado
        "dividend_yield_ttm_pct":   formatar_percentual(safe_get(info, "dividendYield")),
        "dividendo_por_acao":       safe_get(info, "dividendRate"),
        "payout_ratio_pct":         formatar_percentual_forcado(safe_get(info, "payoutRatio")),
        "peg_ratio":                safe_get(info, "pegRatio"),
    }

    # ── 3. RENTABILIDADE ─────────────────────────────────────
    # Estes campos o yfinance SEMPRE retorna como decimal (ex: returnOnEquity=1.47 = 147%),
    # por isso usamos formatar_percentual_forcado que multiplica por 100 incondicionalmente.
    rentabilidade = {
        "gross_margin_pct":              formatar_percentual_forcado(safe_get(info, "grossMargins")),
        "operating_margin_pct":          formatar_percentual_forcado(safe_get(info, "operatingMargins")),
        "profit_margin_pct":             formatar_percentual_forcado(safe_get(info, "profitMargins")),
        "roe_pct":                       formatar_percentual_forcado(safe_get(info, "returnOnEquity")),
        "roa_pct":                       formatar_percentual_forcado(safe_get(info, "returnOnAssets")),
        "roi_estimado_pct":              _calcular_roi(info),
        "crescimento_receita_yoy_pct":   formatar_percentual_forcado(safe_get(info, "revenueGrowth")),
        "crescimento_lucro_yoy_pct":     formatar_percentual_forcado(safe_get(info, "earningsGrowth")),
        "crescimento_eps_qoq_pct":       formatar_percentual_forcado(safe_get(info, "earningsQuarterlyGrowth")),
    }

    # ── 4. SAÚDE FINANCEIRA ──────────────────────────────────
    saude_financeira = {
        "debt_to_equity":           safe_get(info, "debtToEquity"),
        "divida_total_bi":          formatar_moeda_bilhoes(safe_get(info, "totalDebt")),
        "caixa_total_bi":           formatar_moeda_bilhoes(safe_get(info, "totalCash")),
        "caixa_por_acao":           safe_get(info, "totalCashPerShare"),
        "current_ratio":            safe_get(info, "currentRatio"),
        "quick_ratio":              safe_get(info, "quickRatio"),
        "book_value_por_acao":      safe_get(info, "bookValue"),
        "ebitda_bi":                formatar_moeda_bilhoes(safe_get(info, "ebitda")),
        "free_cash_flow_bi":        formatar_moeda_bilhoes(safe_get(info, "freeCashflow")),
        "operating_cash_flow_bi":   formatar_moeda_bilhoes(safe_get(info, "operatingCashflow")),
    }

    # ── 5. MERCADO ───────────────────────────────────────────
    mercado = {
        "market_cap_bi":                formatar_moeda_bilhoes(safe_get(info, "marketCap")),
        "enterprise_value_bi":          formatar_moeda_bilhoes(safe_get(info, "enterpriseValue")),
        "acoes_em_circulacao_bi":       formatar_moeda_bilhoes(safe_get(info, "sharesOutstanding")),
        "float_acoes_bi":               formatar_moeda_bilhoes(safe_get(info, "floatShares")),
        "beta":                         safe_get(info, "beta"),
        "52w_max":                      safe_get(info, "fiftyTwoWeekHigh"),
        "52w_min":                      safe_get(info, "fiftyTwoWeekLow"),
        "media_50d":                    safe_get(info, "fiftyDayAverage"),
        "media_200d":                   safe_get(info, "twoHundredDayAverage"),
        "volume_medio_30d":             safe_get(info, "averageVolume"),
        "short_ratio":                  safe_get(info, "shortRatio"),
        "insider_ownership_pct":        formatar_percentual_forcado(safe_get(info, "heldPercentInsiders")),
        "institutional_ownership_pct":  formatar_percentual_forcado(safe_get(info, "heldPercentInstitutions")),
    }

    # ── 6. HISTÓRICO FINANCEIRO ──────────────────────────────
    historico = _coletar_historico_financeiro(ativo)

    # ── 7. META ──────────────────────────────────────────────
    meta = {
        "data_coleta":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fonte_principal": "Yahoo Finance via yfinance",
    }

    return {
        "identificacao":        identificacao,
        "meta":                 meta,
        "valuation":            valuation,
        "rentabilidade":        rentabilidade,
        "saude_financeira":     saude_financeira,
        "mercado":              mercado,
        "historico_financeiro": historico,
    }


def _calcular_roi(info: dict):
    """ROI estimado = Lucro Líquido / (Ativo Total - Passivo Circulante)"""
    try:
        lucro   = safe_get(info, "netIncomeToCommon")
        ativo   = safe_get(info, "totalAssets")
        passivo = safe_get(info, "totalCurrentLiabilities")
        if lucro and ativo and passivo:
            capital = ativo - passivo
            if capital > 0:
                return round((lucro / capital) * 100, 2)
    except Exception:
        pass
    return None


def _coletar_historico_financeiro(ativo: yf.Ticker) -> dict:
    """Coleta histórico anual e trimestral de receita, lucro bruto, EBITDA e lucro líquido"""
    resultado = {"anual": [], "trimestral": []}

    for modo, df in [("anual", ativo.financials), ("trimestral", ativo.quarterly_financials)]:
        try:
            if df is None or df.empty:
                continue
            for col in df.columns:
                periodo = str(col)[:10]
                linha = {"periodo": periodo}

                def pegar(campo, _df=df, _col=col):
                    try:
                        val = _df.loc[campo, _col]
                        return formatar_moeda_milhoes(float(val)) if val and str(val) != "nan" else None
                    except Exception:
                        return None

                linha["receita_total_mi"]       = pegar("Total Revenue")
                linha["lucro_bruto_mi"]         = pegar("Gross Profit")
                linha["ebitda_mi"]              = pegar("EBITDA")
                linha["lucro_liquido_mi"]       = pegar("Net Income")
                linha["lucro_operacional_mi"]   = pegar("Operating Income")
                linha["pesquisa_desenv_mi"]     = pegar("Research And Development")
                resultado[modo].append(linha)
        except Exception:
            pass

    return resultado


# ─────────────────────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def main():
    # Detecta modo de execução: --ci = GitHub Actions (lê tickers.txt)
    modo_ci = "--ci" in sys.argv

    print("=" * 60)
    print("  ANÁLISE FUNDAMENTALISTA DE AÇÕES — LONGO PRAZO")
    print(f"  Modo: {'GitHub Actions (CI)' if modo_ci else 'Interativo'}")
    print("=" * 60)

    # ── Obtém a lista de tickers ─────────────────────────────
    if modo_ci:
        tickers = ler_tickers_do_arquivo("tickers.txt")
        print(f"\n📋 Tickers lidos de tickers.txt: {', '.join(tickers)}")
    else:
        print("\n  Exemplos: PETR4.SA, VALE3.SA, AAPL, MSFT, WEGE3.SA\n")
        entrada = input("Digite os tickers separados por vírgula: ").strip()
        if not entrada:
            print("⚠  Nenhum ticker informado. Encerrando.")
            sys.exit(0)
        tickers = [t.strip().upper() for t in entrada.split(",") if t.strip()]

    print(f"\n📊 Coletando dados para {len(tickers)} ativo(s)...\n")

    # ── Coleta ───────────────────────────────────────────────
    resultados = {}
    erros      = []

    for ticker in tickers:
        dados = coletar_indicadores(ticker)
        if "erro" in dados:
            print(f"  ✗ {ticker}: {dados['erro']}")
            erros.append({"ticker": ticker, "erro": dados["erro"]})
        else:
            nome = dados["identificacao"].get("nome") or ticker
            print(f"  ✓ {ticker} — {nome}")
            resultados[ticker] = dados

    # ── Monta JSON final ─────────────────────────────────────
    saida = {
        "_metadados": {
            "script":               "Análise Fundamentalista de Ações",
            "versao":               "1.1",
            "data_execucao":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_ativos":         len(tickers),
            "sucesso":              len(resultados),
            "falhas":               len(erros),
            "ativos_solicitados":   tickers,
            "fonte":                "Yahoo Finance via yfinance",
            "nota": (
                "Sufixo _bi = bilhões | _mi = milhões | _pct = percentual já convertido. "
                "None indica dado indisponível na fonte."
            ),
        },
        "acoes":  resultados,
        "erros":  erros,
    }

    # ── Salva JSON ───────────────────────────────────────────
    nome_arquivo = "analise_acoes.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2, default=json_serial)

    print(f"\n✅ JSON salvo: {os.path.abspath(nome_arquivo)}")
    print(f"   Sucesso: {len(resultados)} | Falhas: {len(erros)}")

    # ── Preview no terminal ──────────────────────────────────
    if resultados:
        print("\n📋 PREVIEW DOS PRINCIPAIS INDICADORES:\n")
        cab = f"{'TICKER':<12}{'P/E':>8}{'FWD P/E':>9}{'P/B':>7}{'EPS TTM':>9}{'DY%':>7}{'ROE%':>8}{'MRG LIQ%':>10}{'EV/EBITDA':>11}"
        print(cab)
        print("─" * len(cab))
        for t, d in resultados.items():
            v = d.get("valuation", {})
            r = d.get("rentabilidade", {})
            f = lambda x, c=1: f"{x:.{c}f}" if x is not None else "N/A"
            print(
                f"{t:<12}{f(v.get('pe_ratio_trailing')):>8}{f(v.get('pe_ratio_forward')):>9}"
                f"{f(v.get('pb_ratio')):>7}{f(v.get('eps_ttm'),2):>9}{f(v.get('dividend_yield_ttm_pct')):>7}"
                f"{f(r.get('roe_pct')):>8}{f(r.get('profit_margin_pct')):>10}{f(v.get('ev_ebitda')):>11}"
            )
    print()


if __name__ == "__main__":
    main()
