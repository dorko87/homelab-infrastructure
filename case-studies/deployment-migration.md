# Moving from Komodo to Dockhand

I wanted to change deployment tools without rewriting the whole deployment workflow. The main problem was deciding what should deploy independently of the tool that actually deploys it.

## What changed

I separated the deployment policy from the executor. Git holds the stack definitions, and a central manifest says which stacks can deploy and in what order. The planner identifies changed stacks before Compose validation and Dockhand preflight.

This means the executor does not need to decide which changes belong in a deployment. Documentation changes and excluded stacks are skipped. Dependencies set the order when both stacks are selected, rather than acting as application health checks.

## How changes are checked

The workflow checks the deployed revision against the merge revision. A missing Compose definition stops the selected deployment rather than allowing it to proceed with incomplete configuration. Independent stack failures are reported without stopping every unrelated attempt.

These checks establish which configuration was deployed. They do not prove that every application is healthy.

## Where things stand

Dockhand is the active executor in the documented snapshot. Komodo is still retained, but its former executor and runtime switch were removed. Returning to it would require a deliberate change.

The fallback drill was not performed. I do not count keeping the former tool available as a tested recovery method.

See the [deployment workflow](../ci-cd/deployment-workflow.md) and the [standalone planner example](../examples/deployment-planner/README.md).

## Visual overview

```mermaid
flowchart LR
    A["Earlier · Komodo"] --> B["Separate policy from execution"]
    B --> C["Current · Dockhand"]
    C -.-> D["Former engine retained"]
    D -.-> E["Fallback drill not performed"]
    class A source;
    class B control;
    class C runtime;
    class D recovery;
    class E caution;
    classDef source fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef control fill:#EDE9FE,stroke:#7C3AED,color:#2E1065,stroke-width:1.5px;
    classDef runtime fill:#CCFBF1,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef recovery fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:1.5px;
    classDef caution fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:1.5px;
```
