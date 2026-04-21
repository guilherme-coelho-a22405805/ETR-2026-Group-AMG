# Requirements Validation — Lab 7


## Selected requirements (min. 6)
- **REQ-001:** NBQ Service (Variant impact: No)
- **REQ-002:** Continuity Score Calculation (Variant impact: No)
- **REQ-006:** Explain Endpoint (Variant impact: **Yes**)
- **REQ-007:** Policy Versioning & Registry (Variant impact: **Yes**)
- **REQ-010:** Determinism & Replay Metadata (Variant impact: **Yes**)
- **NFR-001:** Performance de Resposta Analítica (Variant impact: No)

## Variant-driven validation questions (min. 3)
1. Como podemos garantir matematicamente que o cliente recebe sempre o mesmo resultado de score (Determinismo) se não forçarmos o versionamento de tudo o que muda no G1?
2. Para o Explain Endpoint (REQ-006), se um driver for baseado num sistema externo que caiu, o que mostramos ao utilizador para não quebrar a explicabilidade?
3. O REQ-010 fala em guardar um `inputsHash`. Onde é que esse hash é gerado (no G1 ou no G3) e como é garantida a segurança dessa chave para auditoria?

## Validation results

### REQ-001 — NBQ Service
- **Status:** Valid
- **Issues found:** Faltava clarificar o que acontece se o cliente enviar um setor/indústria que não existe no perfil.
- **Proposed fix:** Adicionar AC especificando o fallback para "Generic Profiling" ou erro HTTP 400.
- **Expected evidence:** Teste de API automatizado cobrindo um perfil de setor inválido.

### REQ-002 — Continuity Score Calculation
- **Status:** Needs rewrite
- **Issues found:** O termo "penalização" está ambíguo. Não diz quanto é que um serviço é penalizado pela falta de DR.
- **Proposed fix:** Atualizar o requisito para remeter o cálculo exato para a `policyVersion` ativa, removendo a lógica fixa do texto do requisito.
- **Expected evidence:** Demonstração de cálculo com e sem DR.

### REQ-006 — Explain Endpoint
- **Status:** Valid
- **Issues found:** O "Top 5" é fixo, mas e se o utilizador quiser ver todos os drivers (ex: 20 fatores)?
- **Proposed fix:** Adicionar query parameter `?limit=all` como *Nice to Have*, mas o default mantém-se em 5 para cumprir a variante.
- **Expected evidence:** Unit test verificando a ordenação decrescente de impacto absoluto.

### REQ-007 — Policy Versioning & Registry
- **Status:** Needs rewrite
- **Issues found:** O requisito não especifica se a política pode ser apagada.
- **Proposed fix:** Clarificar que as políticas são "Append-Only". Uma política nunca pode ser eliminada (Hard Delete), apenas inativada.
- **Expected evidence:** Code review à tabela da base de dados e teste de segurança tentando fazer `DELETE`.

### REQ-010 — Determinism & Replay Metadata
- **Status:** Valid
- **Issues found:** Se o payload do G1 mudar o seu esquema JSON (ex: adicionar um campo de metadados invisível), o `inputsHash` vai mudar e quebrar o determinismo.
- **Proposed fix:** O hash tem de ser gerado apenas sobre o subset de dados usados no cálculo (*features* efetivas) e não sobre todo o payload bruto.
- **Expected function:** Teste de BDD comparando o mesmo cenário com metadados extra no JSON.

### NFR-001 — Performance de Resposta Analítica
- **Status:** Needs clarify
- **Issues found:** O tempo de "500ms" inclui a latência da rede entre o G2 e o G3?
- **Proposed fix:** Especificar que os 500ms são de tempo de processamento interno do G3 (Server Response Time).
- **Expected evidence:** Relatório de Load Testing (ex: k6).