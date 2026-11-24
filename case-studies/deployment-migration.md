# Changing the deployment engine

## The problem

I wanted a more maintainable deployment workflow without coupling the entire repository to a single orchestration tool.

## The approach

The migration from Komodo to Dockhand separates policy from execution. Git defines the desired configuration, a manifest determines what can deploy, and the planner identifies changed stacks before validation and preflight. Dockhand handles deployment and the workflow checks the deployed revision.

## Current state

The source snapshot documents Dockhand as the active executor. Komodo is retained but inactive; its former executor and runtime switch were removed from the pipeline. Returning to the former mechanism would require a deliberate change, not an automatic switch.

## Remaining gap

The runbook explicitly records that the fallback drill was not performed. I therefore treat fallback as unproven. The key lesson is that retaining a tool is not equivalent to testing recovery. Canary validation is useful for changes to the active deployment engine, but does not establish fallback readiness.
