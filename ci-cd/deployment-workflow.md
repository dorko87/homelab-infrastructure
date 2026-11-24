# From merge to deployment

A merge to the main branch triggers a workflow that identifies changed runtime stacks. The central deployment manifest determines which stacks may deploy and their order. Documentation-only changes and excluded stacks do not trigger runtime deployment.

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

The workflow delegates planning and validation to scripts, and Dockhand performs the deployment. The manifest classifies every stack as deployable or excluded. Dependencies are ordering constraints when both stacks change; they are not health gates. A failure in one independent stack does not stop all other attempts, but the overall job reports failure. A missing Compose definition for a selected stack fails closed.

The deployed revision is checked against the merge revision. This confirms which configuration was deployed, not whether every application is healthy. Generated documentation is published after successful deployment. The public example manifest is intentionally simplified.
