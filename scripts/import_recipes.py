#!/usr/bin/env python3
"""Convert YAML recipes to Hugo content markdown files."""

import math
import pathlib
import re
from typing import Any

import yaml

RECIPES_DIR = pathlib.Path("recipes")
OUTPUT_DIR = pathlib.Path("content/recipes")


def slug(name: str) -> str:
    s = name.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    return s


def extract_title(content: str) -> str:
    m = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def compute_color_ebc(fermentables: list[dict[str, Any]], batch_size_l: float) -> float:
    """Estimate beer color using Morey's formula."""
    volume_gallons = batch_size_l / 3.78541
    mcu: float = 0.0
    for f in fermentables:
        mcu += (
            (float(f.get("amount_kg", 0)) * 2.20462)
            * (float(f.get("color_ebc", 0)) / 1.97)
            / volume_gallons
        )
    srm: float = 1.4922 * (mcu**0.6859)
    return round(srm * 1.97, 1)


def compute_ibu(hops: list[dict[str, Any]], batch_size_l: float) -> float:
    """Estimate bitterness using Tinseth formula (assumes 1.050 boil gravity)."""
    boil_gravity = 1.050
    bigness = 1.65 * (0.000125 ** (boil_gravity - 1))
    total_ibu = 0.0
    for h in hops:
        if h.get("use", "").lower() != "boil":
            continue
        time_min = h.get("time_min", 0)
        boil_factor = (1 - math.exp(-0.04 * time_min)) / 4.15
        utilization = bigness * boil_factor
        alpha = h.get("alpha", 0.0) / 100
        amount_g = h.get("amount_g", 0)
        total_ibu += (alpha * amount_g * utilization * 1000) / batch_size_l
    return round(total_ibu, 1)


def compute_estimates(data: dict[str, Any]) -> list[str]:
    batch_size_l = data.get("batch_size_l")
    if not batch_size_l:
        return []
    lines = []
    fermentables = data.get("fermentables") or []
    hops = data.get("hops") or []
    if fermentables:
        lines.append(f"est_color_ebc: {compute_color_ebc(fermentables, batch_size_l)}")
    if hops:
        lines.append(f"est_ibu: {compute_ibu(hops, batch_size_l)}")
    return lines


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_files = sorted(RECIPES_DIR.glob("*.yaml"))
    if not yaml_files:
        print("No YAML files found in recipes/")
        return
    for yaml_file in yaml_files:
        content = yaml_file.read_text(encoding="utf-8")
        title = extract_title(content)
        if not title:
            print(f"  skipping {yaml_file} (no title found)")
            continue
        data: dict[str, Any] = yaml.safe_load(content) or {}
        estimates = compute_estimates(data)
        prefix = "\n".join(estimates) + "\n" if estimates else ""
        fname = OUTPUT_DIR / f"{slug(title)}.md"
        fname.write_text(f"---\n{prefix}{content}---\n", encoding="utf-8")
        print(f"  wrote {fname}")


if __name__ == "__main__":
    main()
