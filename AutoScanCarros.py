"""
AutoScan - consulta de carros com interface gráfica (tkinter).
Banco de modelos e cores + classe `carro` + janela de consulta, tudo neste arquivo.

Uso:
    projetocarros - AutoScan.py
"""

import difflib
import re
import unicodedata


# ----------------------------------------------------------------------------
# Utilitários
# ----------------------------------------------------------------------------
def normalizar(texto: str) -> str:
    """minúsculas, sem acentos, sem pontuação, espaços únicos."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return texto.strip()


# ----------------------------------------------------------------------------
# Banco de modelos
# ----------------------------------------------------------------------------
MODELOS = {}


def _m(nome, marca, categoria, bom, ruim, aliases=()):
    MODELOS[nome] = {
        "nome": nome,
        "marca": marca,
        "categoria": categoria,
        "bom_em": list(bom),
        "ruim_em": list(ruim),
        "aliases": [normalizar(nome)] + [normalizar(a) for a in aliases],
    }


# --- Hatches compactos ---
_m("Volkswagen Gol", "Volkswagen", "hatch compacto",
   ["manutenção barata", "peças fáceis de achar", "bom valor de revenda"],
   ["segurança fraca", "acabamento simples", "pouco espaço interno"], ["gol", "vw gol"])
_m("Volkswagen Polo", "Volkswagen", "hatch compacto",
   ["estabilidade", "acabamento", "motor turbo ágil"],
   ["porta-malas pequeno", "revisões mais caras"], ["polo", "vw polo"])
_m("Volkswagen Up!", "Volkswagen", "hatch compacto",
   ["tamanho ideal pra cidade", "econômico", "fácil de estacionar"],
   ["espaço traseiro apertado", "desempenho em estrada"], ["up", "vw up"])
_m("Fiat Mobi", "Fiat", "hatch compacto",
   ["preço baixo", "consumo baixo", "ótimo na cidade"],
   ["isolamento acústico", "segurança básica", "desempenho em estrada"], ["mobi"])
_m("Fiat Argo", "Fiat", "hatch compacto",
   ["bom custo-benefício", "central multimídia", "visual moderno"],
   ["suspensão firme", "porta-malas mediano"], ["argo"])
_m("Fiat Uno", "Fiat", "hatch compacto",
   ["muito barato", "manutenção simples", "econômico"],
   ["conforto", "segurança", "ruído interno"], ["uno"])
_m("Fiat Palio", "Fiat", "hatch compacto",
   ["peças baratas", "mecânica conhecida", "bom espaço interno"],
   ["acabamento", "segurança"], ["palio"])
_m("Chevrolet Onix", "Chevrolet", "hatch compacto",
   ["líder de vendas", "boa revenda", "bom pacote de equipamentos"],
   ["espaço traseiro", "ruído do motor"], ["onix"])
_m("Chevrolet Celta", "Chevrolet", "hatch compacto",
   ["muito econômico", "manutenção baratíssima", "mecânica simples"],
   ["segurança", "conforto", "desempenho"], ["celta"])
_m("Chevrolet Prisma", "Chevrolet", "sedã compacto",
   ["porta-malas grande", "boa revenda", "econômico"],
   ["acabamento simples", "ruído interno"], ["prisma"])
_m("Hyundai HB20", "Hyundai", "hatch compacto",
   ["bom custo-benefício", "garantia longa", "design"],
   ["revisões um pouco caras", "suspensão dura"], ["hb20", "hb 20"])
_m("Renault Kwid", "Renault", "hatch compacto",
   ["preço baixo", "muito econômico", "altura do solo elevada"],
   ["potência baixa", "acabamento simples", "estabilidade"], ["kwid"])
_m("Renault Sandero", "Renault", "hatch compacto",
   ["espaço interno", "conforto", "bom custo-benefício"],
   ["revenda mais fraca", "eletrônica"], ["sandero"])
_m("Toyota Yaris", "Toyota", "hatch compacto",
   ["confiabilidade", "revenda", "baixo custo de manutenção"],
   ["preço alto pro porte", "pouca potência"], ["yaris"])
_m("Peugeot 208", "Peugeot", "hatch compacto",
   ["design", "painel digital", "dirigibilidade"],
   ["revenda", "rede de peças"], ["208", "peugeot208"])
_m("Honda Fit", "Honda", "hatch compacto",
   ["espaço interno incrível", "banco versátil", "durabilidade"],
   ["rumor de rodagem", "preço do usado"], ["fit", "honda fit"])
_m("Ford Ka", "Ford", "hatch compacto",
   ["dirigibilidade", "consumo baixo", "preço acessível"],
   ["revenda", "peças após saída da Ford do Brasil"], ["ka", "ford ka"])
_m("Ford Fiesta", "Ford", "hatch compacto",
   ["comportamento dinâmico", "acabamento", "conforto"],
   ["revenda", "câmbio automatizado antigo"], ["fiesta"])

# --- Sedãs ---
_m("Toyota Corolla", "Toyota", "sedã médio",
   ["confiabilidade", "revenda excelente", "conforto"],
   ["preço alto", "revisões mais caras"], ["corolla", "corola"])
_m("Honda Civic", "Honda", "sedã médio",
   ["dirigibilidade", "motor", "acabamento"],
   ["custo de manutenção", "preço alto"], ["civic", "civic honda"])
_m("Honda City", "Honda", "sedã compacto",
   ["espaço", "consumo", "confiabilidade"],
   ["design discreto", "preço"], ["city"])
_m("Volkswagen Virtus", "Volkswagen", "sedã compacto",
   ["porta-malas enorme", "estabilidade", "motor turbo"],
   ["revisões caras", "preço"], ["virtus"])
_m("Volkswagen Jetta", "Volkswagen", "sedã médio",
   ["conforto", "acabamento", "estabilidade"],
   ["manutenção cara", "depreciação"], ["jetta"])
_m("Chevrolet Cruze", "Chevrolet", "sedã médio",
   ["espaço", "conforto em estrada", "motor turbo"],
   ["manutenção cara", "eletrônica"], ["cruze"])
_m("Nissan Versa", "Nissan", "sedã compacto",
   ["espaço traseiro", "porta-malas", "conforto"],
   ["acabamento", "revenda"], ["versa"])
_m("Hyundai HB20S", "Hyundai", "sedã compacto",
   ["custo-benefício", "equipamentos", "garantia"],
   ["suspensão firme", "revenda mediana"], ["hb20s", "hb20 s"])
_m("Fiat Cronos", "Fiat", "sedã compacto",
   ["porta-malas gigante", "espaço", "bom preço"],
   ["acabamento", "revenda"], ["cronos"])
_m("Toyota Camry", "Toyota", "sedã grande",
   ["conforto", "suavidade", "confiabilidade"],
   ["preço", "consumo"], ["camry"])

# --- SUVs ---
_m("Jeep Renegade", "Jeep", "SUV compacto",
   ["visual marcante", "capacidade off-road", "robustez"],
   ["consumo alto", "manutenção cara"], ["renegade"])
_m("Jeep Compass", "Jeep", "SUV médio",
   ["conforto", "espaço", "presença"],
   ["manutenção cara", "problemas eletrônicos"], ["compass"])
_m("Honda HR-V", "Honda", "SUV compacto",
   ["espaço", "conforto", "revenda"],
   ["preço alto", "ruído do motor"], ["hrv", "hr v", "hr-v"])
_m("Toyota Corolla Cross", "Toyota", "SUV médio",
   ["confiabilidade", "versão híbrida econômica", "revenda"],
   ["preço alto"], ["corolla cross", "cross"])
_m("Hyundai Creta", "Hyundai", "SUV compacto",
   ["conforto", "equipamentos", "bom espaço"],
   ["consumo urbano", "preço"], ["creta"])
_m("Volkswagen T-Cross", "Volkswagen", "SUV compacto",
   ["porta-malas", "estabilidade", "acabamento"],
   ["preço", "revisões caras"], ["tcross", "t cross", "t-cross"])
_m("Chevrolet Tracker", "Chevrolet", "SUV compacto",
   ["tecnologia", "conectividade", "conforto"],
   ["porta-malas", "revenda ainda em formação"], ["tracker"])
_m("Nissan Kicks", "Nissan", "SUV compacto",
   ["conforto", "consumo", "espaço"],
   ["motor pouco potente", "revenda"], ["kicks"])
_m("Fiat Pulse", "Fiat", "SUV compacto",
   ["custo-benefício", "motor turbo", "design"],
   ["acabamento simples", "revenda"], ["pulse"])
_m("Ford EcoSport", "Ford", "SUV compacto",
   ["altura do solo", "versatilidade", "boa posição de dirigir"],
   ["acabamento", "ruído", "peças após saída da Ford do Brasil"], ["ecosport", "eco sport"])
_m("Mitsubishi Pajero", "Mitsubishi", "SUV grande",
   ["off-road excelente", "robustez", "durabilidade"],
   ["consumo muito alto", "tamanho na cidade"], ["pajero"])
_m("Toyota SW4", "Toyota", "SUV grande",
   ["robustez", "revenda", "espaço pra 7 pessoas"],
   ["preço muito alto", "consumo alto"], ["sw4", "sw 4", "hilux sw4"])
_m("Jeep Wrangler", "Jeep", "SUV off-road",
   ["off-road lendário", "personalidade", "capota removível"],
   ["conforto no asfalto", "consumo", "preço"], ["wrangler"])

# --- Picapes ---
_m("Toyota Hilux", "Toyota", "picape grande",
   ["durabilidade", "revenda", "capacidade de carga"],
   ["preço alto", "consumo", "tamanho na cidade"], ["hilux"])
_m("Fiat Strada", "Fiat", "picape compacta",
   ["líder de vendas", "econômica", "boa caçamba"],
   ["conforto traseiro", "segurança básica"], ["strada"])
_m("Fiat Toro", "Fiat", "picape média",
   ["conforto de SUV", "boa dirigibilidade", "bom espaço"],
   ["manutenção cara", "consumo do diesel"], ["toro"])
_m("Chevrolet S10", "Chevrolet", "picape grande",
   ["robustez", "boa carga", "motor diesel forte"],
   ["consumo", "ruído"], ["s10", "s 10"])
_m("Ford Ranger", "Ford", "picape grande",
   ["força", "conforto", "tecnologia"],
   ["preço", "manutenção"], ["ranger"])
_m("Volkswagen Saveiro", "Volkswagen", "picape compacta",
   ["econômica", "boa pra trabalho", "manutenção barata"],
   ["conforto", "segurança"], ["saveiro"])

# --- Elétricos / híbridos / outros ---
_m("BYD Dolphin", "BYD", "elétrico compacto",
   ["custo por km baixíssimo", "silêncio", "aceleração"],
   ["rede de recarga", "revenda incerta"], ["dolphin"])
_m("BYD Seal", "BYD", "elétrico sedã",
   ["desempenho", "autonomia", "tecnologia"],
   ["preço alto", "rede de assistência"], ["seal"])
_m("Tesla Model 3", "Tesla", "elétrico sedã",
   ["tecnologia", "autonomia", "desempenho"],
   ["assistência no Brasil", "preço", "acabamento"], ["model 3", "tesla"])
_m("Toyota Prius", "Toyota", "híbrido",
   ["consumo baixíssimo", "confiabilidade", "silêncio"],
   ["design polêmico", "preço"], ["prius"])
_m("Mini Cooper", "Mini", "hatch premium",
   ["dirigibilidade divertida", "design icônico", "personalidade"],
   ["manutenção cara", "espaço interno"], ["mini cooper", "mini", "cooper"])
_m("Chevrolet Camaro", "Chevrolet", "esportivo",
   ["potência", "som do motor", "visual"],
   ["consumo", "visibilidade", "preço"], ["camaro"])
_m("Ford Mustang", "Ford", "esportivo",
   ["potência", "visual", "som"],
   ["consumo", "peças e assistência", "preço"], ["mustang"])
_m("Volkswagen Fusca", "Volkswagen", "clássico",
   ["icônico", "mecânica simples", "valorização"],
   ["segurança", "conforto", "desempenho"], ["fusca", "vw fusca"])
_m("Chevrolet Opala", "Chevrolet", "clássico",
   ["estilo", "motor 6 cilindros", "nostalgia"],
   ["consumo", "segurança", "restauro caro"], ["opala"])


# ----------------------------------------------------------------------------
# Banco de cores
# ----------------------------------------------------------------------------
CORES = {}


def _c(nome, bom, ruim, aliases=()):
    CORES[nome] = {
        "nome": nome,
        "bom_em": list(bom),
        "ruim_em": list(ruim),
        "aliases": [normalizar(nome)] + [normalizar(a) for a in aliases],
    }


_c("Branco", ["revenda fácil", "esquenta menos no sol", "boa visibilidade à noite", "poucos riscos aparentes"],
   ["suja de lama e poeira facilmente", "pode parecer 'carro de frota'"], ["branca", "branco geleira", "branco perola"])
_c("Preto", ["elegância", "visual sofisticado", "boa revenda"],
   ["esquenta muito no sol", "mostra poeira, riscos e marcas de água", "pior visibilidade à noite"], ["preta"])
_c("Prata", ["esconde sujeira", "boa revenda", "esquenta pouco", "riscos pouco visíveis"],
   ["cor comum", "visual conservador"], ["prateado", "prateada", "cinza claro"])
_c("Cinza", ["esconde sujeira", "visual moderno", "boa revenda"],
   ["pouco vibrante", "esquenta um pouco mais que o branco"], ["cinza", "grafite", "chumbo", "cinza escuro", "cinza grafite", "cinza cromo"])
_c("Vermelho", ["chama atenção", "visual esportivo", "fácil de achar no estacionamento"],
   ["desbota mais com o tempo", "revenda mais lenta", "atrai mais a atenção de fiscais e ladrões"], ["vermelha", "rubi"])
_c("Azul", ["bonito", "boa visibilidade", "esconde bem a sujeira (tons escuros)"],
   ["revenda média", "tons escuros esquentam"], ["azul", "azul marinho", "azul escuro", "azul claro", "azulado"])
_c("Verde", ["diferente da maioria", "bonito em tons escuros", "bom em ambiente natural"],
   ["revenda mais difícil", "gosto específico"], ["verde escuro", "verde claro", "verde militar", "verde musgo"])
_c("Amarelo", ["máxima visibilidade", "alegre", "mais seguro no trânsito"],
   ["revenda difícil", "gosto específico"], ["amarela"])
_c("Laranja", ["muito chamativo", "visibilidade alta", "personalidade"],
   ["revenda difícil", "pouco comum"], [])
_c("Marrom", ["esconde sujeira de terra", "tom sóbrio", "diferente"],
   ["revenda lenta", "visual datado"], ["marrom escuro", "bronze", "café"])
_c("Bege", ["esconde sujeira", "esquenta pouco", "discreto"],
   ["revenda lenta", "visual datado"], ["champagne", "areia", "dourado claro"])
_c("Dourado", ["diferente", "esconde sujeira", "discreto"],
   ["gosto específico", "revenda lenta"], ["dourada", "ouro"])
_c("Vinho", ["elegante", "discreto", "esconde sujeira"],
   ["pouco comum", "revenda média"], ["bordo", "bordô", "vinho escuro"])
_c("Rosa", ["muito diferente", "personalidade", "fácil de achar no estacionamento"],
   ["revenda muito difícil", "gosto bem específico"], ["rosa claro", "rosa pink", "pink"])


# ----------------------------------------------------------------------------
# Busca
# ----------------------------------------------------------------------------
def _busca(texto, banco, corte=0.78):
    """
    Procura o melhor item de `banco` dentro de `texto`.
    Retorna (item | None, pontuação 0-1, como_achou).
    """
    t = normalizar(texto)
    if not t:
        return None, 0.0, "vazio"

    palavras = t.split()
    # janelas de 1 a 3 palavras, para casar "hr v", "corolla cross" etc.
    janelas = set()
    for tam in (1, 2, 3):
        for i in range(len(palavras) - tam + 1):
            janelas.add(" ".join(palavras[i:i + tam]))

    # 1) Correspondência exata de alias como palavra inteira (prefere o alias mais longo)
    melhor, melhor_len = None, 0
    for item in banco.values():
        for alias in item["aliases"]:
            if re.search(rf"\b{re.escape(alias)}\b", t) and len(alias) > melhor_len:
                melhor, melhor_len = item, len(alias)
    if melhor:
        return melhor, 1.0, "exata"

    # 2) Correspondência aproximada (erros de digitação)
    melhor, melhor_score = None, 0.0
    for item in banco.values():
        for alias in item["aliases"]:
            if len(alias) < 4:      # aliases curtos (ka, up, gol) dão falsos positivos
                continue
            for janela in janelas:
                if abs(len(janela) - len(alias)) > 2:
                    continue
                s = difflib.SequenceMatcher(None, janela, alias).ratio()
                if s > melhor_score:
                    melhor, melhor_score = item, s
    if melhor and melhor_score >= corte:
        return melhor, melhor_score, "aproximada"

    return None, melhor_score, "não encontrado"


def buscar_modelo(texto):
    return _busca(texto, MODELOS)


def buscar_cor(texto):
    return _busca(texto, CORES)


def sugestoes_modelo(texto, n=3):
    """Quando não acha, devolve os nomes mais parecidos."""
    t = normalizar(texto)
    todos = {a: item["nome"] for item in MODELOS.values() for a in item["aliases"]}
    achados = difflib.get_close_matches(t, list(todos), n=n, cutoff=0.5)
    return list(dict.fromkeys(todos[a] for a in achados))


# ----------------------------------------------------------------------------
# Análise combinada
# ----------------------------------------------------------------------------
def analisar_resposta(texto):
    """Analisa uma frase livre e devolve modelo e cor encontrados (ou None)."""
    modelo, s_m, como_m = buscar_modelo(texto)
    cor, s_c, como_c = buscar_cor(texto)
    return {
        "modelo": modelo, "confianca_modelo": round(s_m, 2), "tipo_modelo": como_m,
        "cor": cor, "confianca_cor": round(s_c, 2), "tipo_cor": como_c,
    }


def _formatar(item):
    """Monta o texto de um item do banco (modelo ou cor)."""
    bom = ", ".join(item["bom_em"])
    ruim = ", ".join(item["ruim_em"])
    extra = f" ({item['marca']} - {item['categoria']})" if "marca" in item else ""
    return f"{item['nome']}{extra}\n   Bom em:  {bom}\n   Ruim em: {ruim}"


# ----------------------------------------------------------------------------
# Integração com a classe `carro` (marca, modelo, cor)
# ----------------------------------------------------------------------------
_MARCAS_APELIDOS = {"vw": "volkswagen", "volks": "volkswagen", "gm": "chevrolet", "chevy": "chevrolet"}


def _marca_confere(digitada, marca_bd):
    d = normalizar(digitada)
    if not d:
        return True                      # marca em branco: não valida
    d = _MARCAS_APELIDOS.get(d, d)
    m = normalizar(marca_bd)
    if d == m or (len(d) >= 3 and (d in m or m in d)):
        return True
    return difflib.SequenceMatcher(None, d, m).ratio() >= 0.75


def _achar_modelo(obj):
    """Recebe um objeto com .marca e .modelo e devolve o item do banco (ou None)."""
    marca = getattr(obj, "marca", "")
    modelo = getattr(obj, "modelo", "")
    for texto in (f"{marca} {modelo}", str(modelo)):
        item, _, _ = buscar_modelo(texto)
        if item and _marca_confere(marca, item["marca"]):
            return item
    return None


class CarroBD(dict):
    """
    Item do banco que sabe se comparar com um objeto `carro`:
        resposta.carro == resposta   ->  True se o carro digitado existe no banco.
    """

    def __eq__(self, outro):
        if isinstance(outro, dict):
            return dict.__eq__(self, outro)
        if hasattr(outro, "modelo"):
            item = _achar_modelo(outro)
            return item is not None and item["nome"] == self["nome"]
        return NotImplemented

    def __ne__(self, outro):
        igual = self.__eq__(outro)
        return igual if igual is NotImplemented else not igual

    __hash__ = None


def _carro_do_banco(self):
    item = _achar_modelo(self)
    return CarroBD(item) if item else None


def integrar(classe):
    """Adiciona o atributo `.carro` (item correspondente no banco) à sua classe."""
    classe.carro = property(_carro_do_banco)
    return classe


def descrever(obj):
    """
    Imprime o que o carro tem de bom/ruim e o que a cor tem de bom/ruim.
    Aceita um objeto `carro` (marca, modelo, cor) ou um item do banco (dict).
    """
    if isinstance(obj, dict):
        print(_formatar(obj))
        return

    modelo = _achar_modelo(obj)
    if modelo is None:
        sug = sugestoes_modelo(getattr(obj, "modelo", ""))
        print("Não encontrei esse carro no banco."
              + (f" Você quis dizer: {', '.join(sug)}?" if sug else ""))
        return

    print("\n" + _formatar(modelo))

    cor, _, _ = buscar_cor(getattr(obj, "cor", ""))
    if cor is None:
        print(f"\nNão reconheci a cor '{getattr(obj, 'cor', '')}'.")
        return
    print("\n" + _formatar(cor))

    print(f"\nResumo: seu {modelo['nome']} {cor['nome'].lower()}")
    print("  Pontos fortes: " + "; ".join(modelo["bom_em"][:2] + cor["bom_em"][:2]))
    print("  Pontos fracos: " + "; ".join(modelo["ruim_em"][:2] + cor["ruim_em"][:2]))


# ============================================================================
# MINHA CLASSE
# ============================================================================
class carro:
    def __init__(self, marca, modelo, cor):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor 

integrar(carro)   # liga a classe ao banco: cria o atributo resposta.carro


# ============================================================================
# INTERFACE GRÁFICA (tkinter)
# ============================================================================
import tkinter as tk

# Paleta: fundo azul-grafite, destaque ciano discreto
FUNDO = "#0b0f14"
PAINEL = "#121821"
BORDA = "#1f2a37"
TEXTO = "#c9d4e0"
MUTED = "#6b7a8c"
DESTAQUE = "#38bdf8"
BOTAO = "#0c4a6e"
BOTAO_HOVER = "#0369a1"
BOM = "#4ade80"
RUIM = "#f87171"
ALERTA = "#fbbf24"

FONTE = ("Segoe UI", 10)
FONTE_B = ("Segoe UI", 10, "bold")
FONTE_TITULO = ("Segoe UI", 13, "bold")
MONO = ("Consolas", 9)
MONO_B = ("Consolas", 9, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoScan · Consulta de Carros")
        self.configure(bg=FUNDO)
        self.geometry("980x660")
        self.minsize(860, 600)

        self._cabecalho()

        corpo = tk.Frame(self, bg=FUNDO)
        corpo.pack(fill="both", expand=True, padx=18, pady=(14, 18))
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        self._painel_entrada(corpo)
        self._painel_resultados(corpo)

        self.bind("<Escape>", self.limpar)
        self.ent_marca.focus_set()
        self._resetar_resultados()

    # ------------------------------------------------------------------ layout
    def _cabecalho(self):
        topo = tk.Frame(self, bg=FUNDO)
        topo.pack(fill="x", padx=18, pady=(16, 0))
        tk.Label(topo, text="AUTO", font=("Consolas", 16, "bold"), fg=TEXTO, bg=FUNDO).pack(side="left")
        tk.Label(topo, text="SCAN", font=("Consolas", 16, "bold"), fg=DESTAQUE, bg=FUNDO).pack(side="left")
        tk.Label(topo, text="   consulta de veículos · modelo × cor", font=MONO, fg=MUTED,
                 bg=FUNDO).pack(side="left", pady=(6, 0))
        tk.Frame(self, bg=DESTAQUE, height=1).pack(fill="x", padx=18, pady=(10, 0))

    def _caixa(self, pai, **grid):
        f = tk.Frame(pai, bg=PAINEL, highlightbackground=BORDA, highlightthickness=1)
        f.grid(**grid)
        return f

    def _painel_entrada(self, pai):
        caixa = self._caixa(pai, row=0, column=0, sticky="ns", padx=(0, 14))
        caixa.configure(width=290)

        interno = tk.Frame(caixa, bg=PAINEL)
        interno.pack(fill="both", expand=True, padx=16, pady=14)

        tk.Label(interno, text="// ENTRADA", font=MONO_B, fg=DESTAQUE, bg=PAINEL).pack(anchor="w")
        tk.Label(interno, text="preencha e pressione Enter", font=MONO, fg=MUTED,
                 bg=PAINEL).pack(anchor="w", pady=(0, 12))

        self.ent_marca = self._campo(interno, "MARCA", "ex: Toyota, VW, Honda")
        self.ent_modelo = self._campo(interno, "MODELO", "ex: Corolla, Gol, HR-V")
        self.ent_cor = self._campo(interno, "COR", "ex: prata, preto, azul marinho")

        for e in (self.ent_marca, self.ent_modelo, self.ent_cor):
            e.bind("<Return>", self.consultar)

        self.btn_consultar = self._botao(interno, "CONSULTAR", self.consultar, BOTAO, BOTAO_HOVER, TEXTO)
        self.btn_consultar.pack(fill="x", pady=(18, 6))
        self._botao(interno, "LIMPAR", self.limpar, PAINEL, BORDA, MUTED, borda=True).pack(fill="x")

        tk.Frame(interno, bg=BORDA, height=1).pack(fill="x", pady=16)

        self.lbl_status = tk.Label(interno, text="● aguardando consulta", font=MONO, fg=MUTED,
                                   bg=PAINEL, anchor="w", justify="left", wraplength=250)
        self.lbl_status.pack(fill="x")

    def _campo(self, pai, rotulo, dica):
        tk.Label(pai, text=rotulo, font=MONO_B, fg=MUTED, bg=PAINEL).pack(anchor="w", pady=(6, 3))
        e = tk.Entry(pai, font=FONTE, bg=FUNDO, fg=TEXTO, insertbackground=DESTAQUE,
                     relief="flat", highlightthickness=1, highlightbackground=BORDA,
                     highlightcolor=DESTAQUE, selectbackground=BOTAO, selectforeground=TEXTO)
        e.pack(fill="x", ipady=6)
        tk.Label(pai, text=dica, font=("Consolas", 8), fg="#465465", bg=PAINEL).pack(anchor="w", pady=(2, 0))
        return e

    def _botao(self, pai, texto, comando, bg, hover, fg, borda=False):
        b = tk.Button(pai, text=texto, command=comando, font=MONO_B, bg=bg, fg=fg,
                      activebackground=hover, activeforeground=TEXTO, relief="flat",
                      cursor="hand2", pady=8, bd=0,
                      highlightthickness=1 if borda else 0, highlightbackground=BORDA)
        b.bind("<Enter>", lambda _: b.configure(bg=hover))
        b.bind("<Leave>", lambda _: b.configure(bg=bg))
        return b

    def _painel_resultados(self, pai):
        col = tk.Frame(pai, bg=FUNDO)
        col.grid(row=0, column=1, sticky="nsew")
        col.columnconfigure(0, weight=1)
        col.rowconfigure(0, weight=5)
        col.rowconfigure(1, weight=4)
        col.rowconfigure(2, weight=4)

        self.txt_modelo = self._area(col, "// MODELO", 0)
        self.txt_cor = self._area(col, "// COR", 1)
        self.txt_resumo = self._area(col, "// RESUMO", 2)

    def _area(self, pai, titulo, linha):
        caixa = tk.Frame(pai, bg=PAINEL, highlightbackground=BORDA, highlightthickness=1)
        caixa.grid(row=linha, column=0, sticky="nsew", pady=(0, 10) if linha < 2 else 0)
        tk.Label(caixa, text=titulo, font=MONO_B, fg=DESTAQUE, bg=PAINEL).pack(anchor="w", padx=14, pady=(10, 0))

        t = tk.Text(caixa, font=FONTE, bg=PAINEL, fg=TEXTO, relief="flat", wrap="word",
                    height=4, padx=14, pady=6, cursor="arrow", bd=0, highlightthickness=0,
                    spacing1=2, spacing3=2)
        t.pack(fill="both", expand=True)
        t.tag_configure("titulo", font=FONTE_TITULO, foreground=TEXTO)
        t.tag_configure("sub", font=MONO, foreground=MUTED)
        t.tag_configure("rotulo", font=MONO_B, foreground=MUTED)
        t.tag_configure("bom", foreground=BOM)
        t.tag_configure("ruim", foreground=RUIM)
        t.tag_configure("alerta", foreground=ALERTA)
        t.tag_configure("muted", foreground=MUTED)
        t.configure(state="disabled")
        return t

    # ------------------------------------------------------------------ helpers
    def _escrever(self, widget, partes):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        for texto, tag in partes:
            widget.insert("end", texto, tag)
        widget.configure(state="disabled")

    def _status(self, texto, cor):
        self.lbl_status.configure(text="● " + texto, fg=cor)

    def _resetar_resultados(self):
        for w in (self.txt_modelo, self.txt_cor, self.txt_resumo):
            self._escrever(w, [("aguardando consulta...", "muted")])
        self._status("aguardando consulta", MUTED)

    @staticmethod
    def _lista(titulo, itens, tag, simbolo):
        partes = [(titulo + "\n", "rotulo")]
        partes += [(f"  {simbolo} {i}\n", tag) for i in itens]
        return partes

    # ------------------------------------------------------------------ ações
    def limpar(self, _=None):
        for e in (self.ent_marca, self.ent_modelo, self.ent_cor):
            e.delete(0, "end")
        self._resetar_resultados()
        self.ent_marca.focus_set()

    def consultar(self, _=None):
        # usa a SUA classe e o atributo .carro criado por integrar()
        resposta = carro(self.ent_marca.get().strip(),
                         self.ent_modelo.get().strip(),
                         self.ent_cor.get().strip())

        if not resposta.modelo:
            self._resetar_resultados()
            self._status("informe ao menos o modelo", ALERTA)
            return

        # ---- modelo
        if resposta.carro == resposta:
            m = resposta.carro
            self._escrever(self.txt_modelo,
                           [(m["nome"] + "\n", "titulo"),
                            (f"{m['marca']} · {m['categoria']}\n\n", "sub")]
                           + self._lista("BOM EM", m["bom_em"], "bom", "+")
                           + [("\n", None)]
                           + self._lista("RUIM EM", m["ruim_em"], "ruim", "−"))
        else:
            sug = sugestoes_modelo(resposta.modelo)
            partes = [(f"Nenhum carro encontrado para “{resposta.marca} {resposta.modelo}”.\n".replace("  ", " "), "alerta")]
            partes.append(("Verifique se a marca combina com o modelo.\n", "muted"))
            if sug:
                partes.append(("\nVocê quis dizer: " + ", ".join(sug) + "?", "sub"))
            self._escrever(self.txt_modelo, partes)
            self._escrever(self.txt_cor, [("—", "muted")])
            self._escrever(self.txt_resumo, [("—", "muted")])
            self._status("carro não encontrado", RUIM)
            return

        # ---- cor
        c, _, _ = buscar_cor(resposta.cor)
        if c is None:
            msg = "Cor não informada." if not resposta.cor else f"Não reconheci a cor “{resposta.cor}”."
            self._escrever(self.txt_cor, [(msg + "\n", "alerta"),
                                          ("Tente: branco, preto, prata, cinza, azul, vermelho...", "muted")])
            self._escrever(self.txt_resumo, [(f"Seu {m['nome']}\n", "titulo"),
                                             ("Sem a cor, o resumo considera só o modelo.", "muted")])
            self._status("modelo encontrado · cor não reconhecida", ALERTA)
            return

        self._escrever(self.txt_cor,
                       [(c["nome"] + "\n\n", "titulo")]
                       + self._lista("BOM EM", c["bom_em"], "bom", "+")
                       + [("\n", None)]
                       + self._lista("RUIM EM", c["ruim_em"], "ruim", "−"))

        # ---- resumo
        fortes = m["bom_em"][:2] + c["bom_em"][:2]
        fracos = m["ruim_em"][:2] + c["ruim_em"][:2]
        self._escrever(self.txt_resumo,
                       [(f"Seu {m['nome']} {c['nome'].lower()}\n\n", "titulo"),
                        ("PONTOS FORTES  ", "rotulo"), ("; ".join(fortes) + "\n", "bom"),
                        ("PONTOS FRACOS  ", "rotulo"), ("; ".join(fracos), "ruim")])
        self._status("consulta concluída", BOM)


if __name__ == "__main__":
    App().mainloop()
