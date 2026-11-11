#!/usr/bin/env python3
"""Validate protocol-v1 report structure, not truth, applicability or authorization.

From the skill root: python3 scripts/validate_report.py examples/report.json
Only reads the supplied JSON. Never runs commands, follows locators or accesses
target repositories. An approved JSON record is not trusted user permission.

Protocol-v1 text fields are nonempty strings; ordered verification recipes are
arrays of nonempty step strings. Unknown extension fields are preserved/ignored.
Optional verification.requiredEvidenceIds and requiredCoverageAreas identify a
bounded required plan. Without them, verification.evidenceIds and all reported
coverage areas are treated as required when checking "complete".
"""

import argparse
import json
import re
import sys
from pathlib import Path


EXECUTION = {"not-run", "passed", "failed", "blocked", "unavailable"}
LIMITATION = (
    "Structural validation cannot establish evidence truth, standards applicability, "
    "revision immutability or mapping correctness, actual accessibility, trusted user "
    "approval, path authorization or publication permission."
)


class Validator:
    def __init__(self):
        self.errors = []

    def error(self, path, message):
        self.errors.append(f"{path}: {message}")

    def obj(self, value, path, fields):
        if not isinstance(value, dict):
            self.error(path, "must be an object")
            return {}
        for field in fields:
            if field not in value:
                self.error(f"{path}.{field}", "required field is missing")
        return value

    def text(self, value, path):
        if not isinstance(value, str) or not value.strip():
            self.error(path, "must be a nonempty string")
            return False
        return True

    def enum(self, value, path, values):
        if not isinstance(value, str) or value not in values:
            self.error(path, "must be one of " + ", ".join(sorted(values)))

    def array(self, value, path, nonempty=False):
        if not isinstance(value, list):
            self.error(path, "must be an array")
            return []
        if nonempty and not value:
            self.error(path, "must not be empty")
        return value

    def strings(self, value, path, nonempty=False):
        items = self.array(value, path, nonempty)
        for index, item in enumerate(items):
            self.text(item, f"{path}[{index}]")
        return items

    def records(self, value, path, fields, nonempty=False):
        result = []
        for index, item in enumerate(self.array(value, path, nonempty)):
            result.append(self.obj(item, f"{path}[{index}]", fields))
        return result

    def identifiers(self, records, prefix, path):
        found = {}
        for index, item in enumerate(records):
            identity = item.get("id")
            location = f"{path}[{index}].id"
            if not isinstance(identity, str) or not re.fullmatch(
                prefix + r"-[A-Za-z0-9][A-Za-z0-9._-]*", identity
            ):
                self.error(location, f"must be a {prefix}- prefixed identifier")
            elif identity in found:
                self.error(location, f"duplicate identifier {identity}")
            else:
                found[identity] = item
        return found

    def refs(self, value, path, known, nonempty=False):
        items = self.strings(value, path, nonempty)
        seen = set()
        for item in items:
            if not isinstance(item, str):
                continue
            if item not in known:
                self.error(path, f"unknown reference {item}")
            if item in seen:
                self.error(path, f"duplicate reference {item}")
            seen.add(item)
        return [item for item in items if isinstance(item, str)]


def usable(item):
    equivalence = item.get("equivalence")
    return (
        item.get("basis") != "hypothesis"
        and item.get("executionStatus") not in ("failed", "blocked", "unavailable")
        and (not isinstance(equivalence, dict) or equivalence.get("usableForVerdict") is True)
    )


def expectation(item):
    return usable(item) and (
        (item.get("kind") in ("standard", "contract") and item.get("basis") in ("source", "code-inspection"))
        or (item.get("kind") == "code" and item.get("basis") == "code-inspection")
    )


def observation(item):
    return usable(item) and (
        (item.get("kind") == "runtime" and item.get("basis") == "observed" and item.get("executionStatus") == "passed")
        or (item.get("kind") == "code" and item.get("basis") == "code-inspection")
    )


def known_revision(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() != "unknown"


def at_revision(item, revision, mappings):
    actual = item.get("revision")
    return known_revision(revision) and known_revision(actual) and (
        actual == revision
        or (item.get("kind") == "runtime" and (revision, actual) in mappings)
    )


def validate_report(report):
    """Return all discoverable errors; malformed JSON values must not crash."""
    v = Validator()
    r = v.obj(report, "$", (
        "protocolVersion", "runId", "stage", "scope", "capabilities", "evidence",
        "claims", "coverage", "challenges", "approval", "changes", "verification",
        "developerSummary",
    ))
    if type(r.get("protocolVersion")) is not int or r.get("protocolVersion") != 1:
        v.error("$.protocolVersion", "must be integer 1 (not a boolean)")
    for field in ("runId", "developerSummary"):
        v.text(r.get(field), f"$.{field}")
    v.enum(r.get("stage"), "$.stage", {"diagnosis", "awaiting-fix-approval", "implementation", "verification"})
    scope = v.obj(r.get("scope"), "$.scope", ("target", "revision", "boundary", "exclusions"))
    for field in ("target", "revision", "boundary"):
        v.text(scope.get(field), f"$.scope.{field}")
    v.strings(scope.get("exclusions"), "$.scope.exclusions")
    caps = v.records(r.get("capabilities"), "$.capabilities", ("name", "available", "authorized"))
    for index, cap in enumerate(caps):
        v.text(cap.get("name"), f"$.capabilities[{index}].name")
        for field in ("available", "authorized"):
            if type(cap.get(field)) is not bool:
                v.error(f"$.capabilities[{index}].{field}", "must be a boolean")

    evidence = v.records(r.get("evidence"), "$.evidence", (
        "id", "kind", "statement", "locator", "basis", "executionStatus",
        "revision", "environment", "supports", "contradicts", "limits",
    ))
    claims = v.records(r.get("claims"), "$.claims", (
        "id", "origin", "statement", "userImpact", "executionStatus", "verdict",
        "expectedBehavior", "actualBehavior", "remedy", "rootCause", "temporalStatus",
        "evidenceIds", "counterEvidenceIds", "reasoning", "nextAction", "verificationRecipe",
    ), nonempty=True)
    emap = v.identifiers(evidence, "E", "$.evidence")
    cmap = v.identifiers(claims, "C", "$.claims")
    for index, item in enumerate(evidence):
        p = f"$.evidence[{index}]"
        for field in ("statement", "locator", "revision"):
            v.text(item.get(field), f"{p}.{field}")
        v.enum(item.get("kind"), p + ".kind", {"report", "standard", "contract", "runtime", "code", "history", "approval"})
        v.enum(item.get("basis"), p + ".basis", {"observed", "code-inspection", "source", "hypothesis"})
        v.enum(item.get("executionStatus"), p + ".executionStatus", EXECUTION)
        env = v.obj(item.get("environment"), p + ".environment", ())
        if isinstance(item.get("environment"), dict) and not env:
            v.error(p + ".environment", "must record environment information (use explicit unknowns)")
        v.refs(item.get("supports"), p + ".supports", cmap)
        v.refs(item.get("contradicts"), p + ".contradicts", cmap)
        v.strings(item.get("limits"), p + ".limits")
        if item.get("kind") == "standard":
            v.enum(item.get("authority"), p + ".authority", {"normative", "informative", "advisory"})
        if item.get("kind") == "runtime":
            for field in ("command", "result"):
                v.text(item.get(field), f"{p}.{field}")
        if "equivalence" in item:
            eq = v.obj(item["equivalence"], p + ".equivalence", (
                "targets", "matchedInputs", "intentionalDifferences", "unknowns", "usableForVerdict",
            ))
            for field in ("targets", "matchedInputs", "intentionalDifferences", "unknowns"):
                v.strings(eq.get(field), p + ".equivalence." + field, field == "targets")
            if type(eq.get("usableForVerdict")) is not bool:
                v.error(p + ".equivalence.usableForVerdict", "must be a boolean")

    for index, claim in enumerate(claims):
        p = f"$.claims[{index}]"
        cid = claim.get("id")
        for field in ("statement", "userImpact", "expectedBehavior", "actualBehavior", "reasoning", "nextAction"):
            v.text(claim.get(field), f"{p}.{field}")
        v.enum(claim.get("origin"), p + ".origin", {"ticket", "audit"})
        v.enum(claim.get("executionStatus"), p + ".executionStatus", {"not-run", "reproduced", "not-reproduced", "blocked", "unavailable"})
        v.enum(claim.get("verdict"), p + ".verdict", {"confirmed-defect", "wrong-diagnosis-or-remedy", "no-defect-established", "already-corrected", "inconclusive"})
        v.enum(claim.get("remedy"), p + ".remedy", {"appropriate", "inappropriate", "unknown", "not-proposed"})
        v.enum(claim.get("temporalStatus"), p + ".temporalStatus", {"current", "already-corrected", "awaiting-consumption", "unknown"})
        root = v.obj(claim.get("rootCause"), p + ".rootCause", ("layer", "certainty"))
        v.enum(root.get("layer"), p + ".rootCause.layer", {"unknown", "expectation", "consumer", "example", "harness", "component", "content", "modern", "headless", "shared", "deployment", "browser", "assistive-technology"})
        v.enum(root.get("certainty"), p + ".rootCause.certainty", {"established", "supported", "unresolved"})
        ids = v.refs(claim.get("evidenceIds"), p + ".evidenceIds", emap)
        counters = v.refs(claim.get("counterEvidenceIds"), p + ".counterEvidenceIds", emap)
        v.strings(claim.get("verificationRecipe"), p + ".verificationRecipe", nonempty=True)
        for key, referenced, direction in (("evidenceIds", ids, "supports"), ("counterEvidenceIds", counters, "contradicts")):
            for eid in referenced:
                links = emap.get(eid, {}).get(direction)
                if eid in emap and (not isinstance(links, list) or cid not in links):
                    v.error(p + "." + key, f"{eid} must explicitly {direction} {cid}")
        linked = [emap[eid] for eid in ids + counters if eid in emap]
        if claim.get("verdict") not in (None, "inconclusive"):
            if not any(expectation(e) for e in linked):
                v.error(p + ".verdict", "conclusive verdict requires usable expectation evidence (standard, contract or inspected code)")
            if not any(observation(e) for e in linked):
                v.error(p + ".verdict", "conclusive verdict requires successful actual observation or decisive unexecuted code inspection, not hypothesis/failed tests")
            if claim.get("verdict") == "already-corrected" and not any(
                e.get("kind") == "history" and usable(e) for e in linked
            ):
                v.error(p + ".verdict", "already-corrected requires usable correction lineage evidence")

    coverage = v.records(r.get("coverage"), "$.coverage", ("area", "status", "reason"))
    areas = {}
    for index, item in enumerate(coverage):
        p = f"$.coverage[{index}]"
        for field in ("area", "reason"):
            v.text(item.get(field), f"{p}.{field}")
        v.enum(item.get("status"), p + ".status", {"covered", "not-applicable", "unavailable", "deferred"})
        if isinstance(item.get("area"), str):
            if item["area"] in areas:
                v.error(p + ".area", "duplicate coverage area")
            areas[item["area"]] = item
    challenges = v.records(r.get("challenges"), "$.challenges", ("claimIds", "status", "evidenceIds", "explanation"))
    for index, item in enumerate(challenges):
        p = f"$.challenges[{index}]"
        v.refs(item.get("claimIds"), p + ".claimIds", cmap, nonempty=True)
        v.enum(item.get("status"), p + ".status", {"resolved", "unresolved", "not-performed"})
        v.refs(item.get("evidenceIds"), p + ".evidenceIds", emap)
        v.text(item.get("explanation"), p + ".explanation")
    approval = v.obj(r.get("approval"), "$.approval", ("status", "source", "claimIds", "boundaries"))
    v.enum(approval.get("status"), "$.approval.status", {"not-requested", "pending", "approved", "denied", "revoked"})
    v.text(approval.get("source"), "$.approval.source")
    approved_ids = v.refs(approval.get("claimIds"), "$.approval.claimIds", cmap)
    v.strings(approval.get("boundaries"), "$.approval.boundaries", approval.get("status") == "approved")
    if approval.get("status") == "approved" and not approved_ids:
        v.error("$.approval.claimIds", "approved scope must include at least one claim")
    changes = v.records(r.get("changes"), "$.changes", ("claimIds", "paths", "revision"))
    if changes and r.get("stage") in ("diagnosis", "awaiting-fix-approval"):
        v.error("$.changes", "must be empty before approved implementation")
    if r.get("stage") in ("implementation", "verification") and approval.get("status") not in ("approved", "revoked"):
        v.error("$.approval.status", "implementation/verification requires approved scope or a halted revoked snapshot")
    # Revocation must preserve honest records of changes already made.
    if changes and approval.get("status") not in ("approved", "revoked"):
        v.error("$.changes", "source changes require recorded approval")
    for index, item in enumerate(changes):
        p = f"$.changes[{index}]"
        changed_ids = v.refs(item.get("claimIds"), p + ".claimIds", cmap, nonempty=True)
        v.strings(item.get("paths"), p + ".paths", nonempty=True)
        v.text(item.get("revision"), p + ".revision")
        for cid in changed_ids:
            if cid not in approved_ids:
                v.error(p + ".claimIds", f"{cid} is outside approved claim scope")
            claim = cmap.get(cid, {})
            linked = [emap[eid] for field in ("evidenceIds", "counterEvidenceIds")
                      for eid in (claim.get(field) if isinstance(claim.get(field), list) else [])
                      if isinstance(eid, str) and eid in emap]
            if cid in cmap and not any(expectation(e) for e in linked):
                v.error(p + ".claimIds", f"{cid} has no established expectation evidence")

    verification = v.obj(r.get("verification"), "$.verification", ("status", "evidenceIds", "limits"))
    v.enum(verification.get("status"), "$.verification.status", {"not-run", "partial", "complete"})
    verified = v.refs(verification.get("evidenceIds"), "$.verification.evidenceIds", emap)
    v.strings(verification.get("limits"), "$.verification.limits")
    fixed_revision = verification.get("fixedRevision")
    if "fixedRevision" in verification and not known_revision(fixed_revision):
        v.error("$.verification.fixedRevision", "must be a known nonempty revision ID (not unknown)")
    mappings = set()
    if "revisionMappings" in verification:
        for index, mapping in enumerate(v.records(
            verification["revisionMappings"], "$.verification.revisionMappings",
            ("sourceRevision", "runtimeRevision"),
        )):
            p = f"$.verification.revisionMappings[{index}]"
            for field in ("sourceRevision", "runtimeRevision"):
                if not known_revision(mapping.get(field)):
                    v.error(p + "." + field, "must be a known nonempty revision ID (not unknown)")
            if all(known_revision(mapping.get(field)) for field in ("sourceRevision", "runtimeRevision")):
                pair = (mapping["sourceRevision"], mapping["runtimeRevision"])
                if pair in mappings:
                    v.error(p, "duplicate revision mapping")
                mappings.add(pair)
    required = verified
    if "requiredEvidenceIds" in verification:
        required = v.refs(verification["requiredEvidenceIds"], "$.verification.requiredEvidenceIds", emap)
    required_areas = list(areas)
    if "requiredCoverageAreas" in verification:
        required_areas = v.refs(verification["requiredCoverageAreas"], "$.verification.requiredCoverageAreas", areas)
    if verification.get("status") == "complete":
        targets_by_claim = {cid: [] for cid in approved_ids}
        for change in changes:
            claim_ids = change.get("claimIds")
            for cid in claim_ids if isinstance(claim_ids, list) else []:
                if isinstance(cid, str) and cid in targets_by_claim:
                    targets_by_claim[cid].append(change.get("revision"))
        verification_only_ids = [cid for cid, targets in targets_by_claim.items() if not targets]
        if (not changes or verification_only_ids) and "fixedRevision" not in verification:
            v.error("$.verification.fixedRevision", "required for complete verification-only claims")
        for cid in verification_only_ids:
            targets_by_claim[cid].append(fixed_revision)
        bounded_targets = [revision for targets in targets_by_claim.values() for revision in targets]
        if r.get("stage") != "verification" or approval.get("status") != "approved":
            v.error("$.verification.status", "complete requires verification stage and approved bounded scope")
        if not required or not verified or not required_areas:
            v.error("$.verification.status", "complete requires nonempty required evidence and coverage")
        for eid in required:
            e = emap.get(eid, {})
            if eid not in verified or not usable(e) or not (
                observation(e) or expectation(e) or (e.get("kind") == "history" and e.get("basis") == "source")
            ):
                v.error("$.verification.status", f"required evidence {eid} is missing, failed, blocked or non-decisive")
            if observation(e):
                linked_claims = [
                    cid for cid in approved_ids
                    if any(isinstance(e.get(direction), list) and cid in e[direction]
                           for direction in ("supports", "contradicts"))
                ]
                target_groups = [targets_by_claim[cid] for cid in linked_claims] or [bounded_targets]
                if not all(any(at_revision(e, revision, mappings) for revision in targets)
                           for targets in target_groups):
                    v.error("$.verification.status", f"required evidence {eid} lacks observation/inspection at its actual fixed revision")
        for area in required_areas:
            if areas.get(area, {}).get("status") not in ("covered", "not-applicable"):
                v.error("$.verification.status", f"required coverage {area} is missing, unavailable or deferred")
        for cid in approved_ids:
            if not any(
                observation(emap.get(eid, {}))
                and any(at_revision(emap[eid], revision, mappings) for revision in targets_by_claim[cid])
                and any(
                    isinstance(emap[eid].get(direction), list)
                    and cid in emap[eid][direction]
                    for direction in ("supports", "contradicts")
                )
                for eid in verified if eid in emap
            ):
                v.error("$.verification.status", f"approved claim {cid} lacks actual observation/inspection at an identified revision"
                        + (" matching verification.fixedRevision" if cid in verification_only_ids else ""))
        for index, change in enumerate(changes):
            revision = change.get("revision")
            claim_ids = change.get("claimIds")
            for cid in claim_ids if isinstance(claim_ids, list) else []:
                if not isinstance(cid, str):
                    continue
                if not any(
                    at_revision(emap.get(eid, {}), revision, mappings)
                    and observation(emap.get(eid, {}))
                    and any(
                        isinstance(emap[eid].get(direction), list)
                        and cid in emap[eid][direction]
                        for direction in ("supports", "contradicts")
                    )
                    for eid in verified if eid in emap
                ):
                    v.error("$.verification.status", f"change {index} claim {cid} lacks observation/inspection evidence for its actual fixed revision")
    return v.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog=LIMITATION)
    parser.add_argument("report", type=Path, help="JSON report to read")
    args = parser.parse_args(argv)
    try:
        with args.report.open(encoding="utf-8") as handle:
            report = json.load(handle)
    except (OSError, ValueError, RecursionError) as exc:
        print(f"ERROR {args.report}: {exc}", file=sys.stderr)
        return 2
    errors = validate_report(report)
    if errors:
        for error in errors:
            print("ERROR " + error, file=sys.stderr)
        print(f"INVALID: {len(errors)} contract error(s). {LIMITATION}", file=sys.stderr)
        return 1
    print(f"VALID: protocol v1 structural checks passed. {LIMITATION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
