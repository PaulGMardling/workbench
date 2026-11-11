#!/usr/bin/env python3
"""Read-only static readiness checks; never repairs, installs or runs target Git."""

import argparse
import os
from pathlib import Path
import re
import shutil
import string
import subprocess
import sys

try:
    import yaml
except ImportError:
    yaml = None


def load_config(path):
    if yaml is None:
        raise ValueError("PyYAML is missing; use requirements-dev.txt in an authorised environment")

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            if not isinstance(key, str) or key in result:
                raise ValueError("configuration keys must be unique strings")
            result[key] = loader.construct_object(value_node)
        return result

    UniqueLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping
    )
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError("malformed YAML configuration") from exc


def text(value):
    return isinstance(value, str) and bool(value.strip())


def fields(value, allowed, required, label, errors):
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a mapping")
        return {}
    if set(value) - set(allowed):
        errors.append(f"{label}: unknown fields")
    if set(required) - set(value):
        errors.append(f"{label}: missing required fields")
    return value


def local_path(value):
    return text(value) and (value.startswith("/") or value.startswith("~/")) and "$" not in value


def config_errors(config, root, repository=None, environment=False, host="external", editor=None):
    errors = []
    c = fields(config, {"default", "copilotApp", "repositories"}, {"repositories"}, "config", errors)
    repos = c.get("repositories")
    if not isinstance(repos, dict) or not repos:
        return errors + ["repositories: expected a nonempty mapping"]
    if "default" in c and (not text(c["default"]) or c["default"] not in repos):
        errors.append("default: must identify a configured repository")
    app = fields(c.get("copilotApp", {}), {"ide"}, set(), "copilotApp", errors)
    if "ide" in app and not text(app["ide"]):
        errors.append("copilotApp.ide: expected an executable name or path")
    selected = repository
    if repository is not None and repository not in repos:
        return errors + ["repository selection: alias not configured"]
    for alias, raw in repos.items():
        if selected is not None and alias != selected:
            continue
        label = f"repositories.{alias}"
        if not text(alias):
            errors.append("repositories: aliases must be nonempty strings")
        entry = fields(raw, {"path", "worktreeRoot", "ide", "git", "branching", "overlays"},
                       {"path", "worktreeRoot", "ide", "git", "branching"}, label, errors)
        for key in ("path", "worktreeRoot"):
            if not local_path(entry.get(key)):
                errors.append(f"{label}.{key}: expected an absolute or ~/ path")
        if not text(entry.get("ide")):
            errors.append(f"{label}.ide: expected an executable name or path")
        git = fields(entry.get("git"), {"baseRemote", "pushRemote", "baseBranch"},
                     {"baseRemote", "pushRemote", "baseBranch"}, label + ".git", errors)
        for key in ("baseRemote", "pushRemote", "baseBranch"):
            if not text(git.get(key)):
                errors.append(f"{label}.git.{key}: expected a nonempty string")
        branch = fields(entry.get("branching"), {"explicitBranchRequired", "requiresAlias", "templates"},
                        set(), label + ".branching", errors)
        explicit = branch.get("explicitBranchRequired")
        templates = branch.get("templates")
        if "explicitBranchRequired" in branch and type(explicit) is not bool:
            errors.append(f"{label}.branching.explicitBranchRequired: expected a boolean")
        if "requiresAlias" in branch and type(branch["requiresAlias"]) is not bool:
            errors.append(f"{label}.branching.requiresAlias: expected a boolean")
        if explicit is True:
            if "templates" in branch or "requiresAlias" in branch:
                errors.append(f"{label}.branching: explicit strategy cannot also define templates/alias")
        elif not isinstance(templates, dict) or not templates:
            errors.append(f"{label}.branching: require explicitBranchRequired true or templates")
        if isinstance(templates, dict):
            for kind, template in templates.items():
                if not text(kind) or not text(template):
                    errors.append(f"{label}.branching.templates: expected nonempty types/templates")
                    continue
                try:
                    parts = list(string.Formatter().parse(template))
                    if any(name is not None and (
                        name not in {"alias", "identifier", "description"} or spec or conversion
                    ) for _, name, spec, conversion in parts):
                        raise ValueError("unsupported placeholder")
                except ValueError:
                    errors.append(f"{label}.branching.templates: unsupported placeholder or malformed template")
        overlays = entry.get("overlays", [])
        if not isinstance(overlays, list):
            errors.append(f"{label}.overlays: expected an array")
            overlays = []
        seen = set()
        for overlay in overlays:
            if not text(overlay):
                errors.append(f"{label}.overlays: expected nonempty relative paths")
                continue
            p = Path(overlay)
            resolved = (root / p).resolve()
            if p.is_absolute() or ".." in p.parts or root.resolve() not in resolved.parents or p.suffix != ".md":
                errors.append(f"{label}.overlays: path must be Markdown inside workbench")
                continue
            if overlay in seen:
                errors.append(f"{label}.overlays: duplicate path")
            seen.add(overlay)
            if environment:
                try:
                    resolved.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    errors.append(f"{label}.overlays: declared file missing or unreadable")
        if environment:
            if local_path(entry.get("path")):
                repo = Path(entry["path"]).expanduser()
                if not repo.is_dir() or not (repo / ".git").exists():
                    errors.append(f"{label}.path: missing directory or Git marker")
            if local_path(entry.get("worktreeRoot")):
                if not Path(entry["worktreeRoot"]).expanduser().parent.is_dir():
                    errors.append(f"{label}.worktreeRoot: parent directory missing")
            launcher = editor or (app.get("ide") if host == "copilot" else None) or entry.get("ide")
            if text(launcher):
                expanded = str(Path(launcher).expanduser())
                found = (Path(expanded).is_file() and os.access(expanded, os.X_OK)) if "/" in expanded else bool(shutil.which(expanded))
                if not found:
                    errors.append(f"{label}.ide: selected executable unavailable")
    return errors


def content_errors(root):
    """Inspect this workbench's tracked and nonignored files, not private overlays."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        capture_output=True, check=False,
    )
    if result.returncode:
        return ["content: cannot enumerate workbench Git files"]
    paths = set(result.stdout.decode().split("\0")) - {""}
    errors = []
    ignored = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "--no-index", "--stdin", "-z"],
        input=("\0".join(sorted(paths)) + "\0").encode(),
        capture_output=True, check=False,
    )
    if ignored.returncode not in (0, 1):
        errors.append("content: cannot verify publication allowlist")
    elif ignored.stdout:
        errors.append("content: tracked or selected files violate the publication allowlist")
    private = re.compile(
        r"/(?:Users|home)/[A-Za-z0-9_-]+/|https?://(?:dev\.azure\.com|[^/\s]+\.visualstudio\.com)/|"
        r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    )
    for rel in sorted(paths):
        path = root / rel
        if path.is_symlink() or not path.is_file():
            errors.append(f"{rel}: published paths must be regular files")
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{rel}: unreadable or non-text publication file")
            continue
        for number, line in enumerate(body.splitlines(), 1):
            if private.search(line):
                errors.append(f"{rel}:{number}: possible private path, internal URL or credential")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", body):
                if "://" in target or target.startswith("#"):
                    continue
                destination = (path.parent / target.split("#")[0]).resolve()
                try:
                    published = destination.relative_to(root.resolve()).as_posix()
                except ValueError:
                    published = None
                if published not in paths:
                    errors.append(f"{rel}: local Markdown link does not target a published file")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--config", type=Path, help="explicit local YAML; no automatic private reads")
    parser.add_argument("--repository", help="scope config checks to this exact alias")
    parser.add_argument("--environment", action="store_true", help="check local paths/editor/overlays, never target Git")
    parser.add_argument("--host", choices=("copilot", "external"), default="external")
    parser.add_argument("--editor", help="explicit executable override; never launched")
    args = parser.parse_args(argv)
    if (args.environment or args.repository or args.editor) and args.config is None:
        parser.error("--environment, --repository and --editor require --config")
    errors = content_errors(args.root)
    config_path = args.config or args.root / "config/repositories.example.yaml"
    try:
        config = load_config(config_path)
        errors.extend(config_errors(config, args.root, args.repository, args.environment, args.host, args.editor))
    except UnicodeError:
        errors.append("config: selected file must be UTF-8")
    except ValueError as exc:
        errors.append(f"config: {exc}")
    except OSError as exc:
        errors.append(f"config: cannot read selected file ({exc.strerror})")
    for error in errors:
        print("ERROR " + error, file=sys.stderr)
    print("Static readiness only: no target Git, network, authentication, runtime verification or repairs.")
    if errors:
        return 1
    print("PASS: publication links/patterns and selected configuration checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
