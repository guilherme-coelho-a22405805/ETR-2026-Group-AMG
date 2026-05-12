"""
AMS Intake Platform — Desktop Prototype (Lab 8)
Variant 3: Determinismo + Explicabilidade
Persona: Transition Manager
Slice: Continuity Score + Explain (UC-02 + UC-05)
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json

from ai_engine.scoring import calculate_continuity_score
from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.explain import explain_score, DeterminismError
from ai_engine.policy import list_policies, get_active_policy
from storage.runs_store import save_run, get_run, load_all_runs


# Mapeamento UI → factor keys (ordem visível ao Transition Manager)
FACTOR_FIELDS = [
    ("documentation_completeness", "Cobertura da documentação"),
    ("monitoring_coverage", "Cobertura de observabilidade"),
    ("dr_bcp_readiness", "Prontidão DR/BCP"),
    ("access_management", "Gestão de acessos (RBAC)"),
    ("integrations_mapped", "Integrações mapeadas"),
    ("support_model_defined", "Modelo de suporte definido"),
]

SECTORS = ["healthcare", "bfsi", "retail", "other"]


class AMSPrototypeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AMS Intake Platform — Variant 3 (Determinism + Explainability)")
        self.root.geometry("900x720")

        # Notebook (abas)
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.score_frame = ttk.Frame(notebook)
        self.explain_frame = ttk.Frame(notebook)
        self.policy_frame = ttk.Frame(notebook)

        notebook.add(self.score_frame, text="1. Calcular Score (UC-02)")
        notebook.add(self.explain_frame, text="2. Explicar Score (UC-05)")
        notebook.add(self.policy_frame, text="3. Registo de Políticas")

        self._build_score_tab()
        self._build_explain_tab()
        self._build_policy_tab()

    # ---------------------- TAB 1 — Continuity Score ----------------------
    def _build_score_tab(self):
        frm = self.score_frame
        header = ttk.Label(
            frm,
            text="UC-02 — Calcular Continuity Score",
            font=("Helvetica", 14, "bold"),
        )
        header.pack(pady=(10, 4))
        ttk.Label(
            frm,
            text="Persona: Transition Manager  |  REQ-002, REQ-009, REQ-010 (Variant)",
            foreground="gray",
        ).pack(pady=(0, 10))

        form = ttk.Frame(frm)
        form.pack(fill="x", padx=20, pady=5)

        # Application ID
        ttk.Label(form, text="Application ID:").grid(row=0, column=0, sticky="w", pady=4)
        self.app_id_var = tk.StringVar(value="APP-TEST-001")
        ttk.Entry(form, textvariable=self.app_id_var, width=30).grid(row=0, column=1, sticky="w")

        # Sector
        ttk.Label(form, text="Sector:").grid(row=1, column=0, sticky="w", pady=4)
        self.sector_var = tk.StringVar(value="healthcare")
        ttk.Combobox(form, textvariable=self.sector_var, values=SECTORS,
                     state="readonly", width=27).grid(row=1, column=1, sticky="w")

        # Factores (sliders 0.0 → 1.0)
        ttk.Separator(form, orient="horizontal").grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=10)
        ttk.Label(form, text="Fatores de Prontidão (0.0 = nenhum, 1.0 = completo)",
                  font=("Helvetica", 10, "italic")).grid(
            row=3, column=0, columnspan=3, sticky="w")

        self.factor_vars = {}
        self.factor_include = {}
        for i, (key, label) in enumerate(FACTOR_FIELDS):
            row = 4 + i
            include_var = tk.BooleanVar(value=True)
            self.factor_include[key] = include_var
            ttk.Checkbutton(form, variable=include_var,
                            text="incluir").grid(row=row, column=0, sticky="w")
            ttk.Label(form, text=label).grid(row=row, column=1, sticky="w")
            val_var = tk.DoubleVar(value=0.7)
            self.factor_vars[key] = val_var
            scale = ttk.Scale(form, from_=0.0, to=1.0, variable=val_var,
                              orient="horizontal", length=200)
            scale.grid(row=row, column=2, sticky="w", padx=5)
            val_lbl = ttk.Label(form, text="0.70", width=5)
            val_lbl.grid(row=row, column=3, sticky="w")
            # Atualizar label dinamicamente
            val_var.trace_add("write", lambda *a, v=val_var, l=val_lbl:
                              l.config(text=f"{v.get():.2f}"))

        # Botão calcular
        ttk.Button(frm, text="Calcular Continuity Score",
                   command=self._on_calculate).pack(pady=15)

        # Output
        ttk.Label(frm, text="Resultado:", font=("Helvetica", 11, "bold")).pack(
            anchor="w", padx=20)
        self.score_output = scrolledtext.ScrolledText(
            frm, height=12, font=("Courier", 9), wrap="word")
        self.score_output.pack(fill="both", expand=True, padx=20, pady=5)

    def _on_calculate(self):
        # Construir payload a partir dos inputs
        responses = {}
        for key, var in self.factor_vars.items():
            if self.factor_include[key].get():
                responses[key] = var.get()

        payload = {
            "application_id": self.app_id_var.get().strip(),
            "sector": self.sector_var.get(),
            "responses": responses,
        }

        try:
            normalized, uncertainty = validate_and_normalize(payload)
            result = calculate_continuity_score(normalized, uncertainty)
            run_id = save_run(normalized, result)

            self.score_output.delete("1.0", tk.END)
            summary = (
                f"✓ Score calculado e persistido\n"
                f"{'='*60}\n"
                f"runId        : {result['runId']}\n"
                f"applicationId: {result['applicationId']}\n"
                f"SCORE        : {result['score']} / 100\n"
                f"policyVersion: {result['policyVersion']}\n"
                f"checksum     : {result['policyChecksum'][:32]}...\n"
                f"inputsHash   : {result['inputsHash'][:32]}...\n"
                f"uncertainty  : {result['uncertainty_applied']}\n"
            )
            if result["missingOptionalFields"]:
                summary += f"missing      : {', '.join(result['missingOptionalFields'])}\n"
            summary += f"\nBreakdown completo:\n"
            summary += json.dumps(result["breakdown"], indent=2, ensure_ascii=False)
            summary += (
                f"\n\n➡  Vai à aba 'Explicar Score' e cola este runId "
                f"para ver Top 5 drivers:\n{result['runId']}"
            )
            self.score_output.insert(tk.END, summary)

            self._refresh_explain_runs()

        except ValidationError as ve:
            messagebox.showerror(
                f"Erro de Validação: {ve.code}",
                f"{ve.message}\n\nCampos: {', '.join(ve.fields)}",
            )
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))

    # ---------------------- TAB 2 — Explain ----------------------
    def _build_explain_tab(self):
        frm = self.explain_frame
        ttk.Label(frm, text="UC-05 — Consultar Explicação de Score",
                  font=("Helvetica", 14, "bold")).pack(pady=(10, 4))
        ttk.Label(frm, text="REQ-006 + REQ-010 (Variant 3) — Top 5 drivers com check de determinismo",
                  foreground="gray").pack(pady=(0, 10))

        row = ttk.Frame(frm)
        row.pack(fill="x", padx=20, pady=5)
        ttk.Label(row, text="Run ID:").pack(side="left")
        self.run_id_var = tk.StringVar()
        self.runs_combo = ttk.Combobox(row, textvariable=self.run_id_var, width=50)
        self.runs_combo.pack(side="left", padx=5)
        ttk.Button(row, text="Refresh", command=self._refresh_explain_runs).pack(side="left")
        ttk.Button(row, text="Explicar", command=self._on_explain).pack(side="left", padx=5)

        # Botão de simulação de tampering (para mostrar E1)
        ttk.Button(frm, text="⚠ Simular adulteração (mostrar E1 da Variante 3)",
                   command=self._simulate_tampering).pack(pady=5)

        ttk.Label(frm, text="Explicação:", font=("Helvetica", 11, "bold")).pack(
            anchor="w", padx=20)
        self.explain_output = scrolledtext.ScrolledText(
            frm, height=22, font=("Courier", 9), wrap="word")
        self.explain_output.pack(fill="both", expand=True, padx=20, pady=5)

    def _refresh_explain_runs(self):
        runs = load_all_runs()
        ids = [r["result"]["runId"] for r in runs]
        self.runs_combo["values"] = ids
        if ids and not self.run_id_var.get():
            self.run_id_var.set(ids[-1])

    def _on_explain(self):
        run_id = self.run_id_var.get().strip()
        if not run_id:
            messagebox.showwarning("Run ID em falta", "Seleciona ou cola um runId")
            return

        stored = get_run(run_id)
        if not stored:
            messagebox.showerror("Run não encontrado", f"Não existe execução: {run_id}")
            return

        try:
            explanation = explain_score(stored, limit=5)
            self.explain_output.delete("1.0", tk.END)
            out = (
                f"✓ Explicação gerada — Integridade OK\n"
                f"{'='*60}\n"
                f"runId       : {explanation['runId']}\n"
                f"score       : {explanation['score']} / 100\n"
                f"policy      : {explanation['policyVersion']} ({explanation['policyStatus']})\n"
                f"\n"
                f"Metodologia:\n  {explanation['methodology']}\n\n"
                f"TOP 5 DRIVERS (ordenados por contribuição absoluta):\n"
                f"{'-'*60}\n"
            )
            for i, drv in enumerate(explanation["drivers"], 1):
                out += (
                    f"  #{i}  {drv['label']}\n"
                    f"      valor: {drv['value']:.2f}   "
                    f"peso: {drv['weight']:.2f}   "
                    f"contribuição: {drv['contribution']:.2f} pts\n"
                )
            if explanation["policyStatus"] == "deprecated":
                out += "\n⚠  AVISO: política DEPRECATED (REQ-007 AC-3)\n"
            out += f"\n[integrity check] inputsHash = {explanation['integrity']['inputsHash']}\n"
            self.explain_output.insert(tk.END, out)

        except DeterminismError as de:
            self.explain_output.delete("1.0", tk.END)
            self.explain_output.insert(
                tk.END,
                f"✗ FALHA DE DETERMINISMO — UC-05 E1 (Variante 3)\n"
                f"{'='*60}\n\n"
                f"runId        : {de.run_id}\n"
                f"hash original: {de.original_hash}\n"
                f"hash replay  : {de.replay_hash}\n\n"
                f"A explicação foi BLOQUEADA porque os dados não passaram "
                f"o check de integridade.\nUm alerta de auditoria seria gerado neste ponto.\n",
            )
            messagebox.showerror(
                "Variante 3 — Determinismo violado",
                "O inputsHash não coincide. Explicação bloqueada (UC-05 E1).",
            )

    def _simulate_tampering(self):
        """Demo da exceção E1 — adultera o stored run para mostrar o bloqueio."""
        run_id = self.run_id_var.get().strip()
        stored = get_run(run_id)
        if not stored:
            messagebox.showwarning("Sem run", "Calcula primeiro um score na aba 1")
            return
        # Mexer no payload SEM atualizar o hash → replay vai falhar
        tampered = json.loads(json.dumps(stored))
        # Alterar uma feature (ex.: subir documentation_completeness)
        tampered["normalizedPayload"]["responses"]["documentation_completeness"] = 0.99
        try:
            explain_score(tampered, limit=5)
        except DeterminismError as de:
            self.explain_output.delete("1.0", tk.END)
            self.explain_output.insert(
                tk.END,
                f"✗ TAMPERING DETETADO (demo)\n"
                f"{'='*60}\n\n"
                f"Alterámos manualmente o payload guardado e o sistema bloqueou "
                f"a explicação porque o inputsHash recalculado deixou de bater "
                f"certo com o original.\n\n"
                f"hash original: {de.original_hash}\n"
                f"hash replay  : {de.replay_hash}\n\n"
                f"➡  Esta é a salvaguarda da Variante 3 em ação.",
            )

    # ---------------------- TAB 3 — Policy Registry ----------------------
    def _build_policy_tab(self):
        frm = self.policy_frame
        ttk.Label(frm, text="Registo de Políticas (REQ-007 Variant)",
                  font=("Helvetica", 14, "bold")).pack(pady=(10, 4))
        ttk.Label(frm, text="Políticas são imutáveis. Cada versão tem checksum SHA-256 único.",
                  foreground="gray").pack(pady=(0, 10))

        cols = ("version", "status", "checksum")
        tree = ttk.Treeview(frm, columns=cols, show="headings", height=8)
        tree.heading("version", text="Version")
        tree.heading("status", text="Status")
        tree.heading("checksum", text="SHA-256 Checksum")
        tree.column("version", width=100)
        tree.column("status", width=120)
        tree.column("checksum", width=600)
        tree.pack(fill="x", padx=20, pady=5)

        for pol in list_policies():
            tree.insert("", "end", values=(
                pol["version"], pol["status"], pol["checksum"]))

        active = get_active_policy()
        ttk.Label(frm, text="Pesos da política ativa:",
                  font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        weights_text = scrolledtext.ScrolledText(frm, height=12, font=("Courier", 9))
        weights_text.pack(fill="both", expand=True, padx=20, pady=5)
        weights_text.insert(tk.END, json.dumps(active["weights"], indent=2))
        weights_text.config(state="disabled")


def main():
    root = tk.Tk()
    AMSPrototypeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
