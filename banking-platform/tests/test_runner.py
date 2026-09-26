import subprocess

import pytest
from tenacity import wait_none

import run_generation


def test_runner_retries_failed_generator_three_times(monkeypatch):
    attempts = {"count": 0}

    def fake_subprocess_run(*args, **kwargs):
        attempts["count"] += 1

        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=args[0]
        )

    monkeypatch.setattr(
        run_generation.subprocess,
        "run",
        fake_subprocess_run
    )

    test_runner = run_generation.run_generator.retry_with(
        wait=wait_none()
    )

    with pytest.raises(subprocess.CalledProcessError):
        test_runner(
            "mobile",
            "2026-07-01"
        )

    assert attempts["count"] == 3