"""
Part 3 -- lint the Docker files. No Docker needed.

Docker will tell you a build FAILED. It will not tell you your image works but
leaks your API key, or that every one-line edit reinstalls every dependency.
These tests read the files and check the things Docker never complains about.

They are a substitute for reading carefully, not for running it: once they
pass, run `docker compose config` and `docker compose up --build` for real.
"""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent


# ---- a tiny Dockerfile reader -----------------------------------------------------


def stages(path="Dockerfile") -> dict[str, list[tuple[str, str]]]:
    """{stage name: [(INSTRUCTION, arguments), ...]} with continuations joined."""
    text = (ROOT / path).read_text()
    text = re.sub(r"\\\s*\n", " ", text)  # join line continuations
    result: dict[str, list[tuple[str, str]]] = {}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        keyword, _, args = line.partition(" ")
        keyword = keyword.upper()
        if keyword == "FROM":
            m = re.search(r"\bAS\s+(\S+)", args, re.I)
            current = m.group(1) if m else f"stage{len(result)}"
            result[current] = []
        if current is not None:
            result[current].append((keyword, args.strip()))
    return result


def all_instructions(path="Dockerfile"):
    return [i for stage in stages(path).values() for i in stage]


# ---- TODO 1: the Dockerfile ---------------------------------------------------------


def test_requirements_are_copied_and_installed_in_their_own_layer():
    base = stages()["base"]
    kinds = [(k, a) for k, a in base if k in {"COPY", "RUN"}]
    copy_at = next((i for i, (k, a) in enumerate(kinds) if k == "COPY" and "requirements.txt" in a), None)
    pip_at = next((i for i, (k, a) in enumerate(kinds) if k == "RUN" and "pip install -r requirements.txt" in a), None)
    assert copy_at is not None, "TODO 1a: COPY requirements.txt in the base stage"
    assert pip_at is not None, "TODO 1a: RUN pip install -r requirements.txt in the base stage"
    assert copy_at < pip_at, "copy requirements.txt BEFORE you install it"


def test_code_is_never_copied_before_dependencies_are_installed():
    """`COPY . .` first means every edit invalidates the pip layer."""
    for name, instructions in stages().items():
        pip_seen = False
        for keyword, args in instructions:
            if keyword == "RUN" and "pip install" in args:
                pip_seen = True
            if keyword == "COPY" and re.match(r"(\./?|\.)\s+\S+", args) and not pip_seen:
                pytest.fail(f"stage {name!r}: `COPY {args}` comes before pip install")


def test_dev_command_listens_on_all_interfaces():
    cmd = next((a for k, a in stages()["dev"] if k == "CMD"), None)
    assert cmd, "TODO 1b: write the dev CMD"
    assert "0.0.0.0" in cmd, "127.0.0.1 inside a container is the container itself: use --host 0.0.0.0"


def test_dev_command_reloads_only_the_app_folder():
    cmd = next((a for k, a in stages()["dev"] if k == "CMD"), "")
    assert "--reload" in cmd
    assert "--reload-dir" in cmd, "without it, uvicorn watches the whole working directory"


def test_commands_use_exec_form_so_signals_reach_the_server():
    for name, instructions in stages().items():
        for keyword, args in instructions:
            if keyword == "CMD":
                assert args.startswith("["), f"stage {name!r}: CMD must be a JSON list, not a shell string"


# ---- Given: the parts of the Dockerfile that are not TODOs -----------------------------


def test_python_version_is_pinned_to_a_minor_release():
    first = all_instructions()[0]
    assert first[0] == "FROM" and re.match(r"python:\d+\.\d+", first[1]), "pin the runtime: python:3.12-slim, not python:latest"


def test_prod_image_does_not_run_as_root_and_does_not_reload():
    prod = stages()["prod"]
    assert any(k == "USER" for k, _ in prod)
    assert not any("--reload" in a for k, a in prod if k == "CMD")


def test_nothing_ever_copies_the_env_file():
    for path in ("Dockerfile",):
        for keyword, args in all_instructions(path):
            assert not (keyword in {"COPY", "ADD"} and ".env" in args.split()), f"{keyword} {args}"


def test_dockerignore_keeps_secrets_and_clutter_out():
    entries = {
        line.strip() for line in (ROOT / ".dockerignore").read_text().splitlines() if line.strip() and not line.startswith("#")
    }
    for must in (".env", ".venv", ".git", "__pycache__"):
        assert must in entries, f".dockerignore must list {must}"


def test_dependencies_are_pinned_exactly():
    """'Works on my machine' includes 'on my SDK version'. Anthropic's SDK dropped
    `temperature` in a release; an unpinned requirement finds out in production."""
    lines = [
        ln.strip() for ln in (ROOT / "requirements.txt").read_text().splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    loose = [ln for ln in lines if "==" not in ln]
    assert not loose, f"pin these with ==: {loose}"


# ---- TODO 2: compose.yaml -------------------------------------------------------------------


@pytest.fixture
def compose():
    return yaml.safe_load((ROOT / "compose.yaml").read_text())


def test_compose_builds_the_dev_target(compose):
    assert compose["services"]["api"]["build"]["target"] == "dev"


def test_compose_publishes_port_8000(compose):
    ports = [str(p) for p in compose["services"]["api"].get("ports", [])]
    assert "8000:8000" in ports, "TODO 2: ports -- HOST:CONTAINER"


def test_compose_loads_config_from_env_file_at_run_time(compose):
    env_file = compose["services"]["api"].get("env_file")
    assert env_file, "TODO 2: env_file -- config arrives at RUN time, never baked into the image"
    paths = [e["path"] if isinstance(e, dict) else e for e in ([env_file] if isinstance(env_file, str) else env_file)]
    assert any(p in paths for p in (".env", "../.env", "../../.env"))


def test_compose_bind_mounts_the_code_for_hot_reload(compose):
    volumes = [str(v) for v in compose["services"]["api"].get("volumes", [])]
    assert "./app:/srv/app" in volumes, "TODO 2: volumes -- mount ./app at /srv/app"
    assert any(v.startswith("./tests:/srv/tests") for v in volumes), "also mount ./tests"
    assert any(v.startswith("./pytest.ini:/srv/pytest.ini") for v in volumes), "also mount ./pytest.ini"


# ---- Given: dev-mode and the proxy ------------------------------------------------------------


def test_compose_turns_on_dev_mode(compose):
    assert str(compose["services"]["api"]["environment"]["APP_DEBUG"]).lower() == "true"


def test_no_secret_is_written_into_compose(compose):
    text = (ROOT / "compose.yaml").read_text()
    assert "sk-" not in text and not re.search(r"API_KEY\s*[:=]\s*\S", text), "keys belong in .env"


def test_the_proxy_is_optional_and_waits_for_a_healthy_api(compose):
    proxy = compose["services"]["proxy"]
    assert proxy["profiles"] == ["proxy"]
    assert proxy["depends_on"]["api"]["condition"] == "service_healthy"
