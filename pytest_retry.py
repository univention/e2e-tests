#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import argparse
import json
import logging
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

log = logging.getLogger(__name__)

BACKUP_DIR_BASE_NAME = "run_"

# https://docs.pytest.org/en/stable/reference/exit-codes.html
PYTEST_EXIT_TESTS_FAILED = 1


def run_pytest(pytest_args: list[str], rerun_failed: bool) -> int:
    pytest_path = shutil.which("pytest")
    if not pytest_path:
        log.error("'pytest' not found. Quitting")
        return 127

    args = [pytest_path, *pytest_args]
    if rerun_failed:
        args.append("--lf")

    log.info("running pytest with args %s", args[1:])
    ret = subprocess.run(args)

    return ret.returncode


def backup_testrun_artifacts(artifacts: list[str], dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    for artifact in artifacts:
        src = Path(artifact)
        dest = dest_dir / src
        if not src.exists():
            continue

        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def restore_testrun_artifacts(artifacts: list[str], artifacts_dir: Path):
    for artifact in artifacts:
        src = artifacts_dir / artifact
        dest = Path.cwd() / artifact
        if not src.exists():
            continue
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def count_test_failures(junit_xml: Path, test_details: dict[str, int]) -> int:
    if not junit_xml.exists():
        return 0
    tree = ET.parse(junit_xml)
    testcases = tree.findall(".//testcase")
    total_failures = 0
    for testcase in testcases:
        name = testcase.get("name", "<unknown>")
        classname = testcase.get("classname", "<unknown>")
        full_name = f"{classname}::{name}"
        failure_node = testcase.find("failure")
        error_node = testcase.find("error")

        if failure_node is None and error_node is None:
            continue

        test_details[full_name] += 1
        total_failures += 1

    return total_failures


def do_first_run(args, test_details: dict[str, int], artifacts_dir: Path) -> int:
    return_code = run_pytest(args.pytest_args, rerun_failed=False)

    backup_testrun_artifacts(args.backup, artifacts_dir)
    if args.junit_xml:
        test_failures = count_test_failures(Path(args.junit_xml), test_details)
        if test_failures > args.max_retry_failures:
            log.info("More than %d tests failed. Not re-running", args.max_retry_failures)
            return -1

    return return_code


def print_summary(test_details: dict[str, int], runs_count: int):
    """
    Continuously failing: failed in all parsed runs
    Flaky: failed in at least one but not all.
    """
    if runs_count == 0 or not test_details:
        log.info("No JUnit XML parsed or no failures recorded; no summary.")
        return

    continuously = sorted([test for test, count in test_details.items() if count == runs_count])
    flaky = sorted([test for test, count in test_details.items() if 0 < count < runs_count])
    log.info("Summary after %d run(s):", runs_count)

    def log_group(title: str, items: list[str]):
        log.info("  %s (%d):", title, len(items))
        if items:
            for it in items:
                log.info("    - %s", it)
        else:
            log.info("    (none)")

    log_group("Continuously failing", continuously)
    log_group("Flaky (recovered)", flaky)


def relpath_arg(value: str) -> Path:
    """Argparse type: require a path that's relative to CWD and not containing '..'."""
    if not value:
        raise argparse.ArgumentTypeError("--backup paths must be non-empty")
    p = Path(value)
    if p.is_absolute():
        raise argparse.ArgumentTypeError(f"Path must be relative to current workspace: {value}")
    if any(part == ".." for part in p.parts):
        raise argparse.ArgumentTypeError(f"Path must not contain '..': {value}")

    cwd = Path.cwd().resolve()
    if not (cwd / p).resolve().is_relative_to(cwd):
        raise argparse.ArgumentTypeError(f"Path escapes workspace: {value}")
    return p


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s (%(levelname)s): %(message)s", datefmt="%Y-%m-%d %H:%M:%S %Z"
    )
    parser = argparse.ArgumentParser(
        description="Pytest wrapper that retries failed tests while preserving original test artifacts."
    )

    parser.add_argument("-r", "--retry", type=int, default=2, help="Retry attempts (default: 2)")
    parser.add_argument("-w", "--wait", type=int, default=10, help="Seconds to wait between retries (default: 10)")
    parser.add_argument(
        "-b", "--backup", action="append", default=[], type=relpath_arg, help="Artifact path to snapshot (repeatable)"
    )
    parser.add_argument(
        "-j",
        "--junitxml",
        default="",
        dest="junit_xml",
        type=relpath_arg,
        help="Path to JUnit XML (also pass to pytest). Auto-snapshotted.",
    )
    parser.add_argument(
        "-m", "--max-retry-failures", type=int, default=5, help="Only retry if failures+errors <= N (default: 5)"
    )
    parser.add_argument(
        "pytest_args", nargs="*", help="Arguments passed to pytest. Seperate from args to the wraper with a '--'"
    )

    args = parser.parse_args()
    if args.junit_xml:
        args.backup.append(args.junit_xml)

    test_details = defaultdict(int)
    log.info("Starting test run with %d retries", args.retry)
    if (rc := do_first_run(args, test_details, Path(BACKUP_DIR_BASE_NAME + "0"))) != PYTEST_EXIT_TESTS_FAILED:
        return rc

    runs_count = 1

    rc = -1
    for i in range(1, args.retry + 1):
        log.info("ATTEMPT %d/%d: sleeping %d seconds", i, args.retry, args.wait)
        time.sleep(args.wait)
        log.info("ATTEMPT %d/%d: re-running failed tests", i, args.retry)

        # DEBUG: Check pytest cache
        cache_file = Path(".pytest_cache/v/cache/lastfailed")
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    cache_contents = json.load(f)
                    log.info("Pytest cache contains %d failed test(s): %s", len(cache_contents), cache_contents)
            except Exception as e:
                log.warning("Failed to read cache file: %s", e)
        else:
            log.warning("Pytest cache file does not exist at %s", cache_file)

        rc = run_pytest(args.pytest_args, rerun_failed=True)
        backup_testrun_artifacts(args.backup, Path(BACKUP_DIR_BASE_NAME + str(i)))
        if args.junit_xml:
            count_test_failures(Path(args.junit_xml), test_details)
        runs_count += 1

        if rc != PYTEST_EXIT_TESTS_FAILED:
            break

    restore_testrun_artifacts(args.backup, Path(BACKUP_DIR_BASE_NAME + "0"))
    if args.junit_xml:
        print_summary(test_details, runs_count)
    return rc


if __name__ == "__main__":
    sys.exit(main())
