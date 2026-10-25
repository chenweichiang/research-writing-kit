"""Tests for tools/submit/deadline.py (pure standard library, offline)."""
from conftest import run_tool


def run(*args, env=None):
    return run_tool("submit/deadline.py", *args, env=env)


def test_aoe_to_taipei_next_day():
    r = run("2026-10-26 23:59", "--tz", "AoE", "--to", "Asia/Taipei", "--now", "2026-10-25 12:00")
    assert r.returncode == 0, r.stderr
    assert "2026-10-27 19:59 (Tue)" in r.stdout
    assert "Remaining" in r.stdout
    assert "Suggested submit time: 2026-10-26 19:59 (Mon)" in r.stdout


def test_pdt_vs_pst_cross_day():
    out = run("2026-07-01 23:00", "--tz", "PST", "--to", "Asia/Taipei", "--now", "2026-06-01 00:00").stdout
    assert "2026-07-02 14:00" in out
    out = run("2026-12-01 23:00", "--tz", "PDT", "--to", "Asia/Taipei", "--now", "2026-11-01 00:00").stdout
    assert "2026-12-02 15:00" in out


def test_utc_offset_iana_jst_cet():
    base = ("--to", "Asia/Taipei", "--now", "2026-10-01 00:00")
    assert "2026-10-26 22:59" in run("2026-10-26 23:59", "--tz", "UTC+9", *base).stdout
    assert "2026-10-27 11:59" in run("2026-10-26 23:59", "--tz", "America/New_York", *base).stdout
    assert "2026-10-26 22:59" in run("2026-10-26 23:59", "--tz", "JST", *base).stdout
    assert "2026-10-27 06:59" in run("2026-10-26 23:59", "--tz", "CET", *base).stdout


def test_expired():
    r = run("2026-10-01 12:00", "--tz", "UTC+8", "--to", "Asia/Taipei", "--now", "2026-10-02 12:00")
    assert r.returncode == 0
    assert "Expired: 1d 0h" in r.stdout


def test_default_target_is_local_timezone():
    # no --to: the machine's local zone (forced through TZ here); UTC+9 noon is 03:00 UTC
    r = run("2026-10-26 12:00", "--tz", "UTC+9", "--now", "2026-10-01 00:00", env={"TZ": "UTC"})
    assert r.returncode == 0, r.stderr
    assert "Converted: 2026-10-26 03:00 (Mon)" in r.stdout


def test_unknown_tz_exit_2():
    r = run("2026-10-26 23:59", "--tz", "NOWHERE")
    assert r.returncode == 2
    assert "unrecognised" in r.stderr


def test_bad_time_exit_2():
    assert run("tomorrow", "--tz", "AoE").returncode == 2
