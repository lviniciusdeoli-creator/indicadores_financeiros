/**
 * ═══════════════════════════════════════════════════════════════
 *  GOOGLE APPS SCRIPT — Leitor de Indicadores de Ações
 *  Acessa o JSON gerado pelo GitHub Actions e retorna
 *  indicadores filtrados para uso no Google Sheets.
 * ═══════════════════════════════════════════════════════════════
 *
 *  CONFIGURAÇÃO INICIAL:
 *  1. Abra o Google Sheets → Extensões → Apps Script
 *  2. Cole este código no editor
 *  3. Altere a constante JSON_URL abaixo com a URL raw do seu repositório
 *  4. Salve (Ctrl+S) e autorize quando solicitado
 *
 *  COMO USAR NAS CÉLULAS DO SHEETS:
 *  =INDICADORES("AAPL"; "pe_ratio_trailing;roe_pct;profit_margin_pct")
 *  =INDICADORES("PETR4.SA"; "preco_atual;dividend_yield_ttm_pct;ev_ebitda")
 *  =INDICADORES("VALE3.SA"; "TODOS")   ← retorna todos os indicadores flat
 *
 * ═══════════════════════════════════════════════════════════════
 *
 *  PARÂMETROS DA FUNÇÃO INDICADORES():
 *  ─────────────────────────────────────────────────────────────
 *  @param {string} ticker
 *      O código do ativo exatamente como está em tickers.txt.
 *      Exemplos: "AAPL", "PETR4.SA", "VALE3.SA", "MSFT"
 *      Case-insensitive (será convertido para maiúsculas automaticamente).
 *
 *  @param {string} indicadores
 *      Um ou mais nomes de indicadores separados por ponto-e-vírgula (;).
 *      Use "TODOS" para retornar todos os indicadores disponíveis.
 *      Os nomes correspondem às chaves do JSON (ver lista abaixo).
 *
 *  INDICADORES DISPONÍVEIS (nomes das chaves no JSON):
 *  ─────────────────────────────────────────────────────────────
 *  [ IDENTIFICAÇÃO ]
 *    nome                    → Nome completo da empresa
 *    setor                   → Setor de atuação
 *    industria               → Indústria específica
 *    pais                    → País de origem
 *    moeda                   → Moeda de negociação
 *
 *  [ VALUATION ]
 *    preco_atual             → Preço atual da ação
 *    pe_ratio_trailing       → P/E histórico (Preço / Lucro dos últimos 12m)
 *    pe_ratio_forward        → P/E estimado (Preço / Lucro projetado)
 *    pb_ratio                → P/B (Preço / Valor Patrimonial por Ação)
 *    ps_ratio                → P/S (Preço / Receita por Ação)
 *    ev_ebitda               → EV/EBITDA (Valor da Empresa / EBITDA)
 *    ev_receita              → EV/Receita
 *    eps_ttm                 → EPS TTM — Lucro por Ação (últimos 12 meses)
 *    eps_forward             → EPS estimado para os próximos 12 meses
 *    dividend_yield_ttm_pct  → Dividend Yield TTM em % (ex: 6.5 = 6,5%)
 *    dividendo_por_acao      → Dividendo anualizado por ação
 *    payout_ratio_pct        → % do lucro distribuído como dividendo
 *    peg_ratio               → PEG Ratio (P/E ÷ crescimento; < 1 = possível subvalorização)
 *
 *  [ RENTABILIDADE ]
 *    gross_margin_pct             → Margem Bruta %
 *    operating_margin_pct         → Margem Operacional %
 *    profit_margin_pct            → Margem de Lucro Líquido %
 *    roe_pct                      → ROE — Retorno sobre Patrimônio Líquido %
 *    roa_pct                      → ROA — Retorno sobre Ativos %
 *    roic_pct                     → ROIC — Retorno sobre Capital Investido % (NOPAT / Capital Investido)
 *    crescimento_receita_yoy_pct  → Crescimento de Receita ano/ano %
 *    crescimento_lucro_yoy_pct    → Crescimento de Lucro ano/ano %
 *    crescimento_eps_qoq_pct      → Crescimento de EPS trimestre/trimestre %
 *
 *  [ SAÚDE FINANCEIRA ]
 *
 *    divida_bruta_bi         → Dívida Bruta total em bilhões (sem descontar caixa)
 *    divida_liquida_bi       → Dívida Líquida em bilhões (dívida total − caixa)
 *    div_liq_sobre_pl        → Dív. Líquida / Patrimônio Líquido
 *    div_liq_sobre_ebitda    → Dív. Líquida / EBITDA (anos de EBITDA para quitar a dívida)
 *    div_liq_sobre_ebit      → Dív. Líquida / EBIT
 *    caixa_total_bi          → Caixa e equivalentes em bilhões
 *    caixa_por_acao          → Caixa por ação
 *    current_ratio           → Liquidez Corrente (Ativo Circ. / Passivo Circ.)
 *    quick_ratio             → Liquidez Imediata (sem estoques)
 *    book_value_por_acao     → Valor Patrimonial por Ação
 *    ebitda_bi               → EBITDA em bilhões
 *    ebit_bi                 → EBIT (Lucro Operacional) em bilhões
 *    free_cash_flow_bi       → Free Cash Flow em bilhões
 *    operating_cash_flow_bi  → Fluxo de Caixa Operacional em bilhões
 *
 *  [ MERCADO ]
 *    market_cap_bi           → Capitalização de Mercado em bilhões
 *    enterprise_value_bi     → Valor da Empresa (EV) em bilhões
 *    beta                    → Beta (volatilidade vs mercado; > 1 = mais volátil)
 *    52w_max                 → Máxima dos últimos 52 semanas
 *    52w_min                 → Mínima dos últimos 52 semanas
 *    media_50d               → Média Móvel de 50 dias
 *    media_200d              → Média Móvel de 200 dias
 *    volume_medio_30d        → Volume médio diário (30 dias)
 *    insider_ownership_pct   → % das ações detidas por insiders
 *    institutional_ownership_pct → % das ações detidas por instituições
 *
 *  EXEMPLOS DE USO NO SHEETS:
 *  ─────────────────────────────────────────────────────────────
 *  =INDICADORES("AAPL"; "preco_atual;pe_ratio_trailing;roe_pct")
 *  =INDICADORES("VALE3.SA"; "dividend_yield_ttm_pct;ev_ebitda;profit_margin_pct")
 *  =INDICADORES("MSFT"; "TODOS")
 * ═══════════════════════════════════════════════════════════════
 */

// ─────────────────────────────────────────────────────────────
//  ⚙️  CONFIGURAÇÃO — altere apenas esta constante
// ─────────────────────────────────────────────────────────────

const JSON_URL =
  "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/analise_acoes.json";
//                                   ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^
//                     Substitua pelo seu usuário e nome do repositório no GitHub


// ─────────────────────────────────────────────────────────────
//  CACHE: evita requisições repetidas ao GitHub na mesma sessão
// ─────────────────────────────────────────────────────────────

/** Tempo de cache em segundos (padrão: 30 minutos) */
const CACHE_TTL_SEGUNDOS = 1800;

/**
 * Busca o JSON do GitHub com cache no CacheService do Apps Script.
 * Na primeira chamada da sessão faz o fetch; nas seguintes usa o cache.
 * @returns {Object} Objeto JavaScript com os dados do JSON
 */
function buscarJsonComCache_() {
  const cache = CacheService.getScriptCache();
  const chave = "analise_acoes_json";

  // Tenta recuperar do cache primeiro
  const cached = cache.get(chave);
  if (cached) {
    return JSON.parse(cached);
  }

  // Faz a requisição HTTP ao GitHub
  const resposta = UrlFetchApp.fetch(JSON_URL, { muteHttpExceptions: true });

  if (resposta.getResponseCode() !== 200) {
    throw new Error(
      `Erro ao buscar JSON (HTTP ${resposta.getResponseCode()}). ` +
      `Verifique a URL em JSON_URL e se o repositório é público.`
    );
  }

  const texto = resposta.getContentText("UTF-8");

  // Armazena no cache por CACHE_TTL_SEGUNDOS
  try {
    cache.put(chave, texto, CACHE_TTL_SEGUNDOS);
  } catch (_) {
    // Cache pode falhar se o JSON for muito grande (> 100 KB); ignora silenciosamente
  }

  return JSON.parse(texto);
}


// ─────────────────────────────────────────────────────────────
//  UTILITÁRIOS
// ─────────────────────────────────────────────────────────────

/**
 * Achata (flattens) os blocos de indicadores de um ativo em um único objeto.
 * Exclui os blocos "identificacao", "meta" e "historico_financeiro".
 * @param {Object} dadosAtivo  Objeto JSON de um ativo específico
 * @returns {Object} Mapa chave→valor de todos os indicadores
 */
function achatarIndicadores_(dadosAtivo) {
  const blocosFlatteados = ["valuation", "rentabilidade", "saude_financeira", "mercado"];
  const resultado = {};

  // Inclui também campos de identificação úteis
  const id = dadosAtivo.identificacao || {};
  ["nome", "setor", "industria", "pais", "moeda", "bolsa", "site"].forEach(function(k) {
    if (id[k] !== undefined) resultado[k] = id[k];
  });

  // Inclui data de coleta
  if (dadosAtivo.meta && dadosAtivo.meta.data_coleta) {
    resultado["data_coleta"] = dadosAtivo.meta.data_coleta;
  }

  // Achata cada bloco de indicadores
  blocosFlatteados.forEach(function(bloco) {
    const obj = dadosAtivo[bloco];
    if (obj && typeof obj === "object") {
      Object.keys(obj).forEach(function(k) {
        resultado[k] = obj[k];
      });
    }
  });

  return resultado;
}


// ─────────────────────────────────────────────────────────────
//  FUNÇÃO PRINCIPAL — usar como fórmula no Google Sheets
// ─────────────────────────────────────────────────────────────

/**
 * Busca indicadores de um ativo a partir do JSON do GitHub Actions.
 *
 * @param {string} ticker       Código do ativo (ex: "AAPL", "PETR4.SA")
 * @param {string} indicadores  Indicadores separados por ; ou "TODOS"
 * @returns {Array}             Tabela 2D: [["Indicador","Valor"], ...]
 * @customfunction
 */
function INDICADORES(ticker, indicadores) {
  // Validações de entrada
  if (!ticker || typeof ticker !== "string") {
    return [["ERRO", "Parâmetro 'ticker' inválido ou ausente."]];
  }
  if (!indicadores || typeof indicadores !== "string") {
    return [["ERRO", "Parâmetro 'indicadores' inválido. Use nomes separados por ; ou 'TODOS'."]];
  }

  const tickerUpper = ticker.toString().trim().toUpperCase();

  try {
    const dados = buscarJsonComCache_();

    // Verifica se o ticker existe no JSON
    if (!dados.acoes || !dados.acoes[tickerUpper]) {
      const disponiveis = dados.acoes ? Object.keys(dados.acoes).join(", ") : "nenhum";
      return [
        ["ERRO", `Ticker '${tickerUpper}' não encontrado no JSON.`],
        ["Disponíveis", disponiveis],
        ["Última atualização", dados._metadados ? dados._metadados.data_execucao : "desconhecida"]
      ];
    }

    const dadosAtivo    = dados.acoes[tickerUpper];
    const indicadoresFlat = achatarIndicadores_(dadosAtivo);

    // Modo TODOS: retorna todos os indicadores disponíveis
    if (indicadores.toString().trim().toUpperCase() === "TODOS") {
      const linhas = [["Indicador", "Valor"]]; // cabeçalho
      Object.keys(indicadoresFlat).forEach(function(k) {
        const val = indicadoresFlat[k];
        linhas.push([k, val !== null && val !== undefined ? val : "N/D"]);
      });
      return linhas;
    }

    // Modo seletivo: filtra apenas os indicadores solicitados
    const chavesSolicitadas = indicadores
      .toString()
      .split(";")
      .map(function(s) { return s.trim().toLowerCase(); })
      .filter(function(s) { return s.length > 0; });

    const linhas = [["Indicador", "Valor"]]; // cabeçalho

    chavesSolicitadas.forEach(function(chave) {
      // Busca case-insensitive
      const chaveReal = Object.keys(indicadoresFlat).find(
        function(k) { return k.toLowerCase() === chave; }
      );

      if (chaveReal !== undefined) {
        const val = indicadoresFlat[chaveReal];
        linhas.push([chaveReal, val !== null && val !== undefined ? val : "N/D"]);
      } else {
        linhas.push([chave, "❌ indicador não encontrado"]);
      }
    });

    return linhas;

  } catch (e) {
    return [
      ["ERRO", e.message],
      ["Dica", "Verifique se JSON_URL está correto e o repositório é público."]
    ];
  }
}


// ─────────────────────────────────────────────────────────────
//  FUNÇÕES AUXILIARES (uso programático ou em menus)
// ─────────────────────────────────────────────────────────────

/**
 * Retorna os dados brutos de um ativo (incluindo histórico financeiro).
 * Útil para uso em scripts que processam os dados programaticamente.
 * @param {string} ticker  Código do ativo
 * @returns {Object}       Objeto JSON completo do ativo
 */
function getDadosCompletos(ticker) {
  const dados = buscarJsonComCache_();
  const tickerUpper = ticker.toString().trim().toUpperCase();
  if (!dados.acoes || !dados.acoes[tickerUpper]) {
    throw new Error(`Ticker '${tickerUpper}' não encontrado.`);
  }
  return dados.acoes[tickerUpper];
}

/**
 * Retorna o histórico financeiro anual de um ativo como tabela 2D.
 * Uso: =HISTORICO_ANUAL("AAPL")
 * @param {string} ticker  Código do ativo
 * @returns {Array}        Tabela 2D com receita, lucro, etc. por ano
 * @customfunction
 */
function HISTORICO_ANUAL(ticker) {
  try {
    const ativo = getDadosCompletos(ticker);
    const hist  = ativo.historico_financeiro && ativo.historico_financeiro.anual;

    if (!hist || hist.length === 0) {
      return [["AVISO", "Histórico anual não disponível para " + ticker]];
    }

    // Monta cabeçalho dinâmico a partir das chaves do primeiro registro
    const campos  = Object.keys(hist[0]);
    const tabela  = [campos]; // primeira linha = cabeçalho

    hist.forEach(function(linha) {
      tabela.push(campos.map(function(c) {
        const v = linha[c];
        return v !== null && v !== undefined ? v : "N/D";
      }));
    });

    return tabela;
  } catch (e) {
    return [["ERRO", e.message]];
  }
}

/**
 * Retorna a data da última atualização do JSON.
 * Uso: =ULTIMA_ATUALIZACAO()
 * @returns {string}  Data e hora da última execução do script
 * @customfunction
 */
function ULTIMA_ATUALIZACAO() {
  try {
    const dados = buscarJsonComCache_();
    return dados._metadados ? dados._metadados.data_execucao : "desconhecida";
  } catch (e) {
    return "ERRO: " + e.message;
  }
}

/**
 * Lista todos os tickers disponíveis no JSON.
 * Uso: =LISTAR_TICKERS()
 * @returns {Array}  Lista vertical de tickers
 * @customfunction
 */
function LISTAR_TICKERS() {
  try {
    const dados = buscarJsonComCache_();
    if (!dados.acoes) return [["Nenhum ticker disponível"]];
    return Object.keys(dados.acoes).map(function(t) { return [t]; });
  } catch (e) {
    return [["ERRO", e.message]];
  }
}

/**
 * Invalida o cache manualmente.
 * Execute pela aba "Executar" do editor quando quiser forçar uma
 * nova busca sem esperar o TTL expirar.
 */
function limparCache() {
  CacheService.getScriptCache().remove("analise_acoes_json");
  Logger.log("✅ Cache limpo com sucesso.");
}
