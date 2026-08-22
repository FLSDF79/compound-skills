"""Testes do SELF IMPROVEMENT COMPOUND SKILLS.

Sem dependências: unittest + subprocess. Cada teste roda o CLI num HOME
temporário isolado, exatamente como um usuário rodaria.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skill" / "compound-skills" / "scripts" / "compound.py"
SKILL_DIR = REPO / "skill" / "compound-skills"

FRONT = "---\nname: {n}\ndescription: {d}\n---\n\n# {n}\n\ncorpo\n"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.root = self.home / "skills"
        self.root.mkdir()
        self.env = dict(
            os.environ,
            HOME=str(self.home),
            COMPOUND_HOME=str(self.home / ".compound-skills"),
            COMPOUND_SKILLS_ROOT=str(self.root),
        )
        self.env.pop("COMPOUND_PROTEGIDAS", None)
        self.env.pop("COMPOUND_BUDGET_CHARS", None)
        self.env.pop("COMPOUND_TETO_NOVAS_MES", None)
        self.env.pop("COMPOUND_TETO_EDICOES_DIA", None)
        self.env.pop("COMPOUND_MARCADORES", None)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, env_extra=None):
        env = dict(self.env)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True, text=True, env=env,
        )

    def make_skill(self, nome, desc):
        pasta = self.root / nome
        pasta.mkdir()
        (pasta / "SKILL.md").write_text(FRONT.format(n=nome, d=desc), encoding="utf-8")
        return pasta


class TestEstado(Base):
    def test_status_cria_estado_e_mostra_protegidas(self):
        r = self.run_cli("status")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("SELF IMPROVEMENT COMPOUND SKILLS", r.stdout)
        self.assertIn("compound-skills", r.stdout)
        self.assertTrue((self.home / ".compound-skills" / "state.json").exists())

    def test_budget_estourado_bloqueia(self):
        self.make_skill("grande", "x" * 50)
        r = self.run_cli("budget", env_extra={"COMPOUND_BUDGET_CHARS": "10"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("ESTOURADO", r.stdout)

    def test_budget_sinaliza_stub(self):
        self.make_skill("viva", "analise de dados tabulares em planilha")
        self.make_skill("morta", "SUPERSEDIDA por `viva`. Nao use esta skill.")
        r = self.run_cli("budget")
        self.assertIn("(stub)", r.stdout)

    def test_budget_encontra_skill_em_categoria_aninhada(self):
        pasta = self.root / "categoria" / "aninhada"
        pasta.mkdir(parents=True)
        (pasta / "SKILL.md").write_text(
            FRONT.format(n="aninhada", d="skill organizada em categoria"),
            encoding="utf-8")
        r = self.run_cli("budget")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("(1 skills)", r.stdout)
        self.assertIn("aninhada", r.stdout)

    def test_budget_nao_segue_symlink_para_fora_da_raiz(self):
        externa = self.home / "externa"
        externa.mkdir()
        (externa / "SKILL.md").write_text(
            FRONT.format(n="externa", d="nao deve ser inventariada"),
            encoding="utf-8")
        try:
            (self.root / "atalho").symlink_to(externa, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink indisponivel neste sistema")
        r = self.run_cli("budget")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Nenhuma skill", r.stdout)


class TestProtegidas(Base):
    def test_protect_add_list_remove(self):
        self.assertEqual(self.run_cli("protect", "add", "minha-infra").returncode, 0)
        r = self.run_cli("protect", "list")
        self.assertIn("minha-infra", r.stdout)
        self.assertEqual(self.run_cli("protect", "remove", "minha-infra").returncode, 0)
        self.assertNotIn("minha-infra", self.run_cli("protect", "list").stdout)

    def test_motor_nunca_desprotege(self):
        r = self.run_cli("protect", "remove", "compound-skills")
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOQUEADO", r.stderr)

    def test_default_de_fabrica_sem_inventario_pessoal(self):
        r = self.run_cli("protect", "list")
        linhas = [l.strip() for l in r.stdout.splitlines()
                  if l.startswith("  ")]
        self.assertEqual(linhas, ["compound-skills"])

    def test_protegidas_extras_por_ambiente(self):
        r = self.run_cli("protect", "list",
                         env_extra={"COMPOUND_PROTEGIDAS": "infra-a, infra-b"})
        self.assertIn("infra-a", r.stdout)
        self.assertIn("infra-b", r.stdout)

    def test_archive_de_protegida_bloqueado(self):
        self.make_skill("critica", "skill de conformidade")
        self.run_cli("protect", "add", "critica")
        r = self.run_cli("archive", "critica")
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOQUEADO", r.stderr)


class TestNomesSeguros(Base):
    def test_path_traversal_rejeitado(self):
        for cmd in (["archive", "../evil"], ["rollback", "a/b"],
                    ["use", ".."], ["stub", "../x", "y", "--motivo", "m"]):
            r = self.run_cli(*cmd)
            self.assertEqual(r.returncode, 2, cmd)
            self.assertIn("invalido", r.stderr)


class TestLedger(Base):
    def test_regra_de_3(self):
        self.run_cli("ledger-add", "padrao-x", "--contexto", "dominio 1")
        r = self.run_cli("ledger-add", "padrao-x", "--contexto", "dominio 2")
        self.assertIn("Faltam 1", r.stdout)
        r = self.run_cli("ledger-add", "padrao-x", "--contexto", "dominio 3")
        self.assertIn("ELEGIVEL", r.stdout)
        self.assertIn("ELEGIVEL", self.run_cli("ledger-list").stdout)

    def test_anti_ledger(self):
        r = self.run_cli("anti-add", "caminho-y",
                         "--tentativa", "regex direto", "--motivo", "quebra em acentos")
        self.assertEqual(r.returncode, 0)
        self.assertIn("caminho-y", self.run_cli("anti-list").stdout)


class TestScan(Base):
    def test_sem_skills_instaladas(self):
        r = self.run_cli("scan", "qualquer coisa nova")
        self.assertIn("Nenhuma skill instalada", r.stdout)

    def test_absorb_quando_mesmo_job(self):
        self.make_skill("video-x", "analisa video do youtube com transcricao e veredito")
        r = self.run_cli("scan", "analisa video youtube transcricao",
                         "--goal", "40", "--mech", "30")
        self.assertIn("ABSORB", r.stdout)
        self.assertIn("video-x", r.stdout)

    def test_stub_ignorado_como_candidato(self):
        self.make_skill("quiz-novo", "gera quiz interativo de multipla escolha")
        self.make_skill("quiz-velho", "SUPERSEDIDA por `quiz-novo`. quiz interativo antigo.")
        r = self.run_cli("scan", "quiz interativo de perguntas")
        self.assertIn("quiz-novo", r.stdout)
        self.assertNotIn("quiz-velho", r.stdout)

    def test_sem_candidato_comparavel_nao_quebra(self):
        self.make_skill("so-stub", "SUPERSEDIDA por `outra`. dominio migrado.")
        r = self.run_cli("scan", "tema totalmente novo", "--goal", "0", "--mech", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Nenhum candidato comparavel", r.stdout)
        self.assertIn("SUPERSEDE", r.stdout)
        self.assertIn("nenhuma antiga para stubar", r.stdout)


class TestProbes(Base):
    def test_probe_passa_e_detecta_quebra(self):
        pasta = self.make_skill("mapas", "desenha mapa mental hierarquico de conceitos")
        self.run_cli("probe-add", "mapas", "--should", "desenha mapa mental de conceitos")
        self.run_cli("probe-add", "mapas", "--should-not", "cozinhar lasanha ao forno")
        r = self.run_cli("probe-run", "mapas")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("Todos os probes passaram", r.stdout)
        # quebra o gatilho: descricao perde os termos
        (pasta / "SKILL.md").write_text(
            FRONT.format(n="mapas", d="outra coisa totalmente diferente"),
            encoding="utf-8")
        r = self.run_cli("probe-run", "mapas")
        self.assertEqual(r.returncode, 1)
        self.assertIn("FALHA", r.stdout)

    def test_probe_detecta_colisao(self):
        self.make_skill("a-skill", "processa video do youtube com transcricao completa")
        self.make_skill("b-skill", "processa video do youtube com transcricao completa")
        self.run_cli("probe-add", "a-skill", "--should", "processa video do youtube")
        r = self.run_cli("probe-run", "a-skill")
        self.assertEqual(r.returncode, 1)
        self.assertIn("COLISAO", r.stdout)


class TestCiclo(Base):
    def test_cota_mensal_bloqueia_segunda_nova(self):
        p1 = self.make_skill("nova-1", "primeira skill de teste com descricao")
        r = self.run_cli("commit", str(p1), "--decisao", "supersede",
                         "--novelty", "90", "--nota", "n1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("v1.0.0", r.stdout)
        p2 = self.make_skill("nova-2", "segunda skill de teste com descricao")
        r = self.run_cli("commit", str(p2), "--decisao", "supersede",
                         "--novelty", "88", "--nota", "n2")
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOQUEADO", r.stderr)

    def test_teto_ajustavel_por_ambiente(self):
        env = {"COMPOUND_TETO_NOVAS_MES": "2"}
        for i in (1, 2):
            p = self.make_skill(f"amb-{i}", f"skill ambiente {i} com descricao propria")
            r = self.run_cli("commit", str(p), "--decisao", "supersede",
                             "--novelty", "80", "--nota", "n", env_extra=env)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_orcamento_bloqueia_commit(self):
        self.make_skill("ocupa", "descricao longa que consome todo o orcamento disponivel")
        p = self.make_skill("nova-x", "outra")
        r = self.run_cli("commit", str(p), "--decisao", "supersede",
                         "--novelty", "85", "--nota", "n",
                         env_extra={"COMPOUND_BUDGET_CHARS": "10"})
        self.assertEqual(r.returncode, 3)
        self.assertIn("orcamento", r.stderr)

    def test_stub_e_bloqueio_de_protegida(self):
        self.make_skill("velha", "dominio antigo de organizacao de notas")
        self.run_cli("protect", "add", "velha")
        r = self.run_cli("stub", "velha", "nova", "--motivo", "novelty 80%")
        self.assertEqual(r.returncode, 2)
        self.run_cli("protect", "remove", "velha")
        r = self.run_cli("stub", "velha", "nova", "--motivo", "novelty 80%")
        self.assertEqual(r.returncode, 0, r.stderr)
        texto = (self.root / "velha" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("SUPERSEDIDA por `nova`", texto)

    def test_use_e_review(self):
        self.run_cli("use", "qualquer")
        r = self.run_cli("use", "qualquer")
        self.assertIn("2 uso(s)", r.stdout)
        self.assertIn("Nenhuma skill vencida", self.run_cli("review-due").stdout)


class TestSeguranca(Base):
    def test_backup_diff_rollback(self):
        pasta = self.make_skill("seg", "descricao original do gatilho")
        self.assertEqual(self.run_cli("backup", str(pasta)).returncode, 0)
        (pasta / "SKILL.md").write_text(
            FRONT.format(n="seg", d="descricao editada e diferente"), encoding="utf-8")
        r = self.run_cli("diff", str(pasta))
        self.assertIn("DESCRICAO MUDOU", r.stdout)
        self.assertEqual(self.run_cli("rollback", "seg").returncode, 0)
        texto = (self.root / "seg" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("descricao original", texto)

    def test_archive_move_e_e_reversivel(self):
        self.make_skill("efemera", "vive pouco")
        r = self.run_cli("archive", "efemera")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.root / "efemera").exists())
        arq = self.home / ".compound-skills" / "arquivadas"
        self.assertTrue(any(d.name.startswith("efemera__") for d in arq.iterdir()))

    def test_state_nao_depende_de_tmp_fixo(self):
        base = self.home / ".compound-skills"
        base.mkdir()
        (base / "state.json.tmp").mkdir()
        r = self.run_cli("status")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((base / "state.json").exists())


class TestSanitize(Base):
    def _pasta(self):
        p = self.home / "publicavel"
        p.mkdir()
        return p

    def test_detecta_token_e_cpf(self):
        p = self._pasta()
        (p / "vazado.md").write_text(
            "chave: ghp_" + "a" * 35 + "\ncliente 123.456.789-01\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)
        self.assertIn("GitHub", r.stdout)
        self.assertIn("CPF", r.stdout)

    def test_detecta_sk_com_hifens(self):
        p = self._pasta()
        (p / "a.txt").write_text("sk-ant-" + "b" * 24 + "\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)

    def test_marcador_do_usuario_por_ambiente(self):
        p = self._pasta()
        (p / "a.txt").write_text("nota com #interno no corpo\n", encoding="utf-8")
        self.assertEqual(self.run_cli("sanitize", str(p)).returncode, 0)
        r = self.run_cli("sanitize", str(p),
                         env_extra={"COMPOUND_MARCADORES": "#interno"})
        self.assertEqual(r.returncode, 1)
        self.assertIn("#interno", r.stdout)

    def test_supressoes_explicitas(self):
        p = self._pasta()
        (p / "ok.txt").write_text(
            "exemplo didatico ghp_" + "c" * 35 + "  sanitize-ok\n", encoding="utf-8")
        self.assertEqual(self.run_cli("sanitize", str(p)).returncode, 0)
        (p / ".sanitizeignore").write_text("sub/*\n", encoding="utf-8")
        sub = p / "sub"
        sub.mkdir()
        (sub / "fixture.txt").write_text("ghp_" + "d" * 35 + "\n", encoding="utf-8")
        self.assertEqual(self.run_cli("sanitize", str(p)).returncode, 0)

    def test_caminho_pessoal_absoluto(self):
        p = self._pasta()
        (p / "a.txt").write_text(f"log em {self.home}/x.txt\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)
        self.assertIn("path pessoal", r.stdout)

    def test_nao_imprime_literal_segredo_ou_prefixo(self):
        """Teste TDD para fix 1: nunca imprimir valor literal ou prefixo sensivel."""
        p = self._pasta()
        segredo = "ghp_" + "a" * 35
        (p / "vazado.md").write_text(f"token: {segredo}\ncpf: 123.456.789-01\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)
        out = (r.stdout or "") + (r.stderr or "")
        # literal completo e prefixo nao devem aparecer
        self.assertNotIn(segredo, out)
        self.assertNotIn("ghp_aaaaaaaa", out)
        self.assertNotIn("123.456.789-01", out)
        # mas deve detectar e reportar tipo/caminho/linha sem valor
        self.assertIn("[SEGREDO]", out)
        self.assertIn("vazado.md:1", out)
        self.assertIn("GitHub", out)
        self.assertIn("[PII/RESTRITO]", out)
        self.assertIn("vazado.md:2", out)
        self.assertIn("CPF", out)

    def test_detecta_authorization_bearer_sem_revelar_valor(self):
        p = self._pasta()
        valor = "Bearer " + "Z" * 32
        (p / "headers.txt").write_text(
            "AUTHORIZATION   :   " + valor + "\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)
        out = (r.stdout or "") + (r.stderr or "")
        self.assertIn("Bearer", out)
        self.assertNotIn(valor, out)
        self.assertNotIn("ZZZZZZZZ", out)

    def test_ignora_bearer_curto_ou_sem_token(self):
        p = self._pasta()
        (p / "headers.txt").write_text(
            "Authorization: Bearer curto\nAuthorization: Bearer\n",
            encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 0, r.stdout)


class TestPublicacao22(Base):
    def test_versao_e_claims_sao_coerentes(self):
        codigo = SCRIPT.read_text(encoding="utf-8")
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        portable = (REPO / "portable" / "PASTE-ANY-AI.md").read_text(encoding="utf-8")
        self.assertIn('VERSION = "2.2.0"', codigo)
        self.assertIn("portões aplicados por código", readme.lower())
        self.assertIn("portões operacionais", skill.lower())
        self.assertIn("versão degradada", portable.lower())

    def test_urls_publicas_nao_tem_placeholders(self):
        textos = "\n".join(
            p.read_text(encoding="utf-8")
            for p in REPO.rglob("*.md")
        )
        self.assertNotIn("SEU-USUARIO", textos)
        self.assertNotIn("<voce>", textos)
        self.assertIn("https://github.com/FLSDF79/compound-skills.git", textos)

    def test_actions_fixadas_por_sha_verificado(self):
        ci = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("actions/checkout@11d5960a326750d5838078e36cf38b85af677262", ci)
        self.assertIn("actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065", ci)


class TestDogfood(Base):
    """O repositorio publicado passa no proprio detector de vazamento."""

    def test_skill_passa_no_proprio_sanitize(self):
        r = self.run_cli("sanitize", str(SKILL_DIR))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_repo_inteiro_passa_no_sanitize(self):
        r = self.run_cli("sanitize", str(REPO))
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()


class TestMerge21(Base):
    """Correções da revisão 2.1.0: adoção, teto diário, FRIO, stub, ledger."""

    def test_adocao_nao_consome_cota(self):
        pre = self.make_skill("pre-existente", "skill que ja vivia no disco antes do motor")
        r = self.run_cli("commit", str(pre), "--decisao", "absorb",
                         "--novelty", "10", "--nota", "adocao")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ADOTADA", r.stdout)
        nova = self.make_skill("genuinamente-nova", "dominio inedito sem paralelo")
        r = self.run_cli("commit", str(nova), "--decisao", "supersede",
                         "--novelty", "90", "--nota", "criacao")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("CONSUMIDA", r.stdout)

    def test_teto_de_edicoes_por_dia_bloqueia(self):
        a = self.make_skill("alfa", "primeira skill do dia")
        b = self.make_skill("beta", "segunda skill do dia")
        c = self.make_skill("gama", "terceira skill do dia")
        for pasta in (a, b):
            r = self.run_cli("commit", str(pasta), "--decisao", "absorb",
                             "--novelty", "5", "--nota", "x")
            self.assertEqual(r.returncode, 0, r.stderr)
        r = self.run_cli("commit", str(c), "--decisao", "absorb",
                         "--novelty", "5", "--nota", "x")
        self.assertEqual(r.returncode, 4)
        self.assertIn("BLOQUEADO", r.stderr)

    def test_teto_de_edicoes_ajustavel(self):
        env = {"COMPOUND_TETO_EDICOES_DIA": "3"}
        for i in range(3):
            p = self.make_skill(f"sk-{i}", f"skill numero {i} com descricao propria")
            r = self.run_cli("commit", str(p), "--decisao", "absorb",
                             "--novelty", "5", "--nota", "x", env_extra=env)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_ledger_frio_dispara(self):
        home = self.home / ".compound-skills"
        home.mkdir(parents=True, exist_ok=True)
        (home / "ledger.md").write_text(
            "# Ledger\n\n## padrao esquecido\n- [2024-01-01] uma vez so\n",
            encoding="utf-8")
        r = self.run_cli("ledger-list")
        self.assertIn("FRIO", r.stdout)

    def test_ledger_titulo_malicioso_nao_corrompe(self):
        self.run_cli("ledger-add", "padrao x\n## bloco-injetado", "--contexto", "a\nb")
        r = self.run_cli("ledger-list")
        self.assertIn("padrao x ## bloco-injetado", r.stdout)
        self.assertNotIn("\n## bloco-injetado", r.stdout.replace("padrao x ## bloco-injetado", ""))

    def test_stub_faz_backup_automatico(self):
        self.make_skill("condenada", "dominio que sera supersedido")
        r = self.run_cli("stub", "condenada", "vencedora", "--motivo", "novelty 90%")
        self.assertEqual(r.returncode, 0, r.stderr)
        backups = self.home / ".compound-skills" / "backups"
        self.assertTrue(any(d.name.startswith("condenada__") for d in backups.iterdir()))

    def test_commit_exige_skillmd_e_novelty_valido(self):
        r = self.run_cli("commit", str(self.root / "nao-existe"),
                         "--decisao", "absorb", "--novelty", "10", "--nota", "x")
        self.assertEqual(r.returncode, 1)
        p = self.make_skill("valida", "descricao qualquer")
        r = self.run_cli("commit", str(p), "--decisao", "absorb",
                         "--novelty", "500", "--nota", "x")
        self.assertNotEqual(r.returncode, 0)

    def test_sanitize_detecta_token_telegram(self):
        p = self.home / "pub"
        p.mkdir()
        (p / "a.txt").write_text(
            "bot: 123456789:AA" + "h" * 33 + "\n", encoding="utf-8")
        r = self.run_cli("sanitize", str(p))
        self.assertEqual(r.returncode, 1)
        self.assertIn("Telegram", r.stdout)
