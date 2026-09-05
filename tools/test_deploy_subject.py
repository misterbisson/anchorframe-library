"""The OIDC subject this repository's deploy job will present.

The role it assumes lives in `misterbisson/anchorframe-site`, which cannot read
this file, and this file cannot read that role. So the same literal is pinned on
both sides — here, and in that repository's `tools/test_oidc_subjects.py` under
`EXTERNAL_ROLES` — and each side fails when its own half drifts.

The rule GitHub applies, which is the whole subtlety:

    job with `environment: X`   ->  repo:OWNER/REPO:environment:X
    job on pull_request         ->  repo:OWNER/REPO:pull_request
    job on push to main         ->  repo:OWNER/REPO:ref:refs/heads/main

An `environment:` **replaces** the ref form rather than adding to it, so adding
one to a working job breaks it. The symptom is not a clear error:
configure-aws-credentials retries for about a minute and reports only "Not
authorized to perform sts:AssumeRoleWithWebIdentity", naming neither the subject
it presented nor the one the role expected.

The stake here is higher than a broken deploy. This repository is public and
takes pull requests from people nobody vets in advance, and the bucket it writes
to also serves the App Store listing's privacy policy URL. A `pull_request`
subject reaching that role would be a stranger with write access to it.

Dependency-free on purpose: regex over one file, so it runs anywhere python3
does and cannot be broken by an install that fails.
"""

from __future__ import annotations

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEPLOY = ROOT / ".github" / "workflows" / "deploy.yml"

# What the role in misterbisson/anchorframe-site trusts. Change both or neither.
EXPECTED_SUBJECT_SUFFIX = "ref:refs/heads/main"


def deploy_text() -> str:
    return DEPLOY.read_text(encoding="utf-8")


def trigger_block() -> str:
    """Everything between `on:` and the next top-level key."""
    m = re.search(r"^on:\n(.*?)^\w", deploy_text(), re.S | re.M)
    assert m, "could not find the trigger block in deploy.yml"
    return m.group(1)


class DeploySubject(unittest.TestCase):
    def test_the_workflow_exists_and_assumes_a_role(self):
        # Guard the parser: a file whose shape these regexes cannot read
        # verifies nothing, and would do so quietly.
        self.assertTrue(DEPLOY.is_file(), "no deploy.yml")
        self.assertIn("role-to-assume", deploy_text(),
                      "deploy.yml no longer assumes a role; this check is asserting nothing")

    def test_no_pull_request_trigger(self):
        """A fork's pull request must never be able to reach the publish role."""
        self.assertNotIn(
            "pull_request", trigger_block(),
            "deploy.yml triggers on pull_request. The role in anchorframe-site "
            "trusts only ref:refs/heads/main so this would fail rather than leak "
            "-- but a trigger that only fails because IAM says no is a trap for "
            "whoever widens the trust policy next.",
        )

    def test_no_environment_on_the_publishing_job(self):
        """An `environment:` silently changes the subject to environment:<name>."""
        self.assertNotIn(
            "\n    environment:", deploy_text(),
            "the publish job declares an environment, which replaces the ref "
            f"subject. anchorframe-site's library_role trusts only "
            f"{EXPECTED_SUBJECT_SUFFIX!r}; add the environment subject there "
            "first, or remove this.",
        )

    def test_triggers_only_present_the_pinned_subject(self):
        """push-to-main and workflow_dispatch both present the ref form. Nothing else may."""
        block = trigger_block()
        found = set(re.findall(r"^  (\w+):", block, re.M))
        self.assertTrue(found, "parsed no triggers out of deploy.yml")
        self.assertLessEqual(
            found, {"push", "workflow_dispatch"},
            f"deploy.yml triggers on {sorted(found)}. Anything beyond push and "
            "workflow_dispatch presents a subject the role does not trust.",
        )
        # `push:` must be pinned to main; a push subject carries whatever ref ran.
        push = re.search(r"^  push:\n((?:    .*\n)*)", block, re.M)
        self.assertTrue(push, "deploy.yml has no push trigger")
        self.assertIn("branches: [main]", push.group(1),
                      "the push trigger is not restricted to main, so it can "
                      "present ref:refs/heads/<other> and fail to assume the role")

    def test_the_role_arn_comes_from_a_variable_not_a_literal(self):
        self.assertRegex(
            deploy_text(), r"role-to-assume:\s*\$\{\{\s*vars\.LIBRARY_ROLE_ARN\s*\}\}",
            "the role ARN should come from vars.LIBRARY_ROLE_ARN, which "
            "anchorframe-site's `library_github_variables` output names",
        )

    def test_the_sync_cannot_reach_outside_the_library_prefix(self):
        """`--delete` scoped by the destination prefix, on every sync in the file."""
        for dest in re.findall(r"aws s3 sync \S+ \"(s3://[^\"]+)\"", deploy_text()):
            self.assertTrue(
                dest.endswith("/library/"),
                f"sync destination {dest!r} is not the library prefix. With "
                "--delete, a destination one level up deletes the whole site.",
            )


if __name__ == "__main__":
    unittest.main()
