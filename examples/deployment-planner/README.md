# Deployment planner example

This small Python example was written with AI assistance for the public portfolio. It illustrates the planning rules used in the homelab without copying private code. It has no deployment executor and makes no network requests.

Requires Python 3.10 or later. No third-party packages are needed. The manifest uses JSON syntax, which is a subset of YAML 1.2; arbitrary YAML syntax is not supported.

Run from this directory:

```sh
python3 planner.py --manifest deployments.yaml --root fixtures stacks/application/compose.yaml stacks/platform/compose.yaml stacks/manual/compose.yaml README.md
python3 -m unittest -v
```

See [sample output](sample-output.json). The planner takes explicit changed paths rather than invoking Git. Only selected stacks are ordered; an unchanged dependency is not deployed automatically. Excluded stacks and documentation changes are reported separately. Unknown stack paths, invalid policy, dependency cycles and missing selected Compose files fail with exit code 2. Compose syntax and application health are separate checks. No containers are started.

This is a simplified example, not the live homelab planner.
