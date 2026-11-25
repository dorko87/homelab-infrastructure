# AGENTS.md

## Purpose
This repository is a public engineering portfolio based on an independent homelab. It documents infrastructure, deployment automation, reliability, troubleshooting and engineering decisions. It is not a mirror of the private environment or an executable production deployment repository.

## Editorial direction
- Write natural, concise English in the owner's voice. Prefer concrete examples and decisions over buzzwords, generic AI-generated prose and decorative metrics.
- Present professional Tier 3 support experience separately from independent DevOps and infrastructure projects. Do not imply professional DevOps employment or enterprise production ownership based on homelab work.
- Explain the problem, approach, trade-offs, validation, outcome and remaining limitations. Never invent achievements, measurements, tests or implementation status.
- Keep the README approachable; put detailed technical explanations in topic-specific documents. Use accessible Markdown and Mermaid diagrams where useful.

## Writing style
- Use plain, natural English. Write like an engineer explaining their own work to another engineer.
- Avoid em dashes and en dashes in original prose. Use a period, comma, colon or ordinary hyphen as appropriate. Preserve third-party license texts, quoted material, URLs and code syntax.
- Prefer concrete verbs and specific technical details to marketing language. Avoid phrases such as "seamlessly", "robust solution", "leverage", "cutting-edge", and generic claims of excellence.
- Use first person for the owner's verified experience. Use neutral wording for reference material and synthetic examples.
- Do not invent personal experiences, motivations, outcomes, measurements or evidence to make writing sound more personal.
- Keep sentences and paragraphs short where useful. Avoid repetitive introductions, slogan-like headings and unnecessary summaries.
- Retain accurate technical terms and disclose AI-assisted work where relevant. Do not describe an AI-assisted example as independently authored by the owner.
- Review README files, case studies, diagram labels and new documentation for these rules before release.

## AI operations descriptions
- Describe specialized agents as able to work independently, make technical decisions, investigate, implement, review and validate within their responsibilities.
- Describe the human operator as setting overall direction and making critical decisions. Do not imply routine decisions require human approval.
- Keep descriptions at the logical level. Do not publish actual access mappings or specific sensitive approval rules.

## Privacy and public release
- Treat every tracked file, commit, branch, issue, PR and generated artifact as public.
- Never copy private repositories, live configuration, logs, screenshots, exports, or existing private diagrams into this repository.
- Do not publish real IP addresses, hostnames, domains, endpoints, credentials, tokens, identifiers, storage paths, access policies, personal data, customer or employer information, or operational details that expose the live environment.
- Use generic host roles, newly authored logical diagrams and synthetic examples. Do not include realistic credential values. Public technology names may be used when appropriate.
- Do not access private infrastructure, retrieve secrets, or execute live deployment commands for this portfolio. Obtain separate explicit authorization for any such work outside this repository.
- If uncertain whether information is suitable for publication, omit it and ask the owner before publishing. Redaction after a public commit does not remove the original exposure.

## Architecture and accuracy
- Preserve Git as the configuration source of truth and distinguish deployment policy, planning, validation and execution.
- Distinguish intended architecture from verified implementation and historical decisions from current state.
- Do not describe a retained fallback mechanism as automatic rollback or tested recovery without evidence.
- Deployment success does not imply application health; backup success does not imply recoverability.
- Label examples as synthetic and distinguish syntax validation from actual runtime testing.

## Working agreement
- Read this file and the relevant documentation before editing.
- Keep changes focused; do not reorganize the portfolio, change its positioning or introduce new tools and dependencies without a clear reason and owner approval for material changes.
- Preserve established decisions. Record material approved changes in the relevant documentation and update these instructions only when the working agreement changes.
- Use one shared instruction source; tool-specific instruction files may reference this file instead of duplicating its contents.
- Review the diff, check relative links, Markdown and Mermaid syntax, parse YAML examples, and scan the proposed publication for sensitive information before committing. Report checks actually performed and any limitations.
- Do not treat a request to edit as authorization to publish unrelated changes. Obtain explicit approval before exposing new categories of private-derived information.
- Never deploy to the private homelab from this repository.

## Visual design
- Maintain one visual per concept on the landing page; detailed decision flows belong in topic-specific documentation.
- Use local SVG assets, consistent colors and readable labels. Include text alternatives for complex graphics.
- Use authentic service artwork with recorded sources and applicable license notices; do not imply endorsement. Use a generic symbol when a logo cannot be verified.
- Keep animation illustrative, finite and compatible with reduced-motion preferences. Never imply live telemetry.
- Check SVG XML, embedded assets, links, contrast and desktop/mobile rendering before claiming visual QA is complete.

## Portfolio quality workflow
- Use a focused branch and pull request for changes to public portfolio content. Verify the pull-request checks and review the diff before merging; do not assume branch protection is enabled.
- Edit `assets/services.json` and local icon files rather than hand-editing the generated ecosystem SVGs. Run `node scripts/generate_assets.mjs` and verify the generated output with `--check`.
- Keep the illustrative animation under five seconds, retain a static readable fallback, and test reduced-motion behavior.
- Distinguish actual validation results from manual review and from outstanding checks. Never expose private inventory to regenerate public graphics.
