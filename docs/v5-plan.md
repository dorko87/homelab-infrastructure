# V5 engineering showcase plan

## Goal

Show how the homelab is managed, how technical problems are investigated, and how changes are checked. Keep the current visual design and the distinction between professional Tier 3 support and independent infrastructure work.

## Work packages

1. Edit existing prose for plain English, short sentences and natural first-person descriptions. Remove long dashes from original prose, not from third-party licenses or quoted text. Keep technical terminology.
2. Expand the deployment migration case and add cases on missing scheduled activity, backup and recovery, and AI-assisted operations. Use documented facts; distinguish verified results from design goals and synthetic illustrations.
3. Describe the AI operating model confirmed by the owner. Specialized agents can plan, investigate, make technical decisions, implement changes, review work and validate results independently within their responsibilities. The human operator sets the overall direction and makes critical decisions. Do not publish actual permission mappings or examples of sensitive approval rules. Present the diagram as a logical model, not a live integration map.
4. Build a standalone synthetic deployment planner. It must accept changed paths and a manifest, classify eligible and excluded stacks, order selected dependencies, reject missing Compose files and invalid policy, detect cycles, and produce deterministic JSON. It must never deploy or connect to a live environment. Label AI-assisted example code accurately.
5. Add tests and a reproducible sample output. Include documentation-only changes, excluded stacks, unknown stacks, dependencies, cycles, missing configuration and invalid paths. Integrate tests into the public CI.
6. Update README navigation and changelog. Keep the landing page concise and link to the detailed cases and runnable example.
7. Review public diffs for private information and unsupported claims. Run structural, rendering, Mermaid, Compose, secret scanning and planner tests. Verify sample output, then review the PR before merging and check main after merge.

## Release conditions

All required tests pass on the reviewed commit. The cases explain decisions and remaining limitations without inventing outcomes. The example is reproducible and cannot perform live deployment. Original prose follows AGENTS.md. The public profile remains accurate. Existing branch protection and third-party trademark review limitations are recorded separately.

This plan concerns the public portfolio only. It does not authorize changes to private infrastructure.
