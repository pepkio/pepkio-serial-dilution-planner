"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "serial-dilution-planner",
        "title": "Serial Dilution Planner",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "standard_4step",
                "input": {
                    "stock_concentration": 10,
                    "stock_unit": "mM",
                    "target_concentration": 10,
                    "target_unit": "uM",
                    "num_steps": 4,
                    "final_volume_ul": 100,
                    "economy_mode": False,
                },
                "output": {"summary": {"step_count": 4}},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "steps": [{"step": 1, "transfer_ul": 18}],
            "summary": {"step_count": 4, "warning_count": 0},
            "notes": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
