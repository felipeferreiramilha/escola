import streamlit as st
import pandas as pd
from datetime import date

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Sistema Escolar 2027",
    page_icon="🏫",
    layout="wide"
)

# ============================================================
# BANCO DE DADOS
# ============================================================
if "chamadas" not in st.session_state:
    st.session_state.chamadas = []
if "turmas" not in st.session_state:
    st.session_state.turmas = []
# ============================================================
# LIXEIRAS
# ============================================================

if "professores_lixeira" not in st.session_state:
    st.session_state.professores_lixeira = []

if "alunos_lixeira" not in st.session_state:
    st.session_state.alunos_lixeira = []

if "notas_lixeira" not in st.session_state:
    st.session_state.notas_lixeira = []

if "chamadas_lixeira" not in st.session_state:
    st.session_state.chamadas_lixeira = []
if "disciplinas" not in st.session_state:
    st.session_state.disciplinas = []

if "professores" not in st.session_state:
    st.session_state.professores = []

if "alunos" not in st.session_state:
    st.session_state.alunos = []

if "notas" not in st.session_state:
    st.session_state.notas = []

if "chamadas" not in st.session_state:
    st.session_state.chamadas = []


# ============================================================
# FUNÇÕES
# ============================================================

def calcular_media(n1, n2, n3, n4):
    return round((n1 + n2 + n3 + n4) / 4, 2)


def situacao(media):
    if media >= 6:
        return "Aprovado"
    elif media >= 4:
        return "Recuperação"
    else:
        return "Reprovado"


def calcular_faltas(aluno, turma, disciplina=None):
    faltas = 0

    for chamada in st.session_state.chamadas:

        if (
            chamada["aluno"] == aluno
            and chamada["turma"] == turma
            and chamada["presenca"] == "Falta"
        ):

            if disciplina is None or chamada["disciplina"] == disciplina:
                faltas += 1

    return faltas


def calcular_aulas(aluno, turma, disciplina=None):
    total = 0

    for chamada in st.session_state.chamadas:

        if (
            chamada["aluno"] == aluno
            and chamada["turma"] == turma
        ):

            if disciplina is None or chamada["disciplina"] == disciplina:
                total += 1

    return total


def calcular_frequencia(aluno, turma, disciplina=None):

    total = calcular_aulas(
        aluno,
        turma,
        disciplina
    )

    faltas = calcular_faltas(
        aluno,
        turma,
        disciplina
    )

    if total == 0:
        return 100.0

    presentes = total - faltas

    return round(
        (presentes / total) * 100,
        2
    )


# ============================================================
# TÍTULO
# ============================================================

st.title("🏫 SISTEMA DE GESTÃO ESCOLAR - 2027")

st.markdown(
    "### Cadastro de professores, alunos, notas e frequência"
)


# ============================================================
# ABAS
# ============================================================

abas = st.tabs([
    "🏫 Turmas e Disciplinas",
    "👨‍🏫 Professores",
    "👨‍🎓 Alunos",
    "📝 Notas",
    "📅 Chamada 2027",
    "📊 Relatórios",
    "👨‍🏫 Área do Professor"
])


# ============================================================
# ABA 1 - TURMAS E DISCIPLINAS
# ============================================================

with abas[0]:

    st.header("🏫 Cadastro de Turmas")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("➕ Nova turma")

        nome_turma = st.text_input(
            "Nome da turma",
            placeholder="Ex.: 1º Ano A",
            key="nova_turma"
        )

        if st.button(
            "Cadastrar Turma",
            key="btn_cadastrar_turma"
        ):

            if nome_turma.strip() == "":
                st.warning("Digite o nome da turma.")

            elif nome_turma in st.session_state.turmas:
                st.warning("Essa turma já existe.")

            else:

                st.session_state.turmas.append(
                    nome_turma
                )

                st.success(
                    "Turma cadastrada com sucesso!"
                )

                st.rerun()

    with col2:

        st.subheader("🗑️ Excluir turma")

        if st.session_state.turmas:

            turma_excluir = st.selectbox(
                "Selecione a turma",
                st.session_state.turmas,
                key="excluir_turma"
            )

            if st.button(
                "Excluir Turma",
                key="btn_excluir_turma"
            ):

                st.session_state.turmas.remove(
                    turma_excluir
                )

                st.session_state.alunos = [
                    aluno
                    for aluno in st.session_state.alunos
                    if aluno["turma"] != turma_excluir
                ]

                st.success(
                    "Turma excluída!"
                )

                st.rerun()

        else:

            st.info(
                "Nenhuma turma cadastrada."
            )

    st.divider()

    # --------------------------------------------------------
    # DISCIPLINAS
    # --------------------------------------------------------

    st.header("📚 Cadastro de Disciplinas")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("➕ Nova disciplina")

        nome_disciplina = st.text_input(
            "Nome da disciplina",
            placeholder="Ex.: Física",
            key="nova_disciplina"
        )

        if st.button(
            "Cadastrar Disciplina",
            key="btn_cadastrar_disciplina"
        ):

            if nome_disciplina.strip() == "":
                st.warning(
                    "Digite o nome da disciplina."
                )

            elif nome_disciplina in st.session_state.disciplinas:

                st.warning(
                    "Essa disciplina já existe."
                )

            else:

                st.session_state.disciplinas.append(
                    nome_disciplina
                )

                st.success(
                    "Disciplina cadastrada!"
                )

                st.rerun()

    with col2:

        st.subheader("🗑️ Excluir disciplina")

        if st.session_state.disciplinas:

            disciplina_excluir = st.selectbox(
                "Selecione a disciplina",
                st.session_state.disciplinas,
                key="excluir_disciplina"
            )

            if st.button(
                "Excluir Disciplina",
                key="btn_excluir_disciplina"
            ):

                st.session_state.disciplinas.remove(
                    disciplina_excluir
                )

                st.success(
                    "Disciplina excluída!"
                )

                st.rerun()

        else:

            st.info(
                "Nenhuma disciplina cadastrada."
            )

    st.divider()

    st.subheader("📋 Turmas cadastradas")

    if st.session_state.turmas:

        for turma in st.session_state.turmas:
            st.write(
                f"🏫 {turma}"
            )

    else:

        st.info(
            "Nenhuma turma cadastrada."
        )

    st.subheader("📚 Disciplinas cadastradas")

    if st.session_state.disciplinas:

        for disciplina in st.session_state.disciplinas:
            st.write(
                f"📚 {disciplina}"
            )

    else:

        st.info(
            "Nenhuma disciplina cadastrada."
        )


# ============================================================
# ABA 2 - PROFESSORES
# ============================================================

with abas[1]:

    st.header("👨‍🏫 Cadastro de Professores")

    st.success(
        "O professor é cadastrado automaticamente como ATIVO. "
        "Não é necessário aprovação."
    )

    if not st.session_state.disciplinas:

        st.warning(
            "Cadastre pelo menos uma disciplina primeiro."
        )

    else:

        nome_professor = st.text_input(
            "Nome completo do professor",
            placeholder="Digite o nome do professor",
            key="nome_professor"
        )

        disciplinas_professor = st.multiselect(
            "Disciplinas que o professor leciona",
            st.session_state.disciplinas,
            key="disciplinas_professor"
        )

        if st.button(
            "➕ Cadastrar Professor",
            key="btn_cadastrar_professor"
        ):

            if nome_professor.strip() == "":

                st.warning(
                    "Digite o nome do professor."
                )

            elif not disciplinas_professor:

                st.warning(
                    "Selecione pelo menos uma disciplina."
                )

            else:

                existe = any(
                    p["nome"].lower() == nome_professor.lower()
                    for p in st.session_state.professores
                )

                if existe:

                    st.warning(
                        "Esse professor já está cadastrado."
                    )

                else:

                    st.session_state.professores.append({
                        "nome": nome_professor,
                        "disciplinas": disciplinas_professor,
                        "status": "Ativo"
                    })

                    st.success(
                        "Professor cadastrado com sucesso! "
                        "Ele já está ativo."
                    )

                    st.rerun()

    st.divider()

    st.header("📋 Professores cadastrados")

    if not st.session_state.professores:

        st.info(
            "Nenhum professor cadastrado."
        )

    else:

        for i, professor in enumerate(
            st.session_state.professores
        ):

            st.container()

            st.subheader(
                f"👨‍🏫 {professor['nome']}"
            )

            st.write(
                "**Disciplinas:** "
                + ", ".join(
                    professor["disciplinas"]
                )
            )

            st.success(
                "🟢 Professor Ativo"
            )

            if st.button(
                "🗑️ Excluir Professor",
                key=f"excluir_professor_{i}"
            ):

                nome_excluido = professor["nome"]

                st.session_state.professores.pop(i)

                st.success(
                    f"Professor {nome_excluido} excluído."
                )

                st.rerun()

            st.divider()


# ============================================================
# ABA 3 - ALUNOS
# ============================================================

with abas[2]:

    st.header("👨‍🎓 Cadastro de Alunos")

    st.info(
        "Nesta área você pode cadastrar, visualizar e excluir alunos."
    )

    # --------------------------------------------------------
    # CADASTRO DO ALUNO
    # --------------------------------------------------------

    st.subheader("➕ Cadastrar novo aluno")

    if not st.session_state.turmas:

        st.warning(
            "Antes de cadastrar um aluno, cadastre uma turma "
            "na aba 'Turmas e Disciplinas'."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            nome_aluno = st.text_input(
                "Nome completo do aluno",
                placeholder="Digite o nome do aluno",
                key="nome_aluno"
            )

        with col2:

            turma_aluno = st.selectbox(
                "Selecione a turma",
                st.session_state.turmas,
                key="turma_aluno"
            )

        if st.button(
            "➕ Cadastrar Aluno",
            key="btn_cadastrar_aluno"
        ):

            if nome_aluno.strip() == "":

                st.warning(
                    "Digite o nome do aluno."
                )

            else:

                existe = any(
                    a["nome"].lower() == nome_aluno.lower()
                    and a["turma"] == turma_aluno
                    for a in st.session_state.alunos
                )

                if existe:

                    st.warning(
                        "Esse aluno já está cadastrado nessa turma."
                    )

                else:

                    st.session_state.alunos.append({
                        "nome": nome_aluno,
                        "turma": turma_aluno
                    })

                    st.success(
                        f"Aluno {nome_aluno} cadastrado com sucesso!"
                    )

                    st.rerun()

    st.divider()

    # --------------------------------------------------------
    # LISTA DE ALUNOS
    # --------------------------------------------------------

    st.header("📋 Alunos cadastrados")

    if not st.session_state.alunos:

        st.info(
            "Nenhum aluno cadastrado ainda."
        )

    else:

        dados_alunos = []

        for aluno in st.session_state.alunos:

            dados_alunos.append({
                "Aluno": aluno["nome"],
                "Turma": aluno["turma"]
            })

        st.dataframe(
            pd.DataFrame(dados_alunos),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗑️ Excluir aluno")

        aluno_excluir = st.selectbox(
            "Selecione o aluno que deseja excluir",
            [
                f"{a['nome']} — {a['turma']}"
                for a in st.session_state.alunos
            ],
            key="aluno_excluir"
        )

        if st.button(
            "🗑️ Excluir Aluno",
            key="btn_excluir_aluno"
        ):

            nome_excluir, turma_excluir = (
                aluno_excluir.split(
                    " — ",
                    1
                )
            )

            # Exclui o aluno
            st.session_state.alunos = [
                aluno
                for aluno in st.session_state.alunos
                if not (
                    aluno["nome"] == nome_excluir
                    and aluno["turma"] == turma_excluir
                )
            ]

            # Exclui as notas do aluno
            st.session_state.notas = [
                nota
                for nota in st.session_state.notas
                if not (
                    nota["aluno"] == nome_excluir
                    and nota["turma"] == turma_excluir
                )
            ]

            # Exclui as chamadas do aluno
            st.session_state.chamadas = [
                chamada
                for chamada in st.session_state.chamadas
                if not (
                    chamada["aluno"] == nome_excluir
                    and chamada["turma"] == turma_excluir
                )
            ]

            st.success(
                f"Aluno {nome_excluir} excluído com sucesso!"
            )

            st.rerun()


# ============================================================
# ABA 4 - NOTAS
# ============================================================

with abas[3]:

    st.header("📝 Lançamento das 4 Médias")

    if not st.session_state.alunos:

        st.warning(
            "Cadastre alunos primeiro."
        )

    elif not st.session_state.disciplinas:

        st.warning(
            "Cadastre disciplinas primeiro."
        )

    else:

        aluno_selecionado = st.selectbox(
            "Aluno",
            [
                f"{a['nome']} — {a['turma']}"
                for a in st.session_state.alunos
            ],
            key="aluno_notas"
        )

        aluno_nome, turma_nome = (
            aluno_selecionado.split(
                " — ",
                1
            )
        )

        disciplina_selecionada = st.selectbox(
            "Disciplina",
            st.session_state.disciplinas,
            key="disciplina_notas"
        )

        notas_existentes = None

        for registro in st.session_state.notas:

            if (
                registro["aluno"] == aluno_nome
                and registro["turma"] == turma_nome
                and registro["disciplina"] == disciplina_selecionada
            ):

                notas_existentes = registro

        valor_n1 = (
            notas_existentes["n1"]
            if notas_existentes
            else 0.0
        )

        valor_n2 = (
            notas_existentes["n2"]
            if notas_existentes
            else 0.0
        )

        valor_n3 = (
            notas_existentes["n3"]
            if notas_existentes
            else 0.0
        )

        valor_n4 = (
            notas_existentes["n4"]
            if notas_existentes
            else 0.0
        )

        st.subheader(
            "📚 Digite as quatro médias"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            n1 = st.number_input(
                "1ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n1),
                step=0.1,
                key=f"nota1_{aluno_nome}_{disciplina_selecionada}"
            )

        with col2:

            n2 = st.number_input(
                "2ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n2),
                step=0.1,
                key=f"nota2_{aluno_nome}_{disciplina_selecionada}"
            )

        with col3:

            n3 = st.number_input(
                "3ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n3),
                step=0.1,
                key=f"nota3_{aluno_nome}_{disciplina_selecionada}"
            )

        with col4:

            n4 = st.number_input(
                "4ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n4),
                step=0.1,
                key=f"nota4_{aluno_nome}_{disciplina_selecionada}"
            )

        media = calcular_media(
            n1,
            n2,
            n3,
            n4
        )

        resultado = situacao(
            media
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📊 Média Final",
                f"{media:.2f}"
            )

        with col2:

            st.metric(
                "📋 Situação",
                resultado
            )

        if media >= 7:

            st.success(
                "✅ Aluno aprovado."
            )

        elif media >= 4:

            st.warning(
                "⚠️ Aluno em recuperação."
            )

        else:

            st.error(
                "❌ Aluno reprovado."
            )

        if st.button(
            "💾 Salvar Notas",
            key="btn_salvar_notas"
        ):

            novo_registro = {
                "aluno": aluno_nome,
                "turma": turma_nome,
                "disciplina": disciplina_selecionada,
                "n1": n1,
                "n2": n2,
                "n3": n3,
                "n4": n4,
                "media": media,
                "situacao": resultado
            }

            encontrou = False

            for i, registro in enumerate(
                st.session_state.notas
            ):

                if (
                    registro["aluno"] == aluno_nome
                    and registro["turma"] == turma_nome
                    and registro["disciplina"] == disciplina_selecionada
                ):

                    st.session_state.notas[i] = novo_registro

                    encontrou = True

            if not encontrou:

                st.session_state.notas.append(
                    novo_registro
                )

            st.success(
                "Notas salvas com sucesso!"
            )

            st.rerun()


# ============================================================
# :

            # ==========================================
# LIXEIRA DAS CHAMADAS
# ==========================================

if "chamadas_lixeira" not in st.session_state:
    st.session_state.chamadas_lixeira = []
    # ============================================================
# 📅 CHAMADA 2027
# ============================================================

with tab5:

    st.header("📅 Chamada 2027")

    # ========================================================
    # FUNÇÃO PARA CALCULAR FALTAS
    # ========================================================

    def calcular_faltas_chamada(aluno_nome, turma=None, disciplina=None):

        faltas = 0

        for chamada in st.session_state.chamadas:

            if chamada["aluno"] != aluno_nome:
                continue

            if turma is not None and chamada["turma"] != turma:
                continue

            if disciplina is not None and chamada["disciplina"] != disciplina:
                continue

            if chamada["situacao"] == "Falta":
                faltas += 1

        return faltas


    # ========================================================
    # FUNÇÃO PARA CALCULAR AULAS
    # ========================================================

    def calcular_aulas_chamada(aluno_nome, turma=None, disciplina=None):

        total = 0

        for chamada in st.session_state.chamadas:

            if chamada["aluno"] != aluno_nome:
                continue

            if turma is not None and chamada["turma"] != turma:
                continue

            if disciplina is not None and chamada["disciplina"] != disciplina:
                continue

            total += 1

        return total


    # ========================================================
    # FUNÇÃO PARA CALCULAR FREQUÊNCIA
    # ========================================================

    def calcular_frequencia_chamada(aluno_nome, turma=None, disciplina=None):

        total = calcular_aulas_chamada(
            aluno_nome,
            turma,
            disciplina
        )

        faltas = calcular_faltas_chamada(
            aluno_nome,
            turma,
            disciplina
        )

        if total == 0:
            return 0

        presentes = total - faltas

        return (presentes / total) * 100


    # ========================================================
    # 1️⃣ LANÇAR NOVA CHAMADA
    # ========================================================

    st.subheader("➕ Lançar chamada")

    if not st.session_state.alunos:

        st.warning("Cadastre pelo menos um aluno antes de lançar a chamada.")

    elif not st.session_state.disciplinas:

        st.warning("Cadastre pelo menos uma disciplina antes de lançar a chamada.")

    else:

        col1, col2 = st.columns(2)

        with col1:

            data_chamada = st.date_input(
                "📅 Data da chamada",
                value=date.today(),
                min_value=date(2027, 1, 1),
                max_value=date(2027, 12, 31)
            )

        with col2:

            turmas_disponiveis = sorted(
                list(set(
                    aluno["turma"]
                    for aluno in st.session_state.alunos
                ))
            )

            turma_chamada = st.selectbox(
                "🏫 Turma",
                turmas_disponiveis
            )


        disciplinas_disponiveis = st.session_state.disciplinas

        disciplina_chamada = st.selectbox(
            "📚 Disciplina",
            disciplinas_disponiveis
        )


        # ----------------------------------------------------
        # ALUNOS DA TURMA
        # ----------------------------------------------------

        alunos_da_turma = [
            aluno["nome"]
            for aluno in st.session_state.alunos
            if aluno["turma"] == turma_chamada
        ]


        if not alunos_da_turma:

            st.warning(
                "Não existem alunos cadastrados nessa turma."
            )

        else:

            aluno_chamada = st.selectbox(
                "👨‍🎓 Aluno",
                sorted(alunos_da_turma)
            )


            situacao_chamada = st.radio(
                "Situação do aluno:",
                ["Presente", "Falta"],
                horizontal=True
            )


            if st.button(
                "💾 Registrar chamada",
                type="primary"
            ):

                data_texto = data_chamada.strftime("%d/%m/%Y")


                # ------------------------------------------------
                # VERIFICAR SE JÁ EXISTE CHAMADA
                # ------------------------------------------------

                chamada_existente = None
                indice_existente = None

                for i, chamada in enumerate(
                    st.session_state.chamadas
                ):

                    if (
                        chamada["aluno"] == aluno_chamada
                        and chamada["turma"] == turma_chamada
                        and chamada["disciplina"] == disciplina_chamada
                        and chamada["data"] == data_texto
                    ):

                        chamada_existente = chamada
                        indice_existente = i
                        break


                # ------------------------------------------------
                # SE JÁ EXISTIR, ATUALIZA
                # ------------------------------------------------

                if chamada_existente is not None:

                    st.session_state.chamadas[
                        indice_existente
                    ]["situacao"] = situacao_chamada

                    st.success(
                        "A chamada desse aluno nessa data já existia "
                        "e foi atualizada corretamente."
                    )

                    st.rerun()


                # ------------------------------------------------
                # SE NÃO EXISTIR, CRIA
                # ------------------------------------------------

                nova_chamada = {

                    "data": data_texto,

                    "aluno": aluno_chamada,

                    "turma": turma_chamada,

                    "disciplina": disciplina_chamada,

                    "situacao": situacao_chamada
                }


                st.session_state.chamadas.append(
                    nova_chamada
                )


                st.success(
                    f"Chamada registrada para {aluno_chamada}."
                )

                st.rerun()


    # ========================================================
    # 2️⃣ CORRIGIR CHAMADA
    # ========================================================

    st.divider()

    st.subheader("✏️ Corrigir chamada")

    if not st.session_state.chamadas:

        st.info(
            "Nenhuma chamada foi registrada ainda."
        )

    else:

        opcoes_chamadas = []

        for i, chamada in enumerate(
            st.session_state.chamadas
        ):

            texto = (
                f"{i} | "
                f"{chamada['data']} | "
                f"{chamada['aluno']} | "
                f"{chamada['turma']} | "
                f"{chamada['disciplina']} | "
                f"{chamada['situacao']}"
            )

            opcoes_chamadas.append(texto)


        chamada_selecionada = st.selectbox(
            "Selecione a chamada que deseja corrigir:",
            opcoes_chamadas,
            key="chamada_para_editar"
        )


        indice_edicao = int(
            chamada_selecionada.split(" | ")[0]
        )


        chamada_atual = st.session_state.chamadas[
            indice_edicao
        ]


        st.write(
            f"**Aluno:** {chamada_atual['aluno']}"
        )

        st.write(
            f"**Data:** {chamada_atual['data']}"
        )

        st.write(
            f"**Turma:** {chamada_atual['turma']}"
        )

        st.write(
            f"**Disciplina:** {chamada_atual['disciplina']}"
        )

        st.write(
            f"**Situação atual:** {chamada_atual['situacao']}"
        )


        nova_situacao = st.radio(
            "Nova situação:",
            ["Presente", "Falta"],
            index=(
                0
                if chamada_atual["situacao"] == "Presente"
                else 1
            ),
            horizontal=True,
            key="nova_situacao_edicao"
        )


        if st.button(
            "💾 Salvar correção",
            key="salvar_correcao"
        ):

            st.session_state.chamadas[
                indice_edicao
            ]["situacao"] = nova_situacao


            st.success(
                "Chamada corrigida com sucesso!"
            )

            st.rerun()


    # ========================================================
    # 3️⃣ EXCLUIR CHAMADA
    # ========================================================

    st.divider()

    st.subheader("🗑️ Excluir chamada")

    if not st.session_state.chamadas:

        st.info(
            "Não existem chamadas para excluir."
        )

    else:

        opcoes_exclusao = []

        for i, chamada in enumerate(
            st.session_state.chamadas
        ):

            texto = (
                f"{i} | "
                f"{chamada['data']} | "
                f"{chamada['aluno']} | "
                f"{chamada['turma']} | "
                f"{chamada['disciplina']} | "
                f"{chamada['situacao']}"
            )

            opcoes_exclusao.append(texto)


        chamada_excluir = st.selectbox(
            "Selecione a chamada que deseja excluir:",
            opcoes_exclusao,
            key="chamada_para_excluir"
        )


        indice_exclusao = int(
            chamada_excluir.split(" | ")[0]
        )


        chamada_selecionada_exclusao = (
            st.session_state.chamadas[
                indice_exclusao
            ]
        )


        st.warning(
            "A chamada será enviada para a Lixeira. "
            "Ela poderá ser restaurada posteriormente."
        )


        if st.button(
            "🗑️ Enviar chamada para a Lixeira",
            key="enviar_chamada_lixeira"
        ):

            chamada_removida = (
                st.session_state.chamadas.pop(
                    indice_exclusao
                )
            )


            st.session_state.chamadas_lixeira.append(
                chamada_removida
            )


            st.success(
                "Chamada enviada para a Lixeira."
            )

            st.rerun()


    # ========================================================
    # 4️⃣ CONSULTAR CHAMADAS
    # ========================================================

    st.divider()

    st.subheader("📋 Chamadas registradas")

    if st.session_state.chamadas:

        df_chamadas = pd.DataFrame(
            st.session_state.chamadas
        )


        # ----------------------------------------------------
        # FILTROS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            filtro_turma = st.selectbox(
                "Filtrar por turma:",
                ["Todas"] + sorted(
                    list(
                        set(
                            c["turma"]
                            for c in st.session_state.chamadas
                        )
                    )
                ),
                key="filtro_turma_chamada"
            )


        with col2:

            filtro_disciplina = st.selectbox(
                "Filtrar por disciplina:",
                ["Todas"] + sorted(
                    list(
                        set(
                            c["disciplina"]
                            for c in st.session_state.chamadas
                        )
                    )
                ),
                key="filtro_disciplina_chamada"
            )


        with col3:

            filtro_aluno = st.selectbox(
                "Filtrar por aluno:",
                ["Todos"] + sorted(
                    list(
                        set(
                            c["aluno"]
                            for c in st.session_state.chamadas
                        )
                    )
                ),
                key="filtro_aluno_chamada"
            )


        df_filtrado = df_chamadas.copy()


        if filtro_turma != "Todas":

            df_filtrado = df_filtrado[
                df_filtrado["turma"] == filtro_turma
            ]


        if filtro_disciplina != "Todas":

            df_filtrado = df_filtrado[
                df_filtrado["disciplina"]
                == filtro_disciplina
            ]


        if filtro_aluno != "Todos":

            df_filtrado = df_filtrado[
                df_filtrado["aluno"]
                == filtro_aluno
            ]


        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "Nenhuma chamada registrada."
        )


    # ========================================================
    # 5️⃣ RESUMO DE FREQUÊNCIA
    # ========================================================

    st.divider()

    st.subheader("📊 Resumo de frequência")


    if st.session_state.alunos:

        resumo = []


        for aluno in st.session_state.alunos:

            nome = aluno["nome"]
            turma = aluno["turma"]


            total_aulas = calcular_aulas_chamada(
                nome,
                turma
            )


            faltas = calcular_faltas_chamada(
                nome,
                turma
            )


            frequencia = calcular_frequencia_chamada(
                nome,
                turma
            )


            resumo.append({

                "Aluno": nome,

                "Turma": turma,

                "Total de aulas": total_aulas,

                "Faltas": faltas,

                "Presenças": total_aulas - faltas,

                "Frequência (%)": round(
                    frequencia,
                    2
                )
            })


        df_resumo = pd.DataFrame(
            resumo
        )


        st.dataframe(
            df_resumo,
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        csv_chamada = df_resumo.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "⬇️ Baixar resumo de frequência",
            data=csv_chamada,
            file_name="frequencia_2027.csv",
            mime="text/csv"
        )


    else:

        st.info(
            "Cadastre alunos para visualizar a frequência."
        )
# ============================================================
# ABA 6 - RELATÓRIOS
# ============================================================

with abas[5]:

    st.header("📊 Relatórios Escolares")

    if not st.session_state.alunos:

        st.info(
            "Nenhum aluno cadastrado."
        )

    else:

        dados_relatorio = []

        for aluno in st.session_state.alunos:

            nome = aluno["nome"]
            turma = aluno["turma"]

            registros_aluno = [
                nota
                for nota in st.session_state.notas
                if (
                    nota["aluno"] == nome
                    and nota["turma"] == turma
                )
            ]

            for registro in registros_aluno:

                faltas = calcular_faltas(
                    nome,
                    turma,
                    registro["disciplina"]
                )

                frequencia = calcular_frequencia(
                    nome,
                    turma,
                    registro["disciplina"]
                )

                dados_relatorio.append({
                    "Aluno": nome,
                    "Turma": turma,
                    "Disciplina": registro["disciplina"],
                    "1ª Média": registro["n1"],
                    "2ª Média": registro["n2"],
                    "3ª Média": registro["n3"],
                    "4ª Média": registro["n4"],
                    "Média Final": registro["media"],
                    "Situação": registro["situacao"],
                    "Faltas": faltas,
                    "Frequência (%)": frequencia
                })

        if dados_relatorio:

            df = pd.DataFrame(
                dados_relatorio
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Baixar Relatório CSV",
                data=csv,
                file_name="relatorio_escolar_2027.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "Ainda não existem notas lançadas."
            )

    st.divider()

    st.header("👨‍🎓 Relatório Individual")

    if st.session_state.alunos:

        aluno_relatorio = st.selectbox(
            "Selecione o aluno",
            [
                f"{a['nome']} — {a['turma']}"
                for a in st.session_state.alunos
            ],
            key="aluno_relatorio"
        )

        nome_relatorio, turma_relatorio = (
            aluno_relatorio.split(
                " — ",
                1
            )
        )

        st.subheader(
            f"👨‍🎓 {nome_relatorio}"
        )

        st.write(
            f"**Turma:** {turma_relatorio}"
        )

        registros = [
            nota
            for nota in st.session_state.notas
            if (
                nota["aluno"] == nome_relatorio
                and nota["turma"] == turma_relatorio
            )
        ]

        if registros:

            for registro in registros:

                faltas = calcular_faltas(
                    nome_relatorio,
                    turma_relatorio,
                    registro["disciplina"]
                )

                frequencia = calcular_frequencia(
                    nome_relatorio,
                    turma_relatorio,
                    registro["disciplina"]
                )

                st.write(
                    f"### 📚 {registro['disciplina']}"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Média",
                        f"{registro['media']:.2f}"
                    )

                with col2:

                    st.metric(
                        "Situação",
                        registro["situacao"]
                    )

                with col3:

                    st.metric(
                        "Faltas",
                        faltas
                    )

                with col4:

                    st.metric(
                        "Frequência",
                        f"{frequencia}%"
                    )

                st.divider()

        else:

            st.info(
                "Esse aluno ainda não possui notas."
            )


# ============================================================
# ABA 7 - ÁREA DO PROFESSOR
# ============================================================

with abas[6]:

    st.header("👨‍🏫 Área do Professor")

    professores_ativos = [
        professor
        for professor in st.session_state.professores
        if professor["status"] == "Ativo"
    ]

    if not professores_ativos:

        st.warning(
            "Nenhum professor cadastrado."
        )

    else:

        professor_area = st.selectbox(
            "Selecione o professor",
            [
                professor["nome"]
                for professor in professores_ativos
            ],
            key="professor_area"
        )

        professor_obj = next(
            professor
            for professor in professores_ativos
            if professor["nome"] == professor_area
        )

        st.success(
            f"🟢 Professor ativo: {professor_area}"
        )

        disciplina_area = st.selectbox(
            "Selecione a disciplina",
            professor_obj["disciplinas"],
            key="disciplina_area"
        )

        st.info(
            f"Disciplina: {disciplina_area}"
        )

        registros_professor = [
            nota
            for nota in st.session_state.notas
            if nota["disciplina"] == disciplina_area
        ]

        if registros_professor:

            dados_professor = []

            for registro in registros_professor:

                faltas = calcular_faltas(
                    registro["aluno"],
                    registro["turma"],
                    disciplina_area
                )

                frequencia = calcular_frequencia(
                    registro["aluno"],
                    registro["turma"],
                    disciplina_area
                )

                dados_professor.append({
                    "Aluno": registro["aluno"],
                    "Turma": registro["turma"],
                    "1ª Média": registro["n1"],
                    "2ª Média": registro["n2"],
                    "3ª Média": registro["n3"],
                    "4ª Média": registro["n4"],
                    "Média Final": registro["media"],
                    "Situação": registro["situacao"],
                    "Faltas": faltas,
                    "Frequência (%)": frequencia
                })

            st.dataframe(
                pd.DataFrame(
                    dados_professor
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhuma nota lançada para essa disciplina."
            )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🏫 Sistema Escolar 2027 • "
    "Alunos • Professores • Notas • Frequência • Chamada"
)
            
