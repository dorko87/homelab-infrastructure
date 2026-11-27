# Quality gates

The source snapshot defines eleven CI jobs covering these checks:

| Check | Purpose |
| --- | --- |
| Compose validation | Catch invalid container definitions |
| Workflow static analysis | Check workflow structure |
| Renovate validation | Check dependency-update configuration |
| Backup guards | Protect backup-related configuration |
| Trivy scanning | Identify security findings |
| Documentation checks | Keep required documentation present |
| Stack checks | Enforce stack conventions |
| New-stack completeness | Require supporting configuration and documentation |
| Deployment policy | Ensure every stack is classified |
| Secret hygiene | Detect inappropriate credential handling |
| Ticket reference | Support change traceability |

Branch protection and pull-request checks are documented in the private repository. Image updates are managed through Renovate, with review rules and exclusions. These checks catch some problems before deployment. I still need to check application health and plan for recovery.

## Visual overview

```mermaid
flowchart TD
    A["Pull request"] --> B["11 validation jobs"]
    B --> C["Configuration and workflow checks"]
    B --> D["Security and secret hygiene"]
    B --> E["Backup and deployment policy"]
    B --> F["Documentation and traceability"]
    C --> G["Review evidence"]
    D --> G
    E --> G
    F --> G
    class A source;
    class B control;
    class C,D,E,F runtime;
    class G recovery;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```
