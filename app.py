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
# BANCO DE DADOS TEMPORÁRIO
# ============================================================

if "turmas" not in st.session_state:
    st.session_state.turmas = []

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
    if media >= 7:
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
    total = calcular_aulas(aluno, turma, disciplina)
    faltas = calcular_faltas(aluno, turma, disciplina)

    if total == 0:
        return 100.0

    presentes = total - faltas

    return round((presentes / total) * 100, 2)


# ============================================================
# TÍTULO
# ============================================================

st.title("🏫 SISTEMA DE GESTÃO ESCOLAR - 2027")
st.markdown("### Cadastro de professores, alunos, notas e chamada")


# ============================================================
# MENU
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

        nome_turma = st.text_input(
            "Nome da turma",
            key="nova_turma"
        )

        if st.button("Cadastrar Turma"):

            if nome_turma.strip() == "":
                st.warning("Digite o nome da turma.")

            elif nome_turma in st.session_state.turmas:
                st.warning("Essa turma já existe.")

            else:
                st.session_state.turmas.append(nome_turma)
                st.success("Turma cadastrada!")
                st.rerun()

    with col2:

        if st.session_state.turmas:

            turma_excluir = st.selectbox(
                "Excluir turma",
                st.session_state.turmas,
                key="excluir_turma"
            )

            if st.button("Excluir Turma"):

                st.session_state.turmas.remove(turma_excluir)

                st.session_state.alunos = [
                    a for a in st.session_state.alunos
                    if a["turma"] != turma_excluir
                ]

                st.success("Turma excluída!")
                st.rerun()

    st.divider()

    st.header("📚 Cadastro de Disciplinas")

    col1, col2 = st.columns(2)

    with col1:

        nome_disciplina = st.text_input(
            "Nome da disciplina",
            key="nova_disciplina"
        )

        if st.button("Cadastrar Disciplina"):

            if nome_disciplina.strip() == "":
                st.warning("Digite o nome da disciplina.")

            elif nome_disciplina in st.session_state.disciplinas:
                st.warning("Essa disciplina já existe.")

            else:
                st.session_state.disciplinas.append(nome_disciplina)
                st.success("Disciplina cadastrada!")
                st.rerun()

    with col2:

        if st.session_state.disciplinas:

            disciplina_excluir = st.selectbox(
                "Excluir disciplina",
                st.session_state.disciplinas,
                key="excluir_disciplina"
            )

            if st.button("Excluir Disciplina"):

                st.session_state.disciplinas.remove(
                    disciplina_excluir
                )

                st.success("Disciplina excluída!")
                st.rerun()

    st.divider()

    st.subheader("Turmas cadastradas")

    if st.session_state.turmas:
        for turma in st.session_state.turmas:
            st.write("•", turma)
    else:
        st.info("Nenhuma turma cadastrada.")

    st.subheader("Disciplinas cadastradas")

    if st.session_state.disciplinas:
        for disciplina in st.session_state.disciplinas:
            st.write("•", disciplina)
    else:
        st.info("Nenhuma disciplina cadastrada.")


# ============================================================
# ABA 2 - PROFESSORES
# ============================================================

with abas[1]:

    st.header("👨‍🏫 Cadastro de Professores")

    if not st.session_state.disciplinas:
        st.warning(
            "Cadastre pelo menos uma disciplina antes de cadastrar professores."
        )

    else:

        nome_professor = st.text_input(
            "Nome do professor",
            key="nome_professor"
        )

        disciplinas_professor = st.multiselect(
            "Disciplinas do professor",
            st.session_state.disciplinas,
            key="disciplinas_professor"
        )

        if st.button("Cadastrar Professor"):

            if nome_professor.strip() == "":
                st.warning("Digite o nome do professor.")

            elif not disciplinas_professor:
                st.warning("Selecione pelo menos uma disciplina.")

            else:

                existe = any(
                    p["nome"] == nome_professor
                    for p in st.session_state.professores
                )

                if existe:
                    st.warning("Professor já cadastrado.")

                else:

                    st.session_state.professores.append({
                        "nome": nome_professor,
                        "disciplinas": disciplinas_professor,
                        "status": "Pendente"
                    })

                    st.success(
                        "Professor cadastrado e aguardando aprovação."
                    )

                    st.rerun()

    st.divider()

    st.header("📋 Professores cadastrados")

    if not st.session_state.professores:

        st.info("Nenhum professor cadastrado.")

    else:

        for i, professor in enumerate(
            st.session_state.professores
        ):

            with st.container():

                st.write(
                    f"### 👨‍🏫 {professor['nome']}"
                )

                st.write(
                    "**Disciplinas:** "
                    + ", ".join(professor["disciplinas"])
                )

                st.write(
                    f"**Status:** {professor['status']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if professor["status"] == "Pendente":

                        if st.button(
                            "✅ Aprovar Professor",
                            key=f"aprovar_{i}"
                        ):

                            st.session_state.professores[i][
                                "status"
                            ] = "Aprovado"

                            st.success(
                                "Professor aprovado!"
                            )

                            st.rerun()

                    else:

                        st.success("Professor aprovado.")

                with col2:

                    if st.button(
                        "🗑️ Excluir Professor",
                        key=f"excluir_professor_{i}"
                    ):

                        st.session_state.professores.pop(i)

                        st.success(
                            "Professor excluído."
                        )

                        st.rerun()

                st.divider()


# ============================================================
# ABA 3 - ALUNOS
# ============================================================

with abas[2]:

    st.header("👨‍🎓 Cadastro de Alunos")

    if not st.session_state.turmas:

        st.warning("Cadastre uma turma primeiro.")

    else:

        nome_aluno = st.text_input(
            "Nome completo do aluno",
            key="nome_aluno"
        )

        turma_aluno = st.selectbox(
            "Turma",
            st.session_state.turmas,
            key="turma_aluno"
        )

        if st.button("Cadastrar Aluno"):

            if nome_aluno.strip() == "":
                st.warning("Digite o nome do aluno.")

            else:

                existe = any(
                    a["nome"] == nome_aluno
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
                        "Aluno cadastrado!"
                    )

                    st.rerun()

    st.divider()

    st.header("📋 Alunos cadastrados")

    if not st.session_state.alunos:

        st.info("Nenhum aluno cadastrado.")

    else:

        for i, aluno in enumerate(
            st.session_state.alunos
        ):

            col1, col2, col3 = st.columns([4, 3, 1])

            with col1:
                st.write(
                    f"👨‍🎓 **{aluno['nome']}**"
                )

            with col2:
                st.write(
                    f"Turma: **{aluno['turma']}**"
                )

            with col3:

                if st.button(
                    "🗑️",
                    key=f"excluir_aluno_{i}"
                ):

                    nome_excluido = aluno["nome"]
                    turma_excluida = aluno["turma"]

                    st.session_state.alunos.pop(i)

                    st.session_state.notas = [
                        n for n in st.session_state.notas
                        if not (
                            n["aluno"] == nome_excluido
                            and n["turma"] == turma_excluida
                        )
                    ]

                    st.session_state.chamadas = [
                        c for c in st.session_state.chamadas
                        if not (
                            c["aluno"] == nome_excluido
                            and c["turma"] == turma_excluida
                        )
                    ]

                    st.success(
                        "Aluno excluído!"
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
                f"{a['nome']} - {a['turma']}"
                for a in st.session_state.alunos
            ],
            key="aluno_notas"
        )

        aluno_nome, turma_nome = aluno_selecionado.split(
            " - ",
            1
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

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            n1 = st.number_input(
                "1ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n1),
                step=0.1,
                key="n1"
            )

        with col2:
            n2 = st.number_input(
                "2ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n2),
                step=0.1,
                key="n2"
            )

        with col3:
            n3 = st.number_input(
                "3ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n3),
                step=0.1,
                key="n3"
            )

        with col4:
            n4 = st.number_input(
                "4ª Média",
                min_value=0.0,
                max_value=10.0,
                value=float(valor_n4),
                step=0.1,
                key="n4"
            )

        media = calcular_media(
            n1,
            n2,
            n3,
            n4
        )

        resultado = situacao(media)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Média Final",
                f"{media:.2f}"
            )

        with col2:

            st.metric(
                "Situação",
                resultado
            )

        if st.button(
            "💾 Salvar Notas"
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
# ABA 5 - CHAMADA 2027
# ============================================================

with abas[4]:

    st.header("📅 Chamada Escolar - 2027")

    if not st.session_state.alunos:

        st.warning(
            "Cadastre alunos primeiro."
        )

    elif not st.session_state.disciplinas:

        st.warning(
            "Cadastre disciplinas primeiro."
        )

    else:

        data_chamada = st.date_input(
            "Data da aula",
            value=date(2027, 1, 1),
            min_value=date(2027, 1, 1),
            max_value=date(2027, 12, 31)
        )

        disciplina_chamada = st.selectbox(
            "Disciplina",
            st.session_state.disciplinas,
            key="disciplina_chamada"
        )

        turma_chamada = st.selectbox(
            "Turma",
            st.session_state.turmas,
            key="turma_chamada"
        )

        alunos_turma = [
            a["nome"]
            for a in st.session_state.alunos
            if a["turma"] == turma_chamada
        ]

        st.subheader(
            f"Chamada - {turma_chamada}"
        )

        presencas = {}

        for aluno in alunos_turma:

            presencas[aluno] = st.radio(
                aluno,
                [
                    "Presente",
                    "Falta"
                ],
                horizontal=True,
                key=f"presenca_{aluno}_{data_chamada}_{disciplina_chamada}"
            )

        if st.button(
            "💾 Salvar Chamada"
        ):

            for aluno, presenca in presencas.items():

                st.session_state.chamadas = [
                    c for c in st.session_state.chamadas
                    if not (
                        c["aluno"] == aluno
                        and c["turma"] == turma_chamada
                        and c["disciplina"] == disciplina_chamada
                        and c["data"] == str(data_chamada)
                    )
                ]

                st.session_state.chamadas.append({
                    "aluno": aluno,
                    "turma": turma_chamada,
                    "disciplina": disciplina_chamada,
                    "data": str(data_chamada),
                    "presenca": presenca
                })

            st.success(
                "Chamada salva!"
            )

            st.rerun()

        st.divider()

        st.subheader(
            "📊 Resumo de frequência"
        )

        dados_frequencia = []

        for aluno in alunos_turma:

            faltas = calcular_faltas(
                aluno,
                turma_chamada,
                disciplina_chamada
            )

            total = calcular_aulas(
                aluno,
                turma_chamada,
                disciplina_chamada
            )

            frequencia = calcular_frequencia(
                aluno,
                turma_chamada,
                disciplina_chamada
            )

            dados_frequencia.append({
                "Aluno": aluno,
                "Aulas": total,
                "Faltas": faltas,
                "Frequência (%)": frequencia
            })

        if dados_frequencia:

            st.dataframe(
                pd.DataFrame(
                    dados_frequencia
                ),
                use_container_width=True
            )


# ============================================================
# ABA 6 - RELATÓRIOS
# ============================================================

with abas[5]:

    st.header("📊 Relatórios")

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
                n for n in st.session_state.notas
                if (
                    n["aluno"] == nome
                    and n["turma"] == turma
                )
            ]

            if registros_aluno:

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
                use_container_width=True
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
                f"{a['nome']} - {a['turma']}"
                for a in st.session_state.alunos
            ],
            key="aluno_relatorio"
        )

        nome_relatorio, turma_relatorio = (
            aluno_relatorio.split(
                " - ",
                1
            )
        )

        st.subheader(
            f"Aluno: {nome_relatorio}"
        )

        st.write(
            f"**Turma:** {turma_relatorio}"
        )

        registros = [
            n for n in st.session_state.notas
            if (
                n["aluno"] == nome_relatorio
                and n["turma"] == turma_relatorio
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

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**Média:** {registro['media']:.2f}"
                    )

                with col2:
                    st.write(
                        f"**Situação:** {registro['situacao']}"
                    )

                with col3:
                    st.write(
                        f"**Faltas:** {faltas}"
                    )

                st.write(
                    f"**Frequência:** {frequencia}%"
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

    professores_aprovados = [
        p for p in st.session_state.professores
        if p["status"] == "Aprovado"
    ]

    if not professores_aprovados:

        st.warning(
            "Nenhum professor aprovado."
        )

    else:

        professor_area = st.selectbox(
            "Professor",
            [
                p["nome"]
                for p in professores_aprovados
            ],
            key="professor_area"
        )

        professor_obj = next(
            p for p in professores_aprovados
            if p["nome"] == professor_area
        )

        disciplina_area = st.selectbox(
            "Disciplina",
            professor_obj["disciplinas"],
            key="disciplina_area"
        )

        st.success(
            f"Professor aprovado: {professor_area}"
        )

        st.info(
            f"Disciplina selecionada: {disciplina_area}"
        )

        registros_professor = [
            n for n in st.session_state.notas
            if (
                n["disciplina"] == disciplina_area
            )
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
                use_container_width=True
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
    "Sistema Escolar 2027 • Controle de alunos, professores, "
    "notas e frequência"
)
