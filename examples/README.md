# Synthetic examples

These examples show a small Compose workload, a deployment policy and a [read-only deployment planner](deployment-planner/README.md). They are newly written examples, not copied or redacted live files. The manifest is illustrative and has no bundled executor.

To validate the Compose example locally, use `docker compose -f docker-compose.yml config`. To run it, use `docker compose -f docker-compose.yml up -d`. It does not publish a host port. The example image tag is illustrative; review supported versions before use. The health check tests configuration syntax, not HTTP availability.
