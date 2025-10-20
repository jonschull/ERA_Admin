"""Sharing wrapper for Fathom recordings."""
from __future__ import annotations

from scripts.share_fathom_call2 import share_fathom_recording


async def share_call(page, calls_url: str, email: str) -> bool:
    """Share a Fathom call URL to the given email.

    Thin wrapper to keep the orchestrator decoupled from the share implementation.
    Returns True on success, False on failure.
    """
    return await share_fathom_recording(page, calls_url, email)
