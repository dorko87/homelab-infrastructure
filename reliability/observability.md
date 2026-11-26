# Observability

I use Prometheus, Grafana and Checkmk to monitor infrastructure and services. A successful deployment does not tell me whether the application is healthy.

A scheduled task cannot report an error if it never starts. A separate check needs to look for missing activity. This matters for dependency updates, backups and other recurring operations.

See [detecting silent failures](../case-studies/detecting-silent-failures.md) for an example investigation. Live dashboards and monitoring details are not included here.

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
