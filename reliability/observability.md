# Observability

The homelab uses monitoring components including Prometheus, Grafana and Checkmk. I use monitoring to understand infrastructure and service behavior rather than assuming a successful deployment means everything is healthy.

An operational lesson documented in the repository is that a scheduled task cannot reliably detect its own absence. Monitoring for silence requires an independent check of whether expected activity occurred. This matters for dependency updates, backups and other recurring operations.

The public portfolio does not reproduce live dashboards, alert destinations, monitoring targets or operational thresholds.

## Visual overview

```mermaid
flowchart TD
    A["Workloads and infrastructure"] --> B["Metrics and health signals"]
    B --> C["Monitoring tools"]
    D["Expected scheduled activity"] --> E["Independent freshness check"]
    E --> F["Detect missing activity"]
    class A,B source;
    class C,E runtime;
    class D control;
    class F recovery;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```
