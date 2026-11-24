<p align="center"><img src="assets/hero.svg" alt="Homelab infrastructure — Build, Deploy, Observe, Recover" width="100%"></p>

# My Homelab Infrastructure

<p align="center"><strong>From a Git commit to a running service — and everything in between.</strong></p>

<p align="center">
  <img alt="Defined hosts: 5" src="https://img.shields.io/badge/Defined%20hosts-5-2563EB?style=for-the-badge">
  <img alt="Defined stacks: 40" src="https://img.shields.io/badge/Defined%20stacks-40-0D9488?style=for-the-badge">
  <img alt="CI validation jobs: 11" src="https://img.shields.io/badge/CI%20jobs-11-7C3AED?style=for-the-badge">
</p>

<p align="center">
  <a href="architecture/overview.md">Architecture</a> ·
  <a href="ci-cd/deployment-workflow.md">Deployments</a> ·
  <a href="reliability/disaster-recovery.md">Recovery</a> ·
  <a href="case-studies/deployment-migration.md">Case study</a>
</p>

I started building this environment to run my own services. Over time, the interesting part became managing changes across multiple machines without turning every upgrade into a manual maintenance task.

My professional background is in Tier 3 support and production troubleshooting. This homelab is where I independently explore infrastructure engineering, DevOps practices and automation.

The numbers above describe the private configuration snapshot dated November 24, 2026, not a live inventory of running services. The public portfolio has its own independent validation workflow.

[![Portfolio validation](https://github.com/dorko87/homelab-infrastructure/actions/workflows/portfolio-validation.yml/badge.svg?branch=main)](https://github.com/dorko87/homelab-infrastructure/actions/workflows/portfolio-validation.yml)

## The service ecosystem

<picture>
  <source media="(max-width: 600px)" srcset="assets/service-ecosystem-mobile.svg">
  <img src="assets/service-ecosystem.svg" alt="Selected services grouped by delivery, observability, networking, media, security and recovery, and AI-assisted operations." width="100%">
</picture>

[Compact mobile layout](assets/service-ecosystem-mobile.svg) · [Full-size ecosystem](assets/service-ecosystem.svg)

A selected view of the tools and applications I use, grouped by responsibility rather than physical location. I also explore AI-assisted operational workflows as independent experiments. This is not a complete or live service inventory.

<details><summary>Accessible text version of the ecosystem</summary>

- Delivery: Forgejo, Docker, Dockhand, Renovate
- Observability: Grafana, Prometheus, Checkmk, Uptime Kuma
- Networking: Tailscale, AdGuard Home, Unbound
- Media: Frigate, Immich, Plex
- Security and recovery: Infisical, Trivy, Borg, Restic
- Automation: AI-assisted operational experiments

</details>

[Logo sources and attribution](assets/README.md)

## 01 · How everything fits together

[![Platform layers](assets/platform-layers.svg)](assets/platform-layers.svg)

[Detailed architecture and host roles](architecture/overview.md)

*Logical architecture, not a physical network map.*

## 02 · How a change reaches the hosts

[![Illustrative animated deployment flow](assets/deployment-flow.svg)](assets/deployment-flow.svg)

*Conceptual animation, not live status. One 4.8-second cycle; reduced-motion preferences disable the animation. The detailed decision flow is in the deployment documentation.*

The manifest determines which changed stacks are eligible for deployment. Documentation-only changes and excluded stacks do not deploy. Independent stack failures are reported without treating revision verification as an application health check. Dependencies define ordering, not application health. A deployed revision confirms the configuration version, not the health of every service.

[Explore the deployment workflow →](ci-cd/deployment-workflow.md) · [See the 11 quality gates →](ci-cd/quality-gates.md)

## 03 · Designing for recovery

[![Recovery model](assets/recovery-map.svg)](assets/recovery-map.svg)

*Restore verification is a separate activity, not a claim that every restore has been tested.*

I treat a successful backup and a proven restore as different things. Offsite coverage is selective, and recovery confidence depends on verification.

[Read about disaster recovery →](reliability/disaster-recovery.md)

## 04 · Engineering decisions worth documenting

| Topic | Why it matters |
| --- | --- |
| [Architecture and host roles](architecture/overview.md) | Understanding where responsibilities belong |
| [Changing the deployment engine](case-studies/deployment-migration.md) | Separating policy from execution and recognizing an untested fallback |
| [Observability](reliability/observability.md) | Detecting failures, including missing scheduled activity |
| [Secrets management](security/secrets-management.md) | Keeping credentials out of versioned configuration |
| [Synthetic examples](examples/README.md) | Exploring Compose and deployment policy without exposing live configuration |

## What's next?

I'm working toward stronger recovery confidence and easier-to-verify infrastructure changes. One known gap is the untested return path to the former deployment engine. Keeping an older tool available is not the same as proving recovery.

> This is a public engineering portfolio, not a mirror of my private homelab. Network details, private identifiers, credentials, live configurations and operational paths are deliberately omitted. Examples are synthetic.

[Back to my GitHub profile](https://github.com/dorko87)
