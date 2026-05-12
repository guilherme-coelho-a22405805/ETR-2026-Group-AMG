"""
AMS Intake Platform — Web UI (Streamlit)
Variant 3: Determinismo + Explicabilidade
Persona: Transition Manager
Slice: Continuity Score + Explain (UC-02 + UC-05)

Versão web equivalente ao desktop Tkinter — usada em Codespaces / servidores
sem display gráfico. Toda a lógica de negócio permanece em `ai_engine/`.
"""
import json
import sys
import os

# Permite correr a partir da raiz do projeto OU desta pasta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from ai_engine.scoring import calculate_continuity_score
from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.explain import explain_score, DeterminismError
from ai_engine.policy import list_policies, get_active_policy
from storage.runs_store import save_run, get_run, load_all_runs


FACTOR_FIELDS = [
    ("documentation_completeness", "Cobertura da documentação"),
    ("monitoring_coverage", "Cobertura de observabilidade"),
    ("dr_bcp_readiness", "Prontidão DR/BCP"),
    ("access_management", "Gestão de acessos (RBAC)"),
    ("integrations_mapped", "Integrações mapeadas"),
    ("support_model_defined", "Modelo de suporte definido"),
]

SECTORS = ["healthcare", "bfsi", "retail", "other"]


# ---------------- Page config ----------------
st.set_page_config(
    page_title="AMS Intake Platform — Variant 3",
    page_icon="🧮",
    layout="wide",
)

st.title("AMS Intake Platform")
st.caption(
    "Variant 3 — Determinism + Explainability  |  "
    "Persona: Transition Manager  |  Lab 8 prototype"
)

tab1, tab2, tab3 = st.tabs([
    "1. Calcular Score (UC-02)",
    "2. Explicar Score (UC-05)",
    "3. Registo de Políticas",
])


# ====================== TAB 1 — Continuity Score ======================
with tab1:
    st.subheader("UC-02 — Calcular Continuity Score")
    st.caption("REQ-002, REQ-009, REQ-010 (Variant)")

    col_l, col_r = st.columns([1, 1])

    with col_l:
        app_id = st.text_input("Application ID", value="APP-TEST-001")
        sector = st.selectbox("Sector", SECTORS, index=0)

    with col_r:
        st.markdown(
            "**Como simular flows:**\n"
            "- *Happy path:* preenche tudo\n"
            "- *Alt flow A1:* desmarca alguns checkboxes → uncertainty_applied=True\n"
            "- *Exception E1:* deixa o Application ID em branco"
        )

    st.markdown("##### Fatores de prontidão (0.0 = nenhum, 1.0 = completo)")

    responses_ui = {}
    for key, label in FACTOR_FIELDS:
        c1, c2 = st.columns([1, 4])
        with c1:
            include = st.checkbox("incluir", value=True, key=f"inc_{key}")
        with c2:
            value = st.slider(label, 0.0, 1.0, 0.7, 0.05, key=f"val_{key}")
        if include:
            responses_ui[key] = value

    if st.button("Calcular Continuity Score", type="primary"):
        payload = {
            "application_id": app_id.strip(),
            "sector": sector,
            "responses": responses_ui,
        }
        try:
            normalized, uncertainty = validate_and_normalize(payload)
            result = calculate_continuity_score(normalized, uncertainty)
            save_run(normalized, result)

            st.success(f"✓ Score calculado e persistido — runId `{result['runId']}`")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Score", f"{result['score']} / 100")
            m2.metric("Policy", result["policyVersion"])
            m3.metric("Uncertainty", "Sim" if result["uncertainty_applied"] else "Não")
            m4.metric("Missing optional",
                      str(len(result["missingOptionalFields"])))

            st.markdown("**Metadados de integridade (Variante 3):**")
            st.code(
                f"policyChecksum: {result['policyChecksum']}\n"
                f"inputsHash    : {result['inputsHash']}\n"
                f"runId         : {result['runId']}",
                language="text",
            )

            st.markdown("**Breakdown por fator:**")
            st.dataframe(result["breakdown"], use_container_width=True)

            if result["missingOptionalFields"]:
                st.warning(
                    "Campos opcionais em falta (penalização por incerteza): "
                    + ", ".join(result["missingOptionalFields"])
                )

            st.info(
                f"➡  Vai à aba **Explicar Score** e seleciona "
                f"o runId `{result['runId']}` para ver os Top 5 drivers."
            )

        except ValidationError as ve:
            st.error(f"**Erro de Validação:** `{ve.code}` — campos: {ve.fields}")
            st.caption(ve.message)
        except Exception as e:
            st.exception(e)


# ====================== TAB 2 — Explain ======================
with tab2:
    st.subheader("UC-05 — Consultar Explicação de Score")
    st.caption("REQ-006 + REQ-010 (Variant 3) — Top 5 drivers com check de determinismo")

    runs = load_all_runs()
    ids = [r["result"]["runId"] for r in runs]

    if not ids:
        st.warning("Ainda não há execuções. Calcula primeiro um score na aba 1.")
    else:
        selected = st.selectbox(
            "Run ID",
            ids,
            index=len(ids) - 1,
            help="Mais recente em baixo",
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            do_explain = st.button("Explicar (happy path)", type="primary")
        with c2:
            do_tamper = st.button(
                "⚠ Simular adulteração (Variante 3 — E1)",
                help="Adultera o payload guardado e mostra o bloqueio do Explain",
            )

        stored = get_run(selected)

        if do_explain and stored:
            try:
                explanation = explain_score(stored, limit=5)
                st.success(
                    f"✓ Explicação gerada — integridade OK  |  "
                    f"score {explanation['score']}/100"
                )

                m1, m2, m3 = st.columns(3)
                m1.metric("Policy version", explanation["policyVersion"])
                m2.metric("Policy status", explanation["policyStatus"])
                m3.metric("inputsHash (12)", explanation["integrity"]["inputsHash"][:12] + "…")

                if explanation["policyStatus"] == "deprecated":
                    st.warning("⚠ Política DEPRECATED (REQ-007 AC-3)")

                st.markdown("**Metodologia:**")
                st.info(explanation["methodology"])

                st.markdown("##### TOP 5 drivers (ordenados por contribuição absoluta)")
                for i, drv in enumerate(explanation["drivers"], 1):
                    with st.container(border=True):
                        cc1, cc2, cc3, cc4 = st.columns([3, 1, 1, 1])
                        cc1.markdown(f"**#{i} {drv['label']}**")
                        cc2.metric("valor", f"{drv['value']:.2f}")
                        cc3.metric("peso", f"{drv['weight']:.2f}")
                        cc4.metric("contribuição", f"{drv['contribution']:.2f} pts")

            except DeterminismError as de:
                st.error("✗ Falha de determinismo — explicação BLOQUEADA")
                st.code(
                    f"runId        : {de.run_id}\n"
                    f"hash original: {de.original_hash}\n"
                    f"hash replay  : {de.replay_hash}",
                    language="text",
                )

        if do_tamper and stored:
            tampered = json.loads(json.dumps(stored))
            tampered["normalizedPayload"]["responses"]["documentation_completeness"] = 0.99
            try:
                explain_score(tampered, limit=5)
                st.warning("Não esperado: tampering não foi detetado.")
            except DeterminismError as de:
                st.error(
                    "✗ TAMPERING DETETADO — Variant 3 E1\n\n"
                    "Alterámos manualmente o payload guardado e o sistema "
                    "bloqueou a explicação porque o inputsHash recalculado "
                    "deixou de bater certo com o original."
                )
                st.code(
                    f"hash original: {de.original_hash}\n"
                    f"hash replay  : {de.replay_hash}",
                    language="text",
                )
                st.caption("➡  Esta é a salvaguarda da Variante 3 em ação.")


# ====================== TAB 3 — Policy Registry ======================
with tab3:
    st.subheader("Registo de Políticas (REQ-007 Variant)")
    st.caption("Políticas são imutáveis. Cada versão tem checksum SHA-256 único.")

    st.dataframe(list_policies(), use_container_width=True)

    st.markdown("##### Pesos da política ativa")
    active = get_active_policy()
    st.json(active["weights"])