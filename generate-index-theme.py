#!/usr/bin/env python3
import os
from pathlib import Path

# --- Config you can tweak ---
ROOT = ROOT = Path(__file__).resolve().parent / "mint-l-icons-gruvbox-dark" # repo root where Mint-L*/ live
THEME_GLOB = "Mint-L*"             # which dirs count as themes
INHERITS = "hicolor"               # e.g. "Mint-L;hicolor" if you want fallback to Mint-L
COMMENT = "Mint-L Gruvbox icon theme variant"
SCALABLE_MIN = 16
SCALABLE_MAX = 512
DRY_RUN = False                    # set True to preview without writing
# ----------------------------

# Map folder name -> IndexTheme Context (Capitalized per spec)
CONTEXT_NAME = {
    "apps": "Apps",
    "actions": "Actions",
    "categories": "Categories",
    "devices": "Devices",
    "emblems": "Emblems",
    "mimetypes": "MimeTypes",
    "places": "Places",
    "status": "Status",
    "preferences": "Preferences",
    # add more if you use them
}

def list_theme_dirs(root: Path, pattern: str):
    return [p for p in root.glob(pattern) if p.is_dir()]

def find_directory_entries(theme_dir: Path):
    """
    Return a list of (section_name, section_kv_pairs_dict) for index.theme
    and the flat list of section names for Directories=.
    We recognize paths like:
      <context>/<size>
      <context>/<size>@2x
      <context>/scalable
      <context>/<size>x<size> (if present)
    Only directories (that exist) are included.
    """
    entries = []
    for context_dir in sorted([d for d in theme_dir.iterdir() if d.is_dir()]):
        context = context_dir.name  # e.g. 'places'
        context_cap = CONTEXT_NAME.get(context, context.capitalize())

        # consider immediate subdirs inside the context dir
        for d in sorted([p for p in context_dir.iterdir() if p.is_dir()]):
            name = d.name  # e.g. '16', '16@2x', 'scalable', '64x64'
            section = f"{context}/{name}"

            kv = {
                "Context": context_cap
            }

            lname = name.lower()
            if lname == "scalable":
                kv.update({
                    "Type": "Scalable",
                    "Size": str(SCALABLE_MIN),  # required; a nominal size
                    "MinSize": str(SCALABLE_MIN),
                    "MaxSize": str(SCALABLE_MAX),
                })
            else:
                # Fixed size (possibly with @2x)
                size_str = lname
                scale = None
                if "@2x" in size_str:
                    size_str, _ = size_str.split("@2x", 1)
                    scale = 2

                # accept forms like '16' or '64x64'
                if "x" in size_str:
                    base = size_str.split("x")[0]
                else:
                    base = size_str

                try:
                    size_val = int(base)
                except ValueError:
                    # skip odd folders that aren't numeric/scalable
                    continue

                kv.update({
                    "Type": "Fixed",
                    "Size": str(size_val)
                })
                if scale:
                    kv["Scale"] = str(scale)

            entries.append((section, kv))

    # Sort sections naturally by context then by numeric size where possible
    def sort_key(item):
        section, kv = item
        context, name = section.split("/", 1)
        size = kv.get("Size", "0")
        try:
            size_i = int(size)
        except ValueError:
            size_i = 0
        # prefer non-@2x before @2x for same size
        scale = int(kv.get("Scale", "1"))
        return (context, kv["Type"] != "Fixed", size_i, scale)

    entries.sort(key=sort_key)
    directories = [s for s, _ in entries]
    return entries, directories

def render_index_theme(name: str, directories: list[str], sections: list[tuple[str, dict]]):
    lines = []
    lines.append("[Icon Theme]")
    lines.append(f"Name={name}")
    lines.append(f"Comment={COMMENT}")
    lines.append(f"Inherits={INHERITS}")
    if directories:
        lines.append("Directories=" + ";".join(directories))
    else:
        lines.append("Directories=")

    lines.append("")  # blank line

    for section, kv in sections:
        lines.append(f"[{section}]")
        # order keys nicely
        key_order = ["Size", "Type", "MinSize", "MaxSize", "Scale", "Context"]
        for k in key_order:
            if k in kv:
                lines.append(f"{k}={kv[k]}")
        # include any unexpected keys at the end
        for k, v in kv.items():
            if k not in key_order:
                lines.append(f"{k}={v}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

def write_index(theme_dir: Path):
    name = theme_dir.name
    sections, dirs = find_directory_entries(theme_dir)
    content = render_index_theme(name, dirs, sections)
    out = theme_dir / "index.theme"
    if DRY_RUN:
        print(f"--- {out} (dry-run) ---")
        print(content)
    else:
        out.write_text(content, encoding="utf-8")
        print(f"Wrote {out}")

def main():
    theme_dirs = list_theme_dirs(ROOT, THEME_GLOB)
    if not theme_dirs:
        print(f"No theme directories matching {THEME_GLOB} under {ROOT}")
        return
    for tdir in theme_dirs:
        write_index(tdir)

if __name__ == "__main__":
    main()

