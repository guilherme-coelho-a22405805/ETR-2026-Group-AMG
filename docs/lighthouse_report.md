# Lighthouse Report — Lab 13 (Optional)

## Target page
- **URL / local route:** `http://localhost:8501/` — UI web (Streamlit) do protótipo AMS Intake Platform (`docs/ams_prototype_lab8/ams_prototype/ui/app_web.py`)
- **Página testada:** Tab 1 — *Calcular Score (UC-02)* (página de entrada do slice Continuity Score + Explain)
- **Ferramenta:** Google Lighthouse 13.0.2 (Chromium 148), via DevTools
- **Modo:** Navigation | **Device:** Desktop (emulado) | **Throttling:** custom (default)
- **Data de captura:** 06/06/2026, 23:32 (GMT+1)

## Summary
| Categoria | Score | Faixa |
|---|---:|---|
| **Performance** | 49 | 🔴 0–49 |
| **Accessibility** | 99 | 🟢 90–100 |
| **Best Practices** | 100 | 🟢 90–100 |
| **SEO** | 82 | 🟠 50–89 |

### Core metrics (Performance)
| Métrica | Valor | Estado |
|---|---:|---|
| First Contentful Paint (FCP) | 4.7 s | 🔴 |
| Largest Contentful Paint (LCP) | 5.1 s | 🔴 |
| Total Blocking Time (TBT) | 0 ms | 🟢 |
| Cumulative Layout Shift (CLS) | 0.187 | 🟠 |
| Speed Index | 4.7 s | 🔴 |

## Top findings (min. 3)

1. **Finding: Performance baixa (49) — FCP 4.7 s e LCP 5.1 s muito acima do recomendado.**
   - **Why it matters:** O carregamento inicial demora 4–5 segundos até a página ficar visível/utilizável. Diagnósticos principais: *Reduce unused JavaScript* (~1.836 KiB de poupança estimada), *Avoid enormous network payloads* (4.153 KiB no total) e *Font display* (~920 ms). A maioria do peso vem do bundle do próprio framework Streamlit, não do nosso código de negócio (`ai_engine`).
   - **Action:** Para um protótipo de aula o impacto é aceitável, mas as melhorias concretas seriam: ativar `gzip`/compressão no serviço, usar `font-display: swap` para as fontes, e — caso evoluísse para produção — servir a UI atrás de um proxy com cache de estáticos. A médio prazo, expor a lógica via API HTTP (já previsto como *next step* no `bdd_report.md`) e ter uma UI mais leve removeria grande parte deste peso.
   - **Relação com NFR:** Liga-se diretamente ao **NFR-001 (Performance, p95 ≤ 500ms)**. Importante notar que o NFR-001 mede o *Server Response Time interno do G3* (processamento analítico), e **não** o tempo de carregamento do front-end Streamlit — que é o que o Lighthouse mede aqui. Os 4.7 s são do browser a montar a UI; o cálculo do score em si (`calculate_continuity_score`) é praticamente instantâneo. Esta distinção está alinhada com a clarificação feita em `requirements_validation.md` (NFR-001).

2. **Finding: SEO (82) — `Document does not have a meta description` e `robots.txt is not valid` (41 erros).**
   - **Why it matters:** O Lighthouse penaliza a ausência de meta description e um `robots.txt` inválido. No nosso contexto têm impacto praticamente nulo: a aplicação é uma ferramenta interna para o *Transition Manager*, não um site público que precise de ser indexado por motores de busca.
   - **Action:** Não é prioritário corrigir para o âmbito do protótipo. Se necessário para subir o score, bastaria injetar uma `<meta name="description">` via `st.markdown`/config do Streamlit. Documentamos como *não-aplicável ao slice* em vez de o tratar como defeito.
   - **Relação com NFR:** Sem NFR associado (o projeto não tem requisitos de descoberta/SEO).

3. **Finding: Accessibility (99) — `Heading elements are not in a sequentially-descending order`.**
   - **Why it matters:** A hierarquia de cabeçalhos da página salta níveis (ex.: um `h1` seguido diretamente de um `h3` sem `h2`), o que prejudica a navegação por leitores de ecrã e por teclado. É o único achado automático que baixou o score de 100 para 99.
   - **Action:** Reorganizar os títulos do Streamlit para respeitar a ordem `h1 → h2 → h3` (usar `st.header`/`st.subheader` de forma consistente em vez de saltar para `st.markdown("###…")`). É uma correção barata e de baixo risco.
   - **Relação com NFR:** Reforça o objetivo de **transparência/usabilidade** da Variante 3 (explicabilidade dirigida ao Transition Manager); embora não exista um NFR formal de acessibilidade, é coerente com OBJ-2 (transparência das decisões da IA). Best Practices 100/100 mostra que, em segurança e práticas web gerais, a app já está limpa.

## Notes
- **Best Practices = 100:** todos os audits relevantes passaram; os itens listados em *Trust and Safety* (CSP, HSTS, COOP, etc.) aparecem como informativos/não-pontuados e são típicos de qualquer servidor de desenvolvimento local, não defeitos do protótipo.
- **Leitura geral:** os scores baixos (Performance/SEO) derivam de características do framework Streamlit e do contexto *localhost*, não de problemas na lógica do AI Engine. As categorias que dependem do nosso trabalho (Accessibility, Best Practices) estão em 99–100.
- **Evidência:** relatório completo exportado em `docs/assets/lighthouse_report.pdf` (Lighthouse 13.0.2).
