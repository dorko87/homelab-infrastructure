# Secrets management

Configuration and credentials are handled separately. The private environment uses Infisical and repository-level secret hygiene checks, with deployment credentials scoped to the deployment workflow. The deployment runbook documents precautions against printing sensitive API responses.

For this public portfolio, all configuration examples are written from scratch. No private environment files, secret references, authentication settings, internal endpoints or live access policies are included. This is a documentation overview, not a disclosure of the security topology or a security audit of the live system.

## Visual overview

```mermaid
flowchart LR
    G["Git · versioned configuration"] --> C["Validation and deployment"]
    S["Infisical · credential material"] --> D["Deployment executor"]
    C --> D
    D --> R["Runtime workloads"]
    class G source;
    class C,S,D control;
    class R runtime;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```
