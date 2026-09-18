# September 2026 Market Review and Roadmap Update

Received and reviewed: 17 September 2026, during Month 03 / Week 10.

## Decision

Keep the direction: **backend-focused developer building production AI applications,
with practical full-stack capability**. This describes the intended career direction,
not a claim of current production experience or seniority. Continue applying to
appropriate internships and junior Python/backend/full-stack roles.

The material supplied by Furkan was an external ChatGPT research summary. This
record preserves its principal claims and proposed changes, then distinguishes
source verification from the learning decisions we adopt. It is not a new census
of jobs or an independently reproduced statistical study.

## Submitted Research Summary

- Keep Python, FastAPI, PostgreSQL, Docker, GitHub Actions, AWS, OpenAI, RAG,
  and pgvector; retain React with TypeScript.
- Strengthen testing, async Python, Redis, authentication/authorization,
  Linux/networking, observability, CI/CD, and security.
- Expand the AI path from API use to Responses API, Structured Outputs, tool
  calling, RAG/pgvector, evals, MCP, agents, agent security/observability, and
  evaluation of the new Agents API.
- Prioritize evaluation over an unmeasured RAG demo. Learn direct SDK/API use
  before adopting orchestration frameworks. Keep Kubernetes later.
- Treat difficult junior hiring as a reason to build demonstrable engineering
  skills. The submitted October checklist included Python fundamentals, OOP,
  exceptions, types, pytest, async/await, file/JSON/HTTP handling, Git, Ruff,
  Docker, CI, a clear README, and one tested original application.

The submitted numerical and product claims are retained in the verification
table below rather than silently converted into universal market facts.

## Source Verification

Sources accessed on 17 September 2026. Verification means the publisher reports
the finding, not that we audited its raw collection pipeline.

| Submitted claim | Finding and limitation |
| --- | --- |
| 360,000+ postings: Python 18.6%, AWS 11.3%, Docker 7%, CI/CD 6.7%, React 6.7%; Software Engineer: Python 31.2%, AI 26.6%, AWS 21.4%, React 18% | These figures appear in [Qarera's report](https://www.qarera.com/reports/most-in-demand-skills-2026). The corpus was collected December 2025–June 2026; it is not a September-only snapshot. |
| LangChain/LangGraph 2.2%, RAG 1.6%, vector databases 1%, OpenAI APIs 0.9% | Also reported by Qarera. Broad-corpus mention frequencies do not determine the usefulness of a technology for one specific role. |
| TypeScript became #1 on GitHub while Python remained prominent in AI | [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) supports this, using monthly contributor activity for the language ranking. GitHub activity is not hiring demand. |
| 390 AI-engineer postings: LLMs 63%, Python 59%, evals 56%, agents 50%, RAG 26%, AWS 20% | [Dexity's August report](https://dexity.com/intel/ai-engineer-hiring-report-2026) reports these for its July scan of 69 company boards. It also reports a median requirement of five years and approximately 1% junior roles. The sample is senior-heavy and keyword-coded. |
| 2,852 live AI jobs: Python 1,505, agents 877, AWS 454, Kubernetes 382, evals 305, CI/CD 296 | Verified in [AI Hiring Board's skills report](https://www.aihiringboard.com/blog/ai-skills-in-demand-september-2026), published September 8 using a September 7 snapshot. These are keyword mentions, including optional skills, in the companies the board tracks. |
| UK CS graduates entering coding roles fell from about 40% to 28% | [The Guardian reports this comparison](https://www.theguardian.com/education/2026/sep/12/ai-computer-science-graduates-job-prospects-uk-data). We did not reproduce it from the underlying graduate data. |
| NYC entry-level tech postings fell 49% over 2022–2025 | Supported by the [Center for an Urban Future report](https://nycfuture.org/research/nyc-entry-level-tech-pathways-in-the-age-of-ai). This is a regional postings result, not a Turkish/global employment rate or proof of a single cause. |
| Agents API launched September 10, 2026 in public beta | Confirmed in the [official OpenAI changelog](https://developers.openai.com/api/docs/changelog). The [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview) describes managed agent execution. Beta availability is not an adoption requirement. |
| AWS DVA-C03 moves toward AI-assisted development | The [AWS September announcement](https://aws.amazon.com/blogs/training-and-certification/september-2026-new-offerings/) supports this. Registration is announced for October 27 and delivery for December 1, 2026. The announcement excludes RAG design, prompt engineering, and model selection from exam scope; it does not replace the AI learning plan. |

Qarera's [dataset documentation](https://github.com/dreamjobs-tech/most-in-demand-skills-2026)
explains that one posting can mention multiple skills and that country/pay fields
were too sparse to report. The AI board likewise warns that keyword matches are
not necessarily requirements. Do not add percentages across skills, average these
different samples, or infer month-over-month growth by comparing unlike datasets.
Neither these sources nor the UK/NYC figures establish Furkan's individual hiring
probability in Türkiye, Germany, or remote work.

## Fit With the Existing Roadmap

React + TypeScript, testing, authentication/authorization, and retrieval evaluation
were already present. Responses API, Structured Outputs, tool calling, and bounded
MCP study were also part of the mentoring baseline. This review strengthens and
clarifies those topics; it does not present all of them as new additions.

Furkan recalls a prior review at the beginning of Month 02. Preserve the existing
roadmap and decision history as that baseline. A separately sourced August market
report was not located during this review; do not reconstruct one or invent its
sources/date. Existing ROADMAP.md and the Month 02 report document the earlier
delivery targets and their actual carry-over.

The supplied suggestion to start FastAPI/PostgreSQL after October's fundamentals
checklist is out of date for this learner. Month 02 already covered that stack,
and OpsDesk's foundation and guarded PostgreSQL infrastructure are merged. Current
evidence is 37 local non-database tests and six local PostgreSQL tests; the existing
hosted workflow selects seven foundation tests. No completed product deployment,
AI feature, business schema, or production operation is implied.

## Adopted Changes and Sequencing

| Phase | Concrete application | Completion evidence |
| --- | --- | --- |
| Month 03, now | Continue OpsDesk schema, authorization boundaries, tests, safe logging, and the planned backend preview. Expand fast CI selection in a bounded follow-up. | Reviewed migrations and integration tests, explicit error/security cases, CI evidence for the tests actually selected, and deployment evidence when delivered. |
| Month 03–04, after the synchronous lifecycle is understood | A small async Python exercise using outbound HTTP: await, concurrent I/O, timeouts, cancellation, and blocking-call behavior. Add Linux process/permissions and DNS/TCP/TLS troubleshooting around deployment. | Tests for success, timeout, and cancellation; explanation of when concurrency helps. No automatic conversion to async SQLAlchemy. |
| Month 04 | Keep React + TypeScript and API integration. | Typed client behavior and a working full-stack demo. |
| Month 05 | Keep Docker/Compose, Redis, and background jobs in their planned phase. Use AWS as the preferred cloud learning target after checking cost and fit. | Reproducible environment, cache/job failure behavior, IAM/secrets/logs/budget controls in any AWS deployment. No mandatory certification purchase. |
| Month 06 | Start with the maintained OpenAI SDK and Responses API, Structured Outputs, and one bounded tool workflow. Introduce evals with the first AI feature, not after a full RAG system. | Versioned examples and expected criteria, baseline comparison, schema checks, tool authorization/failure cases, latency/cost measurements, and a repeatable evaluation command. |
| Months 07–08 | Build DocuMind RAG with pgvector and separate retrieval/answer evaluation. Study MCP after direct tool calling and evaluate one bounded agent workflow only when its simpler baseline works. | Retrieval relevance, grounded answers/citations, tenant-safe retrieval, prompt-injection cases, and measured regressions. Agent exercises require step/time/cost limits and observable tool traces. |
| Month 08 onward, capacity permitting | Compare a maintained Agents SDK/workflow implementation with the Agents API if the project needs durable managed execution. Recheck API status, pricing, data handling, and compatibility then. | A documented adopt/defer decision based on measured benefit. No beta API, framework, or multi-agent dependency is required to finish the core projects. |
| Month 10 | Deepen the existing deployment/CI/monitoring/security work. Kubernetes remains optional after practical containers/cloud operations. | Operational failure/recovery evidence and measured improvements, not a technology checklist. |

Evals, authorization, observability, and security accompany each AI increment.
They are not steps postponed until after autonomous execution is added. MCP is
an integration protocol; agent workflows do not require it. Agents API and Agents
SDK are distinct implementation options, not interchangeable product names or
mandatory successive milestones.

For agent exercises, start read-only, validate tool arguments, check current
user/tenant permissions in application code, treat retrieved/tool text as
untrusted, and require review for consequential writes. Log useful traces without
secrets or unnecessary personal data. Compare against the simpler non-agent path.

## October Checkpoint and Capacity

By the end of Month 03, prioritize a tested original OpsDesk backend increment,
schema/authorization evidence, an honest README, and the planned preview or a
clearly recorded deployment blocker. Preserve Python fundamentals and review
gaps through project work rather than restart introductory exercises. Docker
remains Month 05; the report does not impose a new September Docker deadline.

Stay within the existing 15–20 hour weekly plan. The async exercise replaces a
bounded learning block after current prerequisites; agent API/framework comparisons
use optional capacity and are deferred before core features or tests are cut.
AWS certification is a later decision after practical deployment experience.
Keep official exam dates under review: the AWS announcement and localized landing
page differed on DVA-C02's last exam day during this check, so do not book from
this note.

## Immediate Effect — 17 September

Proceed with issue #7, the Users/Organizations/Memberships schema and Alembic
verification. Preserve synchronous persistence and the dedicated
opsdesk_product_test target; the Month 02 databases remain untouched.
This is a roadmap/documentation update, not new implementation or completed learning.

At the next monthly review, compare this plan with actual delivery and a small
deduplicated sample of relevant junior/internship postings, recording dates,
location, experience requirements, and work-authorization constraints. Treat a
new API release as a candidate tool, not a reason to replace the career direction.
