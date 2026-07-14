# CLAUDE.md — RECONECTA (ML Educação)

## Contexto do Projeto
Empresa de mentoria high-ticket para profissionais de harmonização facial
(dentistas, médicos, biomédicos). Stack de automação e operações comerciais.

## Stack Técnico
- **Automações**: n8n (workflows.reconectaoficial.com)
- **CRM**: Zoho CRM (credential ID: G6Pk2iJsiTF9v5Wk)
- **WhatsApp**: Evolution API (instância: "Suporte")
- **Banco de dados**: PostgreSQL no Railway
- **Atendimento**: Chatwoot
- **Gestão de tarefas**: ClickUp (Pós-Vendas space ID: 901313716855)
- **E-mail transacional**: ZeptoMail
- **DNS/Proxy**: Cloudflare
- **Rastreamento**: Stape / sGTM

## Convenções de Código
- Comentários SEMPRE em português (BR)
- Variáveis: camelCase
- Nomes de workflow n8n: snake_case descritivo (ex: zoho_lead_reengajamento)
- Nomes de nodes n8n: verbo + objeto (ex: "Buscar Lead no Zoho", "Criar Task ClickUp")
- JSON de payloads: sempre validar estrutura antes de enviar para APIs externas

## Regras de Segurança
- NUNCA modificar workflows ativos em produção sem confirmar comigo
- NUNCA expor credentials, tokens ou API keys no código
- Antes de qualquer DELETE em banco: mostrar o SELECT equivalente e aguardar confirmação
- Mudanças em Evolution API (WhatsApp): confirmar antes — erros afetam 550+ grupos

## Arquitetura de Dados (Zoho CRM)
- Estrutura centrada em Deals (não Contacts)
- Pipeline principal: Perdidos → Outbound/Reengajamento
- Campos críticos: status do deal, etapa do funil, atribuição de closer
- Queries via COQL — sempre testar com LIMIT 5 antes de rodar em escala

## Contexto de Negócio
- Produto principal: Mentoria RECONECTA (ciclos 6m/12m)
- Metodologia core: SUPERCASO (lente de transformação, não procedural)
- Framework de agenda: "Agenda do Milhão" (3 novos/semana + 4 recorrências)
- Gamificação pós-vendas: Sistema de Faixas com pontos e multiplicadores
- Evento recorrente: "Momento Reconecta" (presencial)

## Padrões de Automação n8n
- Sempre incluir node de tratamento de erro com notificação
- Webhooks: validar payload antes de processar
- Loops em grandes volumes: adicionar delay para não estourar rate limits
- Evolution API: checar status da instância antes de enviar mensagem

## O que NÃO fazer
- Não criar soluções que não escalam para volume (100+ leads/dia)
- Não hardcodar IDs — usar variáveis de ambiente ou parâmetros
- Não assumir que webhook chegou completo — sempre validar campos obrigatórios
- Não usar mocks em testes — testar contra dados reais quando possível

## Pasta de produção (carrosséis/conteúdo)
- No Mac do Sávio, os posts produzidos vivem em `/Volumes/SSD kenipe/estáticos/novos/SEM{xx}/{slug}/` (pasta semanal criada por launchd aos domingos).
- **Em máquinas sem esse SSD** (ex.: outro membro do time): usar `./producao/SEM{xx}/{slug}/` na raiz deste repo (gitignorada — post produzido é local). Toda skill/checklist que citar o SSD segue esta regra de fallback.
- Posts JÁ EXPORTADOS são imutáveis: post novo = pasta nova + AD novo (nunca sobrescrever).

## Pessoas-chave (para contexto, não incluir em código)
- Leonardo Rosso e Ana Luiza: fundadores
- Jardel: infraestrutura tech
- Gabriel: dados e BI
- Letícia/Leidianne: liderança pré-vendas
