<p align="center"><img src="assets/hero.svg" alt="Homelab infrastructure — Build, Deploy, Observe, Recover" width="100%"></p>

# My Homelab Infrastructure

<p align="center"><strong>From a Git commit to a running service — and everything in between.</strong></p>

<p align="center">
  <img alt="Defined hosts: 5" src="https://img.shields.io/badge/Defined%20hosts-5-2563EB?style=for-the-badge">
  <img alt="Defined stacks: 39" src="https://img.shields.io/badge/Defined%20stacks-39-0D9488?style=for-the-badge">
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

The numbers above describe the documented repository snapshot, not a live inventory of running services.

## The tools behind the lab

| Source & deployment | Monitoring | Security & recovery |
| --- | --- | --- |
| ![Forgejo](https://img.shields.io/badge/Forgejo-FB923C?style=for-the-badge&logo=forgejo&logoColor=white) | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white) | ![Infisical](https://img.shields.io/badge/Infisical-475569?style=for-the-badge) |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white) | ![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=for-the-badge) |
| ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) | ![Checkmk](https://img.shields.io/badge/Checkmk-087F65?style=for-the-badge) | ![Restic](https://img.shields.io/badge/Restic-475569?style=for-the-badge) |
| ![Dockhand](https://img.shields.io/badge/Dockhand-2563EB?style=for-the-badge) | ![Renovate](https://img.shields.io/badge/Renovate-1A1F6C?style=for-the-badge&logo=renovate&logoColor=white) | ![Borg](https://img.shields.io/badge/Borg-475569?style=for-the-badge) |

## 01 · How everything fits together

```mermaid
flowchart TD
    G["Forgejo · Git"] --> Q["Pull request · CI checks"]
    Q --> P["Merge · deployment planner"]
    P --> V["Compose validation · preflight"]
    V --> D["Dockhand · deployment"]
    S["Infisical · secrets"] --> D
    D --> H["Multi-host Docker environment"]
    H --> O["Prometheus · Grafana · Checkmk"]
    H --> B["Backup · recovery"]
    B --> F["Selective offsite copies"]
    class G,Q source;
    class P,V,D,S control;
    class H,O runtime;
    class B,F recovery;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```

*Logical architecture, not a physical network map.*

| Area | Tools and responsibilities |
| --- | --- |
| Version control | Forgejo, Git, pull requests |
| Deployment | CI/CD, central policy, Docker Compose, Dockhand |
| Secrets | Infisical, separation of configuration and credentials |
| Observability | Prometheus, Grafana, Checkmk |
| Recovery | Restic, Borg, selective offsite backups |

## 02 · How a change reaches the hosts

![Illustrative animated deployment flow](assets/deployment-flow.svg)


```mermaid
flowchart TD
    A["Merge to main"] --> B["Identify changed stacks"]
    B --> C{"Eligible runtime change?"}
    C -->|No| N["No runtime deployment"]
    C -->|Yes| V["Validate Compose"]
    V --> P["Dockhand preflight"]
    P --> D["Deploy selected stacks"]
    D --> R["Verify deployed revision"]
    R --> E["Report outcome"]
    class A,B source;
    class C,V,P control;
    class D,R,E runtime;
    class N recovery;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```

The manifest determines which changed stacks are eligible for deployment. Dependencies define ordering, not application health. A deployed revision confirms the configuration version, not the health of every service.

[Explore the deployment workflow →](ci-cd/deployment-workflow.md) · [See the 11 quality gates →](ci-cd/quality-gates.md)

## 03 · Designing for recovery

```mermaid
flowchart LR
    A["Workload data"] --> B["Backup preparation"]
    C["Database-native dumps"] --> B
    B --> D["Local backup tier"]
    D --> E["Selective offsite tier"]
    D -.-> F["Restore verification"]
    E -.-> F
    F --> G["Recovery confidence"]
    class A,C source;
    class B control;
    class D,E recovery;
    class F,G runtime;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```

*The dashed paths represent verification activities, not a claim that every restore has been tested.*

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
