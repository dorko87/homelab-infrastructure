# Backup and disaster recovery

The repository maintains a backup inventory organized by priority and recovery requirements. It distinguishes database backups, configuration and credential-related data, and the offsite backup tier. Restic and Borg are among the tools used.

A copy on the same storage failure domain is not an independent backup. For databases, copying live volume files may leave an inconsistent backup. The documented approach includes database-native dumps.

The inventory explicitly distinguishes covered, deferred and externally managed targets. Offsite coverage is selective, not universal. Backup job success is not proof that restoration works. Restore drills and verification of backup freshness are important parts of recovery confidence.

No recovery commands, storage paths, retention policies, schedules or target identifiers are published here.

## Visual overview

```mermaid
flowchart LR
    A["Workload data"] --> B["Backup preparation"]
    C["Database-native dumps"] --> B
    B --> D["Local backup tier"]
    B --> E["Selective offsite tier"]
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

*Dashed arrows indicate verification activities, not completed restore tests.*
