# Visual assets

Service logos identify tools used in the independent homelab and do not imply endorsement. Logos remain subject to their respective owners' trademark and licensing terms.

- Forgejo: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/forgejo.svg)
- Docker: [source](https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg)
- Dockhand: [source](https://github.com/Finsys/dockhand/blob/main/static/logo.svg)
- Renovate: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/renovate.svg)
- Grafana: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/grafana.svg)
- Prometheus: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/prometheus.svg)
- Checkmk: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/checkmk.svg)
- Uptime Kuma: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/uptime-kuma.svg)
- Tailscale: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/tailscale.svg)
- AdGuard Home: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/adguard-home.svg)
- Unbound: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/unbound.svg)
- Frigate: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/frigate.svg)
- Immich: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/immich.svg)
- Plex: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/plex.svg)
- Infisical: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/infisical.svg)
- Trivy: [source](https://github.com/simple-icons/simple-icons/blob/develop/icons/trivy.svg)
- Borg: [source](https://github.com/homarr-labs/dashboard-icons/blob/main/svg/borg.svg)

Original diagrams are conceptual, not live telemetry.

## License and display notes

Upstream collection license texts retrieved in November 2026 are preserved here:

- [Dashboard Icons — Apache License 2.0](licenses/dashboard-icons.txt)
- [Simple Icons — CC0 1.0](licenses/simple-icons.txt)
- [Dockhand — upstream license terms](licenses/dockhand.txt)
- [Devicon — upstream license](licenses/devicon.txt)

The collection and software licenses do not by themselves grant trademark rights for every brand. The logos are used solely to identify the tools described, not to indicate affiliation or endorsement. Individual brand policies have not all been independently reviewed.

The ecosystem embeds isolated SVG images using data URIs rather than merging their CSS and IDs into a single namespace. Display copies use a common viewport; Dockhand uses a local symbol-only display variant with the wordmark path removed; the original remains in the icons directory. Infisical's editor metadata has been removed. The Docker tile uses the full-color Devicon artwork. Restic uses a generic backup symbol: the upstream logo is available as [PNG](https://github.com/restic/restic/blob/master/doc/logo/logo.png), not yet included locally.

## Validation

The public [service catalog](services.json) is the source for both generated ecosystem diagrams. Run `node scripts/generate_assets.mjs` from the repository root to regenerate them, then `node scripts/generate_assets.mjs --check` and `python3 scripts/validate_assets.py` to verify them. GitHub Actions runs the same structural checks. This validates XML, internal SVG references, embedded image data, active-content restrictions and relative links; it is not a browser-rendering, trademark-clearance or live-infrastructure audit.
