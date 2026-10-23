
#!/usr/bin/env python3

import argparse
import ast
import difflib
import shutil
import subprocess
import sys
from pathlib import Path

TARGET = Path("litellm/proxy/proxy_server.py")
START = "ui_link: Final ="
END = "\n\ndef cleanup_router_config_variables():"

NEW_BLOCK = '''### API DOCUMENTATION BRANDING ###
title: Final = os.getenv("DOCS_TITLE", "DCLLM API") if premium_user else "DCLLM API"

_title: Final = title
_description: Final = (
    os.getenv(
        "DOCS_DESCRIPTION",
        "DCLLM Proxy Server for calling 100+ LLMs through an OpenAI-compatible API.",
    )
    if premium_user
    else "DCLLM Proxy Server for calling 100+ LLMs through an OpenAI-compatible API."
)'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not TARGET.is_file():
        sys.exit(f"Target file not found: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")

    if original.count(START) != 1 or original.count(END) != 1:
        sys.exit("Unexpected replacement markers. No changes made.")

    start = original.index(START)
    end = original.index(END, start)
    old_block = original[start:end].rstrip("\n")

    if old_block == NEW_BLOCK:
        print("Already updated.")
        return

    if "LiteLLM API" not in old_block or "_description: Final =" not in old_block:
        sys.exit("Original branding block not recognized. No changes made.")

    updated = original[:start] + NEW_BLOCK + original[end:]

    print("".join(difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=str(TARGET),
        tofile=str(TARGET) + " (DCLLM)",
    )))

    if not args.apply:
        print("\nPreview only. Run with --apply to make the change.")
        return

    ast.parse(updated, filename=str(TARGET))

    backup = TARGET.with_suffix(TARGET.suffix + ".pre_dcllm")
    if backup.exists():
        sys.exit(f"Backup already exists: {backup}")

    shutil.copy2(TARGET, backup)

    try:
        TARGET.write_text(updated, encoding="utf-8")
        subprocess.run(
            [sys.executable, "-m", "py_compile", str(TARGET)],
            check=True,
        )
    except Exception:
        shutil.copy2(backup, TARGET)
        print("Validation failed. Original file restored.", file=sys.stderr)
        raise

    print(f"Updated {TARGET}")
    print(f"Backup saved to {backup}")


if __name__ == "__main__":
    main()
