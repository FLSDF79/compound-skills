#!/usr/bin/env python3
"""
compound.py — motor do SELF IMPROVEMENT COMPOUND SKILLS.

Crescimento ILIMITADO em profundidade. Teto RIGIDO em quantidade.

Zero dependencias externas. Python 3.8+. Portavel (macOS / Linux / WSL).

Grupos de comando
-----------------
  ESTADO      status, budget, use
  DECISAO     scan
  MEMORIA     ledger-add, ledger-list, anti-add, anti-list
  REGRESSAO   probe-add, probe-run
  SEGURANCA   backup, diff, rollback, sanitize, protect
  CICLO       commit, stub, review-due, review-renew, archive

Rode `compound.py <comando> -h` para detalhes de cada um.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from datetime import datetime, timedelta, timezone

VERSION = "2.2.0"

# ─────────────────────────── configuracao ───────────────────────────

HOME = os.path.expanduser("~")
BASE = os.environ.get("COMPOUND_HOME", os.path.join(HOME, ".compound-skills"))
SKILLS_ROOT = os.environ.get("COMPOUND_SKILLS_ROOT", os.path.join(HOME, ".claude", "skills"))
ARCHIVE_ROOT = os.path.join(BASE, "arquivadas")
BACKUPS = os.path.join(BASE, "backups")
STATE = os.path.join(BASE, "state.json")
LEDGER = os.path.join(BASE, "ledger.md")
ANTILEDGER = os.path.join(BASE, "anti-ledger.md")
CHANGELOG = os.path.join(BASE, "CHANGELOG.md")

# Tetos. Existem para os casos em que incomodam.
# Os defaults sao OPINATIVOS (calibrados para ~15-30 skills). Ajuste UMA vez,
# na instalacao, por ambiente — nunca por incomodo pontual no meio de um ciclo.
TETO_SKILLS_NOVAS_MES = int(os.environ.get("COMPOUND_TETO_NOVAS_MES", "1"))
TETO_EDICOES_DIA = int(os.environ.get("COMPOUND_TETO_EDICOES_DIA", "2"))  # por dia UTC, proxy verificavel de sessao
OCORRENCIAS_PARA_SKILL = int(os.environ.get("COMPOUND_REGRA_DE_N", "3"))
JANELA_REVISAO_DIAS = int(os.environ.get("COMPOUND_REVISAO_DIAS", "90"))
LEDGER_FRIO_DIAS = 60

# Orcamento de contexto: soma de TODAS as descricoes de skill instaladas.
# Estourou o teto, nada novo entra sem algo sair. Crescimento e soma zero em largura.
BUDGET_CHARS = int(os.environ.get("COMPOUND_BUDGET_CHARS", "16000"))
CHARS_POR_TOKEN = 4

# Skills que exigem confirmacao escrita a cada edicao.
# De fabrica, so o proprio motor. NAO liste suas skills aqui (codigo publico
# nao e lugar de inventario pessoal). Adicione as suas com:
#   compound.py protect add <nome>          (persiste em state.json)
# ou por ambiente: COMPOUND_PROTEGIDAS="infra-skill,compliance-skill"
PROTEGIDAS_PADRAO = ["compound-skills"] + [
    n.strip()
    for n in os.environ.get("COMPOUND_PROTEGIDAS", "").split(",")
    if n.strip()
]

# Palavras funcionais ignoradas no score lexical de gatilho.
STOP = set("""
a o as os um uma uns umas de do da dos das em no na nos nas por para com sem sob sobre
e ou mas que se quando onde como qual quais isso isto aquilo ao aos à às pelo pela
ser estar ter fazer usar use usar quando não nao nunca sempre apenas so só mais menos
the a an of to in on for with without and or but that this these those is are be use
when where how what which not never always only more less should must can may
skill skills usuario usuário user claude
""".split())

SEGREDO_PADROES = [
    (r"sk-[A-Za-z0-9_\-]{20,}", "chave estilo OpenAI/Anthropic (inclui sk-ant-, sk-proj-)"),
    (r"ghp_[A-Za-z0-9]{30,}", "token GitHub"),
    (r"glpat-[A-Za-z0-9_\-]{20,}", "token GitLab"),
    (r"npm_[A-Za-z0-9]{30,}", "token npm"),
    (r"\b\d{8,10}:AA[A-Za-z0-9_\-]{30,}\b", "token de bot Telegram"),
    (r"\b[sr]k_live_[A-Za-z0-9]{20,}\b", "chave Stripe live"),
    (r"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/\-]{15,}={0,2}",
     "header Bearer literal"),
    (r"github_pat_[A-Za-z0-9_]{50,}", "token GitHub fine-grained"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "token Slack"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"AIza[0-9A-Za-z_\-]{35}", "chave Google API"),
    (r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "chave privada"),
    (r"(?i)\b(?:senha|password|passwd|secret|api[_-]?key|token)\s*[:=]\s*[\"']?[^\s\"'{}<>]{8,}", "credencial literal"),
    (r"postgres(?:ql)?://[^\s]+:[^\s]+@", "string de conexao com senha"),
    (r"mongodb(?:\+srv)?://[^\s]+:[^\s]+@", "string de conexao com senha"),
]

PII_PADROES = [
    (r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "CPF"),
    (r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", "CNPJ"),
    (r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", "possivel cartao"),
    (r"(?i)\bag[êe]ncia\s*\d{4}\b.{0,40}\bconta\s*\d{3,}", "agencia+conta"),
    (r"(?i)#restricao", "marcador de conteudo restrito"),  # sanitize-ok
    (r"(?i)\b(?:confidencial|uso interno|sigiloso|proprietary)\b", "marcador de confidencialidade"),  # sanitize-ok
]

# Marcadores restritos ADICIONAIS do usuario (literais, case-insensitive).
# Ex.: COMPOUND_MARCADORES="#interno,PROJETO-X" — sem expor sua convencao no codigo.
for _m in os.environ.get("COMPOUND_MARCADORES", "").split(","):
    _m = _m.strip()
    if _m:
        PII_PADROES.append((r"(?i)" + re.escape(_m), f"marcador do usuario: {_m}"))
del _m


# ─────────────────────────── infra ───────────────────────────

def agora() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _ensure():
    os.makedirs(BACKUPS, exist_ok=True)
    for caminho, cabecalho in (
        (LEDGER, "# Ledger — o que subiu o piso\n\nAppend-only. Mais novo em cima.\n"),
        (ANTILEDGER,
         "# Anti-ledger — o que NAO funcionou\n\n"
         "Falha registrada e falha que nao se repete. Mais barato que acerto.\n"),
        (CHANGELOG, "# CHANGELOG\n"),
    ):
        if not os.path.exists(caminho):
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(cabecalho + "\n")
    if not os.path.exists(STATE):
        salvar_state({
            "versao": VERSION,
            "skills": {},
            "cota": {},
            "probes": {},
            "protegidas": list(PROTEGIDAS_PADRAO),
        })


def carregar_state() -> dict:
    _ensure()
    with open(STATE, encoding="utf-8") as f:
        st = json.load(f)
    st.setdefault("skills", {})
    st.setdefault("cota", {})
    st.setdefault("probes", {})
    st.setdefault("protegidas", list(PROTEGIDAS_PADRAO))
    return st


def salvar_state(st: dict):
    os.makedirs(BASE, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=BASE, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=2, ensure_ascii=False, sort_keys=True)
        os.replace(tmp, STATE)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def normalizar(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt)
    return "".join(c for c in txt if not unicodedata.combining(c)).lower()


def tokens(txt: str) -> set:
    palavras = re.findall(r"[a-z0-9][a-z0-9_-]{2,}", normalizar(txt))
    return {p for p in palavras if p not in STOP}


def nome_de(caminho: str) -> str:
    return os.path.basename(os.path.normpath(caminho))


def eh_stub(desc: str) -> bool:
    """Stubs de supersede nao contam como candidatos de novelty (so como custo)."""
    return desc.strip().upper().startswith("SUPERSEDIDA")


def nome_arg(v: str) -> str:
    """Valida nomes de skill vindos do CLI: sem separador de path, sem '..'."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", v) or ".." in v:
        raise argparse.ArgumentTypeError(f"nome de skill invalido: {v!r}")
    return v


def caminho_na_raiz(nome: str) -> str:
    """Resolve SKILLS_ROOT/<nome> e garante que segue DENTRO do root (anti-symlink)."""
    raiz = os.path.realpath(SKILLS_ROOT)
    destino = os.path.realpath(os.path.join(raiz, nome))
    if destino != raiz and not destino.startswith(raiz + os.sep):
        print(f"ERRO: caminho fora do skills root: {destino}", file=sys.stderr)
        sys.exit(2)
    return os.path.join(SKILLS_ROOT, nome)


def skillmd(caminho: str) -> str:
    return os.path.join(caminho, "SKILL.md") if os.path.isdir(caminho) else caminho


def ler_frontmatter(caminho_md: str) -> dict:
    """Parser minimo de frontmatter YAML. Sem dependencia externa de proposito."""
    if not os.path.exists(caminho_md):
        return {}
    with open(caminho_md, encoding="utf-8", errors="replace") as f:
        texto = f.read()
    if not texto.startswith("---"):
        return {}
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}
    bloco = texto[3:fim]
    dados, chave, buf = {}, None, []
    for linha in bloco.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", linha)
        if m:
            if chave:
                dados[chave] = " ".join(buf).strip()
            chave = m.group(1)
            valor = m.group(2).strip()
            buf = [] if valor in (">", "|", ">-", "|-") else [valor]
        elif chave and linha.strip():
            buf.append(linha.strip())
    if chave:
        dados[chave] = " ".join(buf).strip()
    return dados


def inventario(raiz: str = None) -> list:
    """Lista skills recursivamente, sem sair da raiz nem seguir symlinks."""
    raiz = raiz or SKILLS_ROOT
    itens = []
    if not os.path.isdir(raiz):
        return itens
    raiz_real = os.path.realpath(raiz)
    ignorar = {".git", ".venv", "__pycache__", "node_modules", "backups", "arquivadas"}
    nomes_vistos = set()
    for pasta, dirs, nomes in os.walk(raiz, followlinks=False):
        dirs[:] = sorted(
            d for d in dirs
            if d not in ignorar
            and not os.path.islink(os.path.join(pasta, d))
            and (lambda real: real == raiz_real or real.startswith(raiz_real + os.sep))(
                os.path.realpath(os.path.join(pasta, d)))
        )
        if "SKILL.md" not in nomes:
            continue
        pasta_real = os.path.realpath(pasta)
        if pasta_real != raiz_real and not pasta_real.startswith(raiz_real + os.sep):
            continue
        md = os.path.join(pasta, "SKILL.md")
        fm = ler_frontmatter(md)
        nome = fm.get("name", os.path.basename(pasta))
        if nome in nomes_vistos:
            dirs[:] = []
            continue
        nomes_vistos.add(nome)
        itens.append((nome, fm.get("description", ""), pasta))
        # Uma skill pode conter references/templates com fixtures; não os conte.
        dirs[:] = []
    return itens


def bar(frac: float, largura: int = 28) -> str:
    cheio = max(0, min(largura, int(round(frac * largura))))
    return "[" + "#" * cheio + "." * (largura - cheio) + "]"


# ─────────────────────────── orcamento de contexto ───────────────────────────

def cmd_budget(args) -> int:
    """A largura e soma zero. A profundidade nao."""
    itens = inventario(args.raiz)
    if not itens:
        print(f"Nenhuma skill em {args.raiz or SKILLS_ROOT}")
        return 0
    linhas = sorted(((len(d), n, eh_stub(d)) for n, d, _ in itens), reverse=True)
    total = sum(c for c, _, _ in linhas)
    frac = total / BUDGET_CHARS if BUDGET_CHARS else 0

    print(f"ORCAMENTO DE CONTEXTO  ({len(itens)} skills)")
    print(f"{bar(frac)} {total}/{BUDGET_CHARS} chars "
          f"(~{total // CHARS_POR_TOKEN} tokens) — {frac * 100:.0f}%")
    print()
    print(f"{'SKILL':<38} {'CHARS':>7} {'%':>6}")
    print("-" * 54)
    for chars, nome, stub in linhas[:args.top]:
        marca = " (stub)" if stub else ""
        print(f"{(nome[:30] + marca) if stub else nome[:37]:<38} "
              f"{chars:>7} {chars / total * 100:>5.1f}%")
    if len(linhas) > args.top:
        print(f"... mais {len(linhas) - args.top}")

    print()
    if frac >= 1.0:
        print("ESTOURADO. Nada novo entra sem algo sair.")
        print("As descricoes serao truncadas pelo host e as skills param de disparar.")
        print("Rode: compound.py review-due  →  arquive antes de criar.")
        return 1
    if frac >= 0.8:
        print("ATENCAO: acima de 80%. Proxima skill nova exige arquivar uma.")
    else:
        folga = BUDGET_CHARS - total
        print(f"Folga: {folga} chars (~{folga // 400} descricoes de tamanho medio).")
    return 0


# ─────────────────────────── novelty scan ───────────────────────────

def cmd_scan(args) -> int:
    """
    Mecaniza o que da para mecanizar (overlap lexical de gatilho, 0-30).
    Exige julgamento declarado para goal e mechanism — com justificativa.
    """
    itens = inventario(args.raiz)
    if not itens:
        print("Nenhuma skill instalada. novelty=100% — mas a Regra de 3 continua valendo.")
        return 0

    alvo = tokens(args.descricao)
    if not alvo:
        print("ERRO: descricao sem conteudo lexical util.", file=sys.stderr)
        return 1

    marcados = []
    for nome, desc, _ in itens:
        if args.excluir and nome == args.excluir:
            continue
        if eh_stub(desc):
            continue
        outro = tokens(desc)
        if not outro:
            continue
        inter = len(alvo & outro)
        # Containment: quanto da skill nova ja esta coberto pela existente.
        cont = inter / len(alvo)
        jac = inter / len(alvo | outro)
        # Vies deliberado para o containment: pergunta certa e "isso ja existe?",
        # nao "sao parecidas?".
        score = round(30 * (0.7 * cont + 0.3 * jac), 1)
        marcados.append((score, nome, sorted(alvo & outro)[:8]))

    if not marcados:
        print("Nenhum candidato comparavel (so stubs, vazias ou excluidas).")
        print("Eixo de gatilho = 0/30. Regra de 3, cota e orcamento continuam valendo.")
        top_score, top_nome = 0.0, "-"
    else:
        marcados.sort(reverse=True)
        print(f"OVERLAP LEXICAL DE GATILHO (0-30, mecanico) — {len(marcados)} candidatos\n")
        for score, nome, comuns in marcados[:args.top]:
            print(f"  {score:>5.1f}/30  {nome}")
            if comuns:
                print(f"           termos em comum: {', '.join(comuns)}")
        top_score, top_nome, _ = marcados[0]
    print()

    if args.goal is None or args.mech is None:
        print("Parcial. Faltam os dois eixos que exigem julgamento:")
        print("  --goal 0-40   0=outro problema | 20=mesma familia | 40=o MESMO job")
        print("  --mech 0-30   0=outra operacao | 15=mesmos passos, outro nome | 30=o MESMO pipeline")
        print(f"\nRode de novo:  compound.py scan \"...\" --goal N --mech N")
        print("Na duvida, SUPERESTIME o overlap. Errar para menos skill custa menos.")
        return 0

    overlap = min(100, args.goal + args.mech + top_score)
    novelty = round(100 - overlap, 1)

    sem_alvo = top_nome == "-"
    if novelty <= 30:
        decisao, acao = "ABSORB", f"patch minimo em `{top_nome}`. Mesmo nome."
    elif novelty <= 70:
        decisao, acao = "UPGRADE", f"reescrita robusta de `{top_nome}`, absorvendo conceitos E tarefas."
    else:
        decisao = "SUPERSEDE"
        acao = ("skill nova (nenhuma antiga para stubar)." if sem_alvo
                else f"skill nova; `{top_nome}` vira stub de 5 linhas.")
    if sem_alvo and decisao != "SUPERSEDE":
        acao += "  ATENCAO: voce declarou overlap alto sem candidato instalado — revise goal/mech."

    print(f"  goal={args.goal}/40  mech={args.mech}/30  trig={top_score}/30")
    print(f"  overlap={overlap}%  →  NOVELTY = {novelty}%")
    print(f"\n  DECISAO: {decisao}")
    print(f"  {acao}")

    if decisao == "SUPERSEDE":
        print("\n  SUPERSEDE ainda exige, cumulativamente:")
        print("    [ ] 3 ocorrencias no ledger (Regra de 3)")
        print("    [ ] cota mensal disponivel  → compound.py status")
        print("    [ ] orcamento de contexto   → compound.py budget")
        print("    [ ] probes de regressao     → compound.py probe-run")
        print("  Qualquer um faltando → cai para UPGRADE ou ledger.")
    return 0


# ─────────────────────────── probes de regressao ───────────────────────────

def cmd_probe_add(args) -> int:
    st = carregar_state()
    p = st["probes"].setdefault(args.skill, {"should": [], "should_not": []})
    alvo = "should" if args.should else "should_not"
    frase = args.should or args.should_not
    if frase in p[alvo]:
        print("Probe ja existe.")
        return 0
    p[alvo].append(frase)
    salvar_state(st)
    print(f"Probe adicionado a `{args.skill}` [{alvo}]: {frase}")
    print(f"  should: {len(p['should'])}  |  should_not: {len(p['should_not'])}")
    if len(p["should"]) < 3:
        print(f"  Minimo recomendado: 3 should. Faltam {3 - len(p['should'])}.")
    return 0


def _match(frase: str, desc: str) -> float:
    t_frase, t_desc = tokens(frase), tokens(desc)
    if not t_frase:
        return 0.0
    return len(t_frase & t_desc) / len(t_frase)


def cmd_probe_run(args) -> int:
    """
    A rede de seguranca que faltava nos dois motores anteriores.
    Detecta: gatilho quebrado por edicao, e captura cruzada entre skills.
    """
    st = carregar_state()
    itens = inventario(args.raiz)
    descs = {n: d for n, d, _ in itens}
    alvos = [args.skill] if args.skill else sorted(st["probes"].keys())
    if not alvos:
        print("Nenhum probe registrado. Adicione com: compound.py probe-add ...")
        return 0

    falhas = 0
    for skill in alvos:
        p = st["probes"].get(skill)
        if not p:
            print(f"[{skill}] sem probes.")
            continue
        if skill not in descs:
            print(f"[{skill}] SKILL NAO INSTALADA — probes orfaos.")
            falhas += 1
            continue

        print(f"\n[{skill}]")
        for frase in p["should"]:
            proprio = _match(frase, descs[skill])
            rivais = sorted(
                ((_match(frase, d), n) for n, d in descs.items() if n != skill),
                reverse=True,
            )
            melhor_rival, nome_rival = rivais[0] if rivais else (0.0, "-")
            if proprio < args.limiar:
                print(f"  FALHA  should  ({proprio:.2f} < {args.limiar})  \"{frase}\"")
                print(f"         a descricao perdeu os termos desta frase.")
                falhas += 1
            elif melhor_rival >= proprio:
                print(f"  COLISAO should  (proprio {proprio:.2f} <= `{nome_rival}` {melhor_rival:.2f})")
                print(f"         \"{frase}\"")
                falhas += 1
            else:
                print(f"  ok     should  ({proprio:.2f} vs rival {melhor_rival:.2f})  \"{frase[:52]}\"")

        for frase in p["should_not"]:
            proprio = _match(frase, descs[skill])
            if proprio >= args.limiar:
                print(f"  FALHA  should-not ({proprio:.2f} >= {args.limiar})  \"{frase}\"")
                print(f"         a skill esta capturando o que nao deveria.")
                falhas += 1
            else:
                print(f"  ok     should-not ({proprio:.2f})  \"{frase[:52]}\"")

    print(f"\n{'=' * 56}")
    if falhas:
        print(f"{falhas} falha(s). NAO PUBLIQUE a alteracao.")
        print("Reverta com: compound.py rollback <skill>")
        return 1
    print("Todos os probes passaram.")
    return 0


# ─────────────────────────── ledger / anti-ledger ───────────────────────────

def _titulo_seguro(p: str) -> str:
    """Titulo vira `## <p>`; quebra de linha ou '#' inicial corromperia o parse."""
    p = " ".join((p or "").split()).lstrip("#").strip()
    return p[:120] or "(sem nome)"


def _uma_linha(p: str) -> str:
    return " ".join((p or "").split())


def _append_bloco(caminho: str, cabecalho: str, linha: str):
    _ensure()
    with open(caminho, encoding="utf-8") as f:
        txt = f.read()
    if cabecalho in txt:
        antes, resto = txt.split(cabecalho, 1)
        corte = resto.find("\n## ")
        bloco, cauda = (resto, "") if corte == -1 else (resto[:corte], resto[corte:])
        txt = antes + cabecalho + bloco.rstrip("\n") + "\n" + linha + cauda
    else:
        txt = txt.rstrip("\n") + f"\n\n{cabecalho}\n{linha}"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(txt)


def cmd_ledger_add(args) -> int:
    padrao = _titulo_seguro(args.padrao)
    cab = f"## {padrao}"
    linha = f"- [{agora():%Y-%m-%d}] {_uma_linha(args.contexto) or 'contexto nao informado'}\n"
    _append_bloco(LEDGER, cab, linha)
    n = len(_blocos(LEDGER).get(padrao, []))
    print(f"Registrado: {padrao}  ({n} ocorrencia(s))")
    if n >= OCORRENCIAS_PARA_SKILL:
        print("  Regra de 3 ATINGIDA → ELEGIVEL, se passar em scan, cota, budget e probes.")
    else:
        print(f"  Faltam {OCORRENCIAS_PARA_SKILL - n}. Segue como nota, nao como skill.")
    return 0


def cmd_anti_add(args) -> int:
    padrao = _titulo_seguro(args.padrao)
    cab = f"## {padrao}"
    linha = (f"- [{agora():%Y-%m-%d}] TENTADO: {_uma_linha(args.tentativa)}\n"
             f"  FALHOU PORQUE: {_uma_linha(args.motivo)}\n")
    _append_bloco(ANTILEDGER, cab, linha)
    print(f"Anti-ledger: {padrao}")
    print("Caminho fechado. A proxima execucao nao paga esse custo de novo.")
    return 0


def _blocos(caminho: str) -> dict:
    _ensure()
    with open(caminho, encoding="utf-8") as f:
        linhas = f.read().splitlines()
    blocos, atual = {}, None
    for ln in linhas:
        if ln.startswith("## "):
            atual = ln[3:].strip()
            blocos[atual] = []
        elif atual and ln.strip().startswith("- ["):
            blocos[atual].append(ln.strip())
    return blocos


def _listar(caminho: str, titulo: str, com_status: bool) -> int:
    blocos = _blocos(caminho)
    if not blocos:
        print(f"{titulo} vazio.")
        return 0
    hoje = agora()
    print(f"{titulo}\n")
    for padrao, itens in blocos.items():
        n = len(itens)
        if not com_status:
            print(f"  {padrao}  ({n})")
            continue
        datas = []
        for it in itens:
            try:
                # linha `- [AAAA-MM-DD] ...` — a data comeca no indice 3
                datas.append(datetime.strptime(it[3:13], "%Y-%m-%d").replace(tzinfo=timezone.utc))
            except Exception:
                pass
        ultima = max(datas) if datas else None
        if n >= OCORRENCIAS_PARA_SKILL:
            status = "ELEGIVEL"
        elif ultima and (hoje - ultima).days > LEDGER_FRIO_DIAS:
            status = f"FRIO ({(hoje - ultima).days}d) → descartar"
        else:
            status = f"aguardando ({OCORRENCIAS_PARA_SKILL - n})"
        print(f"  {padrao[:44]:<46} {n:>2}  {status}")
    return 0


def cmd_ledger_list(args) -> int:
    return _listar(LEDGER, "LEDGER — candidatas", True)


def cmd_anti_list(args) -> int:
    return _listar(ANTILEDGER, "ANTI-LEDGER — caminhos fechados", False)


# ─────────────────────────── seguranca ───────────────────────────

def _fazer_backup(origem: str) -> str:
    """Copia a skill para BACKUPS/<nome>__<timestamp>. Nome de dir saneado."""
    _ensure()
    nome = re.sub(r"[^A-Za-z0-9._-]", "_", nome_de(origem)) or "sem-nome"
    destino = os.path.join(BACKUPS, f"{nome}__{agora():%Y%m%d-%H%M%S}")
    if os.path.isdir(origem):
        shutil.copytree(origem, destino)
    else:
        os.makedirs(destino, exist_ok=True)
        shutil.copy2(origem, os.path.join(destino, os.path.basename(origem)))
    return destino


def cmd_backup(args) -> int:
    origem = os.path.normpath(args.caminho)
    if not os.path.exists(origem):
        print(f"ERRO: nao existe: {origem}", file=sys.stderr)
        return 1
    nome = nome_de(origem)
    destino = _fazer_backup(origem)
    print(f"Backup: {destino}")
    st = carregar_state()
    if nome in st["protegidas"]:
        print(f"\n  PROTEGIDA. `{nome}` exige confirmacao escrita do dono NESTA ocasiao.")
        print("  Confirmacao de sessao anterior nao vale.")
    return 0


def _ultimo_backup(nome: str):
    if not os.path.isdir(BACKUPS):
        return None
    c = sorted(d for d in os.listdir(BACKUPS) if d.startswith(nome + "__"))
    return os.path.join(BACKUPS, c[-1]) if c else None


def cmd_diff(args) -> int:
    origem = os.path.normpath(args.caminho)
    nome = nome_de(origem)
    bkp = _ultimo_backup(nome)
    if not bkp:
        print(f"Sem backup de `{nome}`. Rode: compound.py backup {origem}", file=sys.stderr)
        return 1
    a_p, b_p = os.path.join(bkp, "SKILL.md"), skillmd(origem)
    if not (os.path.exists(a_p) and os.path.exists(b_p)):
        print("ERRO: SKILL.md ausente em um dos lados.", file=sys.stderr)
        return 1
    with open(a_p, encoding="utf-8") as f:
        a = f.readlines()
    with open(b_p, encoding="utf-8") as f:
        b = f.readlines()
    d = list(difflib.unified_diff(a, b, fromfile=f"{nome} (backup)",
                                  tofile=f"{nome} (atual)", n=2))
    if not d:
        print("Sem diferencas.")
    else:
        sys.stdout.writelines(d)
        fa = ler_frontmatter(a_p).get("description", "")
        fb = ler_frontmatter(b_p).get("description", "")
        if fa != fb:
            print("\n>>> A DESCRICAO MUDOU. O gatilho mudou junto.")
            print(">>> Obrigatorio antes de aplicar: compound.py probe-run " + nome)
    return 0


def cmd_rollback(args) -> int:
    bkp = _ultimo_backup(args.nome)
    if not bkp:
        print(f"Sem backup de `{args.nome}`.", file=sys.stderr)
        return 1
    destino = caminho_na_raiz(args.nome)
    if os.path.isdir(destino):
        preservado = f"{destino}.pre-rollback-{agora():%Y%m%d-%H%M%S}"
        shutil.move(destino, preservado)
        print(f"Estado atual preservado: {preservado}")
    shutil.copytree(bkp, destino)
    print(f"Rollback: {args.nome} <- {os.path.basename(bkp)}")
    _changelog(args.nome, "rollback", "-", f"restaurado de {os.path.basename(bkp)}")
    return 0


MARCADOR_OK = "sanitize-ok"


def _carregar_ignore(raiz: str) -> list:
    """
    Le .sanitizeignore (um glob por linha, # comenta).
    Existe porque o proprio scanner e seus testes contem padroes por definicao —
    e um scanner que nao consegue passar em si mesmo nao e usavel em CI.
    Use com parcimonia: cada linha aqui e um ponto cego que voce escolheu ter.
    """
    caminho = os.path.join(raiz, ".sanitizeignore")
    if not os.path.exists(caminho):
        return []
    padroes = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.split("#", 1)[0].strip()
            if linha:
                padroes.append(linha)
    return padroes


def cmd_sanitize(args) -> int:
    """Rode ANTES de qualquer git commit. Um vazamento em repo publico e permanente."""
    import fnmatch

    raiz = os.path.normpath(args.caminho)
    ignore_globs = _carregar_ignore(raiz)
    achados, arquivos, suprimidos = [], 0, 0
    ignorar = {".git", "node_modules", "__pycache__", ".venv", "backups"}

    for pasta, dirs, nomes in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in ignorar]
        for nome in nomes:
            if nome.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip",
                              ".pyc", ".woff", ".woff2", ".ico")):
                continue
            caminho = os.path.join(pasta, nome)
            try:
                with open(caminho, encoding="utf-8", errors="replace") as f:
                    linhas = f.readlines()
            except Exception:
                continue
            arquivos += 1
            rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
            if any(fnmatch.fnmatch(rel, g) for g in ignore_globs):
                suprimidos += 1
                continue
            for i, linha in enumerate(linhas, 1):
                if MARCADOR_OK in linha:
                    suprimidos += 1
                    continue
                for pad, rotulo in SEGREDO_PADROES:
                    m = re.search(pad, linha)
                    if m:
                        valor = m.group(0)
                        fp = hashlib.sha256(valor.encode("utf-8")).hexdigest()[:8]
                        achados.append(("SEGREDO", rel, i, rotulo, fp))
                for pad, rotulo in PII_PADROES:
                    m = re.search(pad, linha)
                    if m:
                        valor = m.group(0)
                        fp = hashlib.sha256(valor.encode("utf-8")).hexdigest()[:8]
                        achados.append(("PII/RESTRITO", rel, i, rotulo, fp))
            if HOME != "/" and HOME in "".join(linhas):
                achados.append(("CAMINHO", rel, 0, "path pessoal absoluto", None))

    print(f"SANITIZE — {arquivos} arquivos em {raiz}")
    if suprimidos:
        print(f"           {suprimidos} linha(s)/arquivo(s) suprimidos por allowlist "
              f"— cada um e um ponto cego escolhido.")
    print()
    if not achados:
        print("Nada encontrado. Seguro para commit.")
        print("Lembrete: o scanner e heuristico. Ele reduz risco; nao o elimina.")
        return 0

    vistos = set()
    for tipo, rel, ln, rotulo, info in achados:
        chave = (tipo, rel, rotulo)
        if chave in vistos:
            continue
        vistos.add(chave)
        loc = f"{rel}:{ln}" if ln else rel
        print(f"  [{tipo}] {loc}")
        if info:
            print(f"      {rotulo} [fp:{info}]")
        else:
            print(f"      {rotulo}")
    print(f"\n{len(vistos)} ocorrencia(s) distinta(s). NAO COMMITE antes de resolver.")
    return 1


def cmd_protect(args) -> int:
    """Gerencia a lista de skills protegidas SEM hardcode no codigo-fonte."""
    st = carregar_state()
    prot = st.setdefault("protegidas", list(PROTEGIDAS_PADRAO))
    if args.acao == "list":
        print("PROTEGIDAS — exigem confirmacao escrita do dono a cada edicao:")
        for n in sorted(set(prot)):
            print(f"  {n}")
        print("\nGerencie com: compound.py protect add|remove <nome>")
        return 0
    if not args.nome:
        print("ERRO: informe o nome da skill.", file=sys.stderr)
        return 1
    if args.acao == "add":
        if args.nome in prot:
            print(f"`{args.nome}` ja e protegida.")
            return 0
        prot.append(args.nome)
        salvar_state(st)
        print(f"Protegida: {args.nome}  (persistido em state.json, fora do codigo)")
        return 0
    # remove
    if args.nome == "compound-skills":
        print("BLOQUEADO: o proprio motor permanece protegido. Sempre.", file=sys.stderr)
        return 2
    if args.nome not in prot:
        print(f"`{args.nome}` nao esta na lista.")
        return 1
    prot.remove(args.nome)
    salvar_state(st)
    print(f"Desprotegida: {args.nome}")
    return 0


# ─────────────────────────── ciclo ───────────────────────────

def _mes() -> str:
    return f"{agora():%Y-%m}"


def _dia() -> str:
    return f"{agora():%Y-%m-%d}"


def _cota(st: dict) -> dict:
    c = st.get("cota", {})
    if c.get("mes") != _mes():
        c = {"mes": _mes(), "novas": 0, "dia": _dia(), "edicoes_dia": 0}
        st["cota"] = c
    if c.get("dia") != _dia():
        c["dia"], c["edicoes_dia"] = _dia(), 0
    return c


def _changelog(nome: str, tipo: str, versao: str, nota: str):
    _ensure()
    with open(CHANGELOG, "a", encoding="utf-8") as f:
        f.write(f"\n## {agora():%Y-%m-%d %H:%M} — {nome} [{tipo}] v{versao}\n{nota}\n")


def _bump(v: str, tipo: str) -> str:
    try:
        ma, mi, pa = (int(x) for x in v.split("."))
    except Exception:
        ma, mi, pa = 0, 0, 0
    return {"major": f"{ma+1}.0.0", "minor": f"{ma}.{mi+1}.0"}.get(tipo, f"{ma}.{mi}.{pa+1}")


def cmd_commit(args) -> int:
    if not os.path.exists(skillmd(args.caminho)):
        print(f"ERRO: SKILL.md nao encontrado em {args.caminho}", file=sys.stderr)
        return 1
    try:
        nome = nome_arg(nome_de(args.caminho))
    except argparse.ArgumentTypeError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2
    st = carregar_state()
    registrada = nome in st["skills"]
    e = st["skills"].get(nome, {"versao": "0.0.0", "criada": iso(agora()), "usos": 0})
    # Skill nova = fora do state E decisao supersede (criacao consome cota).
    # Fora do state com absorb/upgrade = ADOCAO de skill pre-existente no disco:
    # a descricao dela ja esta no orcamento — nao consome cota de nova.
    nova_skill = (not registrada) and args.decisao == "supersede"
    adocao = (not registrada) and args.decisao != "supersede"

    c = _cota(st)
    if c.get("edicoes_dia", 0) >= TETO_EDICOES_DIA:
        print(f"BLOQUEADO: teto de {TETO_EDICOES_DIA} edicoes/sessao ja consumido "
              f"hoje ({c['dia']}).", file=sys.stderr)
        print("O script aplica o teto por dia UTC, como proxy verificavel de sessao.",
              file=sys.stderr)
        print("Registre no ledger e volte amanha. Padrao bom espera.", file=sys.stderr)
        return 4

    if nova_skill:
        if c.get("novas", 0) >= TETO_SKILLS_NOVAS_MES:
            print(f"BLOQUEADO: cota de {TETO_SKILLS_NOVAS_MES} skill nova/mes "
                  f"ja consumida em {c['mes']}.", file=sys.stderr)
            print("Va para o ledger. Padrao bom sobrevive a 30 dias de espera.", file=sys.stderr)
            return 2
        itens = inventario()
        total = sum(len(d) for _, d, _ in itens)
        if total >= BUDGET_CHARS:
            print(f"BLOQUEADO: orcamento de contexto estourado "
                  f"({total}/{BUDGET_CHARS}).", file=sys.stderr)
            print("Largura e soma zero. Arquive algo antes: compound.py review-due",
                  file=sys.stderr)
            return 3
        c["novas"] = c.get("novas", 0) + 1

    c["edicoes_dia"] = c.get("edicoes_dia", 0) + 1
    if nova_skill or adocao:
        versao = "1.0.0"
    else:
        versao = _bump(e["versao"], args.tipo)
    e.update({
        "versao": versao,
        "ultima_alteracao": iso(agora()),
        "revisao_em": iso(agora() + timedelta(days=JANELA_REVISAO_DIAS)),
        "protegida": nome in st["protegidas"],
        "decisao": args.decisao,
        "novelty": args.novelty,
    })
    if args.absorveu:
        e.setdefault("procedencia", []).append({
            "de": args.absorveu, "em": iso(agora()), "decisao": args.decisao,
        })
    st["skills"][nome] = e
    salvar_state(st)

    proc = f" absorveu={args.absorveu}" if args.absorveu else ""
    _changelog(nome, args.decisao, versao,
               f"novelty={args.novelty}%{proc}\n{args.nota}")

    print(f"{nome} → v{versao}   [{args.decisao.upper()}]  novelty={args.novelty}%")
    print(f"Revisao agendada: {e['revisao_em'][:10]}")
    if nova_skill:
        print("Cota de skill nova do mes CONSUMIDA.")
    if adocao:
        print("Skill pre-existente ADOTADA pelo motor (nao consome cota de nova).")
    if args.absorveu:
        print(f"Procedencia registrada: absorveu `{args.absorveu}`.")
    print("\nObrigatorio agora:")
    print(f"  1. compound.py probe-run {nome}")
    print(f"  2. compound.py budget")
    print("  3. auditoria externa (/checkup ou equivalente). Quem cria nao audita sozinho.")
    return 0


def cmd_stub(args) -> int:
    caminho = caminho_na_raiz(args.antiga)
    md = os.path.join(caminho, "SKILL.md")
    if not os.path.exists(md):
        print(f"Nao encontrada: {md}", file=sys.stderr)
        return 1
    st = carregar_state()
    if args.antiga in st["protegidas"]:
        print(f"BLOQUEADO: `{args.antiga}` e protegida.", file=sys.stderr)
        return 2
    bkp = _fazer_backup(caminho)
    print(f"Backup automatico antes do stub: {bkp}")
    fm = ler_frontmatter(md)
    with open(md, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"name: {fm.get('name', args.antiga)}\n")
        f.write(f"description: SUPERSEDIDA por `{args.nova}`. Nao use esta skill; "
                f"todo o dominio migrou. Mantida apenas como ponteiro para nao "
                f"quebrar referencias antigas.\n")
        f.write("---\n\n")
        f.write(f"# {args.antiga} — supersedida\n\n")
        f.write(f"Substituida por **`{args.nova}`** em {agora():%Y-%m-%d}.\n\n")
        f.write(f"Motivo: {args.motivo}\n\n")
        f.write(f"Abra `{args.nova}`. Nao edite este arquivo.\n")
    print(f"Stub criado: {args.antiga} → {args.nova}")
    print("Um playbook vivo por trabalho. Dois motores derivam.")
    _changelog(args.antiga, "supersede", "-", f"stub → {args.nova}: {args.motivo}")
    return 0


def cmd_use(args) -> int:
    st = carregar_state()
    e = st["skills"].setdefault(args.nome, {"versao": "1.0.0", "usos": 0})
    e["usos"] = e.get("usos", 0) + 1
    e["ultimo_uso"] = iso(agora())
    salvar_state(st)
    print(f"{args.nome}: {e['usos']} uso(s), ultimo em {e['ultimo_uso'][:10]}")
    return 0


def cmd_review_due(args) -> int:
    st = carregar_state()
    hoje = agora()
    venc = []
    for nome, e in st["skills"].items():
        if "arquivada_em" in e or "revisao_em" not in e:
            continue
        try:
            d = parse_iso(e["revisao_em"])
        except Exception:
            continue
        if d <= hoje:
            venc.append((nome, e, (hoje - d).days))
    if not venc:
        print("Nenhuma skill vencida.")
        return 0
    print("VENCIDAS — decidir: manter / fundir / arquivar\n")
    for nome, e, atraso in sorted(venc, key=lambda x: -x[2]):
        usos = e.get("usos", 0)
        ult = e.get("ultimo_uso", "nunca")[:10]
        tag = " [PROTEGIDA]" if e.get("protegida") else ""
        sinal = "  ← SEM USO, forte candidata a arquivo" if usos == 0 else ""
        print(f"  {nome}{tag}  v{e.get('versao','?')}  vencida ha {atraso}d  "
              f"usos={usos} ultimo={ult}{sinal}")
    print("\nNa duvida, arquive. Arquivar e reversivel; skill morta viva e cara e invisivel.")
    return 0


def cmd_review_renew(args) -> int:
    st = carregar_state()
    if args.nome not in st["skills"]:
        print(f"`{args.nome}` nao esta no state.", file=sys.stderr)
        return 1
    st["skills"][args.nome]["revisao_em"] = iso(agora() + timedelta(days=JANELA_REVISAO_DIAS))
    salvar_state(st)
    print(f"{args.nome}: revisao renovada para "
          f"{st['skills'][args.nome]['revisao_em'][:10]}")
    return 0


def cmd_archive(args) -> int:
    st = carregar_state()
    if args.nome in st["protegidas"]:
        print(f"BLOQUEADO: `{args.nome}` e protegida.", file=sys.stderr)
        return 2
    origem = caminho_na_raiz(args.nome)
    if not os.path.isdir(origem):
        print(f"Nao encontrada: {origem}", file=sys.stderr)
        return 1
    os.makedirs(ARCHIVE_ROOT, exist_ok=True)
    destino = os.path.join(ARCHIVE_ROOT, f"{args.nome}__{agora():%Y%m%d}")
    shutil.move(origem, destino)
    st["skills"].setdefault(args.nome, {})["arquivada_em"] = iso(agora())
    salvar_state(st)
    _changelog(args.nome, "arquivada", "-", f"→ {destino}")
    print(f"Arquivada: {destino}")
    print("Reversivel: mova de volta para o skills root.")
    return 0


def cmd_status(args) -> int:
    st = carregar_state()
    c = _cota(st)
    salvar_state(st)
    ativas = [k for k, v in st["skills"].items() if "arquivada_em" not in v]
    print("=" * 60)
    print(f" SELF IMPROVEMENT COMPOUND SKILLS  v{VERSION}")
    print("=" * 60)
    print(f"\n Skills sob gestao : {len(ativas)}")
    print(f" Cota {c['mes']}      : {c.get('novas',0)}/{TETO_SKILLS_NOVAS_MES} skills novas")
    print(f" Edicoes hoje      : {c.get('edicoes_dia',0)}/{TETO_EDICOES_DIA}")
    print(f" Protegidas        : {', '.join(sorted(set(st.get('protegidas', []))))}")
    print(f" Estado em disco   : {BASE}")
    print(f" Skills root       : {SKILLS_ROOT}")
    print("\n--- ORCAMENTO ---")
    cmd_budget(argparse.Namespace(raiz=None, top=5))
    print("\n--- LEDGER ---")
    cmd_ledger_list(args)
    print("\n--- ANTI-LEDGER ---")
    cmd_anti_list(args)
    print("\n--- REVISAO ---")
    cmd_review_due(args)
    return 0


# ─────────────────────────── cli ───────────────────────────

def main():
    p = argparse.ArgumentParser(
        prog="compound.py",
        description=f"SELF IMPROVEMENT COMPOUND SKILLS v{VERSION} — "
                    "profundidade ilimitada, largura com teto.")
    p.add_argument("--version", action="version", version=VERSION)
    s = p.add_subparsers(dest="cmd", required=True)

    s.add_parser("status", help="visao geral").set_defaults(fn=cmd_status)

    b = s.add_parser("budget", help="orcamento de contexto das descricoes")
    b.add_argument("--raiz"); b.add_argument("--top", type=int, default=12)
    b.set_defaults(fn=cmd_budget)

    sc = s.add_parser("scan", help="novelty % contra as skills instaladas")
    sc.add_argument("descricao")
    sc.add_argument("--goal", type=int, choices=range(0, 41), metavar="0-40")
    sc.add_argument("--mech", type=int, choices=range(0, 31), metavar="0-30")
    sc.add_argument("--excluir"); sc.add_argument("--raiz")
    sc.add_argument("--top", type=int, default=5)
    sc.set_defaults(fn=cmd_scan)

    pa = s.add_parser("probe-add", help="registra frase-teste de gatilho")
    pa.add_argument("skill", type=nome_arg)
    g = pa.add_mutually_exclusive_group(required=True)
    g.add_argument("--should"); g.add_argument("--should-not", dest="should_not")
    pa.set_defaults(fn=cmd_probe_add)

    pr = s.add_parser("probe-run", help="testa gatilhos e colisao")
    pr.add_argument("skill", nargs="?", type=nome_arg); pr.add_argument("--raiz")
    pr.add_argument("--limiar", type=float, default=0.34)
    pr.set_defaults(fn=cmd_probe_run)

    la = s.add_parser("ledger-add", help="registra ocorrencia de padrao")
    la.add_argument("padrao"); la.add_argument("--contexto", default="")
    la.set_defaults(fn=cmd_ledger_add)
    s.add_parser("ledger-list").set_defaults(fn=cmd_ledger_list)

    aa = s.add_parser("anti-add", help="registra caminho que NAO funcionou")
    aa.add_argument("padrao"); aa.add_argument("--tentativa", required=True)
    aa.add_argument("--motivo", required=True)
    aa.set_defaults(fn=cmd_anti_add)
    s.add_parser("anti-list").set_defaults(fn=cmd_anti_list)

    for nome, fn in (("backup", cmd_backup), ("diff", cmd_diff)):
        sp = s.add_parser(nome); sp.add_argument("caminho"); sp.set_defaults(fn=fn)
    rb = s.add_parser("rollback"); rb.add_argument("nome", type=nome_arg); rb.set_defaults(fn=cmd_rollback)

    pt = s.add_parser("protect", help="lista/gerencia skills protegidas (state.json)")
    pt.add_argument("acao", choices=["add", "remove", "list"])
    pt.add_argument("nome", nargs="?", type=nome_arg)
    pt.set_defaults(fn=cmd_protect)

    sa = s.add_parser("sanitize", help="varre segredos/PII antes de publicar")
    sa.add_argument("caminho"); sa.set_defaults(fn=cmd_sanitize)

    cm = s.add_parser(
        "commit",
        help="versiona, consome cota, agenda revisao",
        description="supersede em skill fora do state = CRIACAO (consome cota de "
                    "nova). absorb/upgrade em skill fora do state = ADOCAO de "
                    "pre-existente (nao consome). Toda gravacao consome 1 edicao "
                    "do dia (teto por dia UTC, proxy de sessao).")
    cm.add_argument("caminho")
    cm.add_argument("--tipo", choices=["patch", "minor", "major"], default="patch")
    cm.add_argument("--decisao", choices=["absorb", "upgrade", "supersede"], required=True)
    cm.add_argument("--novelty", type=int, choices=range(0, 101),
                    metavar="0-100", required=True)
    cm.add_argument("--nota", required=True)
    cm.add_argument("--absorveu")
    cm.set_defaults(fn=cmd_commit)

    stb = s.add_parser("stub", help="converte skill antiga em ponteiro")
    stb.add_argument("antiga", type=nome_arg); stb.add_argument("nova", type=nome_arg)
    stb.add_argument("--motivo", required=True)
    stb.set_defaults(fn=cmd_stub)

    us = s.add_parser("use", help="registra uso (telemetria de decaimento)")
    us.add_argument("nome", type=nome_arg); us.set_defaults(fn=cmd_use)

    s.add_parser("review-due").set_defaults(fn=cmd_review_due)
    rr = s.add_parser("review-renew"); rr.add_argument("nome", type=nome_arg); rr.set_defaults(fn=cmd_review_renew)
    ar = s.add_parser("archive"); ar.add_argument("nome", type=nome_arg); ar.set_defaults(fn=cmd_archive)

    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
