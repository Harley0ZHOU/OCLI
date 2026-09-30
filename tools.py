import os
import subprocess
import json
from pathlib import Path
WORK_DIR = Path.cwd()

def safe_file_path(filename):
    target = (WORK_DIR / filename).resolve()

    try:
        target.relative_to(WORK_DIR)
    except ValueError:
        raise PermissionError("只能操作当前工作目录内的文件")

    return target


def write_file(filename, content, mode="create"):
    target = safe_file_path(filename)

    if mode == "create" and target.exists():
        return f"文件已存在，未覆盖：{filename}"

    target.parent.mkdir(parents=True, exist_ok=True)

    if mode == "append":
        file_mode = "a"
    else:
        file_mode = "w"

    with target.open(file_mode, encoding="utf-8") as file:
        file.write(content)

    return f"文件已写入：{filename}"

def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)

def clear_screen():
    if os.name == "nt":
        # Windows
        subprocess.run(["cmd", "/c", "cls"], check=False)
    else:
        # macOS / Linux
        subprocess.run(["clear"], check=False)