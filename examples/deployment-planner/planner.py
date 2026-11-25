"""Synthetic, read-only deployment planning example. No deployment or network access."""
import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

class PolicyError(ValueError):
    pass

def relative(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise PolicyError("Expected a relative POSIX path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ("", ".", "..") for x in value.split("/")) or ":" in value:
        raise PolicyError(f"Invalid relative path: {value}")
    return p

def order(selected, deps):
    pending = set(selected)
    result = []
    while pending:
        ready = sorted(n for n in pending if not (set(deps[n]) & pending))
        if not ready:
            raise PolicyError("Dependency cycle: " + ", ".join(sorted(pending)))
        result.extend(ready)
        pending.difference_update(ready)
    return result

def plan(policy, changed, root):
    if not isinstance(policy, dict) or set(policy) != {"stacks", "excluded"}:
        raise PolicyError("Expected stacks and excluded mappings")
    active, excluded = policy["stacks"], policy["excluded"]
    if not isinstance(active, dict) or not isinstance(excluded, dict):
        raise PolicyError("Expected mappings")
    if set(active) & set(excluded):
        raise PolicyError("Stack classified twice")
    names = set(active) | set(excluded)
    for name in names:
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise PolicyError("Invalid stack name")
    deps = {}
    for name, spec in active.items():
        if not isinstance(spec, dict) or set(spec) != {"after"} or not isinstance(spec["after"], list):
            raise PolicyError(f"Invalid stack policy: {name}")
        after = spec["after"]
        if any(not isinstance(x, str) or x not in active for x in after) or len(set(after)) != len(after):
            raise PolicyError(f"Invalid dependency: {name}")
        deps[name] = after
    for name, reason in excluded.items():
        if not isinstance(reason, str) or not reason.strip():
            raise PolicyError(f"Missing exclusion reason: {name}")
    order(active, deps)  # reject cycles even if no affected stacks
    selected, skipped, ignored = set(), set(), set()
    for value in changed:
        p = relative(value)
        if p.parts[0] != "stacks":
            ignored.add(value)
            continue
        if len(p.parts) < 3 or p.parts[1] not in names:
            raise PolicyError(f"Unclassified stack path: {value}")
        name = p.parts[1]
        if p.suffix.lower() == ".md":
            ignored.add(value)
        elif name in excluded:
            skipped.add(name)
        else:
            selected.add(name)
    root = Path(root).resolve()
    for name in sorted(selected):
        compose = (root / "stacks" / name / "compose.yaml").resolve()
        if not compose.is_relative_to(root) or not compose.is_file():
            raise PolicyError(f"Missing or unsafe Compose definition: {name}")
    return {"mode": "dry-run", "deploy": order(selected, deps),
            "excluded": sorted(skipped), "ignored": sorted(ignored)}

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PolicyError(f"Duplicate policy key: {key}")
        result[key] = value
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("changed", nargs="*")
    args = parser.parse_args()
    try:
        policy = json.loads(args.manifest.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
        result = plan(policy, args.changed, args.root)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc), "mode": "dry-run"}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
