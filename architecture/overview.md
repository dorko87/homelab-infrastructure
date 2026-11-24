# Architecture overview

The environment is organized around five defined host roles, with container workloads distributed according to their resource and recovery needs. Git is the source of truth for stack definitions. Forgejo runs validation and deployment workflows; Dockhand is the active deployment engine. Infisical provides centralized secrets management. Monitoring and backup systems are separate operational concerns rather than implicit properties of the deployment pipeline.

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

The host roles include general application workloads, GPU workloads, backup, additional compute and offsite recovery. A defined host or stack is not necessarily online. The diagram intentionally omits physical topology and access details.

## Design choices

- Keep deployment policy separate from the executor and from documentation policy.
- Use versioned container definitions, rather than relying on moving image tags.
- Keep operational documentation and configuration changes in the same review process.
- Treat deployment success, application health and recoverability as distinct checks.

## Defined host roles

```mermaid
flowchart TD
    H["Defined host roles · 5"]
    H --> A["General applications"]
    H --> B["GPU workloads"]
    H --> C["Backup"]
    H --> D["Additional compute"]
    H --> E["Offsite recovery"]
    class H control;
    class A,B,D runtime;
    class C,E recovery;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```

*Logical responsibilities; not a live inventory.*
