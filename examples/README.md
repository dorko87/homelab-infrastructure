# Synthetic examples

These files illustrate two ideas from the homelab: a small Compose workload and a central deployment policy. They are newly written examples, not copied or redacted live files. The manifest is illustrative and has no bundled executor.

To validate the Compose example locally, use `docker compose -f docker-compose.yml config`. To run it, use `docker compose -f docker-compose.yml up -d`. It does not publish a host port. The example image tag is illustrative; review supported versions before use. The health check tests configuration syntax, not HTTP availability.
