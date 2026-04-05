#!/usr/bin/env python3
"""Convert BeerXML recipes to Hugo content markdown files."""

import xml.etree.ElementTree as ET
import pathlib
import re
import datetime

RECIPES_DIR = pathlib.Path("recipes")
OUTPUT_DIR = pathlib.Path("content/recipes")


def text(el: ET.Element, tag: str, default: str = "") -> str:
    child = el.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return default


def floatval(el: ET.Element, tag: str, default: float = 0.0) -> float:
    val = text(el, tag)
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def intval(el: ET.Element, tag: str, default: int = 0) -> int:
    val = text(el, tag)
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def slug(name: str) -> str:
    s = name.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    return s


def parse_date(date_str: str) -> str:
    if not date_str:
        return datetime.date.today().isoformat()
    for fmt in ("%d %b %y", "%d %b %Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(date_str, fmt).date().isoformat()
        except ValueError:
            continue
    return datetime.date.today().isoformat()


def yaml_str(val: object) -> str:
    """Safely quote a string value for YAML."""
    if val is None:
        return '""'
    s = str(val).replace('"', '\\"')
    return f'"{s}"'


def process_recipe(recipe_el: ET.Element) -> str:
    name = text(recipe_el, "NAME")
    date = parse_date(text(recipe_el, "DATE"))
    recipe_type = text(recipe_el, "TYPE")
    brewer = text(recipe_el, "BREWER")
    batch_size = floatval(recipe_el, "BATCH_SIZE")
    boil_time = intval(recipe_el, "BOIL_TIME")
    efficiency = floatval(recipe_el, "EFFICIENCY")
    est_og = floatval(recipe_el, "EST_OG")
    est_fg = floatval(recipe_el, "EST_FG")
    ibu = floatval(recipe_el, "IBU")
    est_abv = floatval(recipe_el, "EST_ABV")
    calories = intval(recipe_el, "CALORIES")
    est_color = floatval(recipe_el, "EST_COLOR")
    ibu_method = text(recipe_el, "IBU_METHOD")
    fermentation_stages = intval(recipe_el, "FERMENTATION_STAGES", 1)
    primary_age = intval(recipe_el, "PRIMARY_AGE")
    primary_temp = floatval(recipe_el, "PRIMARY_TEMP")
    notes = text(recipe_el, "NOTES")

    # Style
    style_el = recipe_el.find("STYLE")
    style_name = text(style_el, "NAME") if style_el is not None else ""
    style_category = text(style_el, "CATEGORY") if style_el is not None else ""
    style_guide = text(style_el, "STYLE_GUIDE") if style_el is not None else ""
    style_notes = text(style_el, "NOTES") if style_el is not None else ""

    lines = ["---"]
    lines.append(f"title: {yaml_str(name)}")
    lines.append(f"date: {date}")
    lines.append(f"recipe_type: {yaml_str(recipe_type)}")
    lines.append(f"brewer: {yaml_str(brewer)}")
    if style_name:
        lines.append(f"style_name: {yaml_str(style_name)}")
    if style_category:
        lines.append(f"style_category: {yaml_str(style_category)}")
    if style_guide:
        lines.append(f"style_guide: {yaml_str(style_guide)}")
    if style_notes:
        lines.append(f"style_notes: {yaml_str(style_notes)}")
    lines.append(f"batch_size: {batch_size}")
    lines.append(f"boil_time: {boil_time}")
    lines.append(f"efficiency: {efficiency}")
    lines.append(f"est_og: {est_og}")
    lines.append(f"est_fg: {est_fg}")
    lines.append(f"ibu: {ibu}")
    lines.append(f"est_abv: {est_abv}")
    lines.append(f"calories: {calories}")
    lines.append(f"est_color: {round(est_color, 2)}")
    lines.append(f"ibu_method: {yaml_str(ibu_method)}")
    lines.append(f"fermentation_stages: {fermentation_stages}")
    lines.append(f"primary_age: {primary_age}")
    lines.append(f"primary_temp: {primary_temp}")
    if notes:
        lines.append(f"notes: {yaml_str(notes)}")

    # Fermentables
    fermentables = recipe_el.findall("FERMENTABLES/FERMENTABLE")
    if fermentables:
        lines.append("fermentables:")
        for f in fermentables:
            lines.append(f"  - name: {yaml_str(text(f, 'NAME'))}")
            lines.append(f"    type: {yaml_str(text(f, 'TYPE'))}")
            lines.append(f"    amount_kg: {round(floatval(f, 'AMOUNT'), 3)}")
            lines.append(f"    yield_pct: {round(floatval(f, 'YIELD'), 1)}")
            lines.append(f"    color_ebc: {round(floatval(f, 'COLOR'), 2)}")

    # Hops
    hops = recipe_el.findall("HOPS/HOP")
    if hops:
        lines.append("hops:")
        for h in hops:
            amount_g = int(round(floatval(h, "AMOUNT") * 1000))
            lines.append(f"  - name: {yaml_str(text(h, 'NAME'))}")
            lines.append(f"    alpha: {floatval(h, 'ALPHA')}")
            lines.append(f"    amount_g: {amount_g}")
            lines.append(f"    use: {yaml_str(text(h, 'USE'))}")
            lines.append(f"    time_min: {intval(h, 'TIME')}")
            lines.append(f"    form: {yaml_str(text(h, 'FORM'))}")

    # Yeasts
    yeasts = recipe_el.findall("YEASTS/YEAST")
    if yeasts:
        lines.append("yeasts:")
        for y in yeasts:
            lines.append(f"  - name: {yaml_str(text(y, 'NAME'))}")
            lines.append(f"    form: {yaml_str(text(y, 'FORM'))}")
            display = text(y, "DISPLAY_AMOUNT") or text(y, "AMOUNT")
            lines.append(f"    display_amount: {yaml_str(display)}")
            attenuation = intval(y, "ATTENUATION")
            if attenuation:
                lines.append(f"    attenuation: {attenuation}")
            product_id = text(y, "PRODUCT_ID")
            if product_id:
                lines.append(f"    product_id: {yaml_str(product_id)}")
            laboratory = text(y, "LABORATORY")
            if laboratory:
                lines.append(f"    laboratory: {yaml_str(laboratory)}")

    # Miscs
    miscs = recipe_el.findall("MISCS/MISC")
    if miscs:
        lines.append("miscs:")
        for m in miscs:
            lines.append(f"  - name: {yaml_str(text(m, 'NAME'))}")
            lines.append(f"    use: {yaml_str(text(m, 'USE'))}")
            lines.append(f"    type: {yaml_str(text(m, 'TYPE'))}")
            lines.append(f"    time_min: {intval(m, 'TIME')}")
            display = text(m, "DISPLAY_AMOUNT")
            if display:
                lines.append(f"    display_amount: {yaml_str(display)}")
            else:
                lines.append(f"    amount: {floatval(m, 'AMOUNT')}")

    # Mash steps
    mash_steps = recipe_el.findall("MASH/MASH_STEPS/MASH_STEP")
    if mash_steps:
        lines.append("mash_steps:")
        for s in mash_steps:
            lines.append(f"  - name: {yaml_str(text(s, 'NAME'))}")
            lines.append(f"    type: {yaml_str(text(s, 'TYPE'))}")
            lines.append(f"    step_time: {intval(s, 'STEP_TIME')}")
            lines.append(f"    step_temp: {floatval(s, 'STEP_TEMP')}")
            lines.append(f"    end_temp: {floatval(s, 'END_TEMP')}")

    lines.append("---")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    xml_files = sorted(RECIPES_DIR.glob("*.xml"))
    if not xml_files:
        print("No XML files found in recipes/")
        return
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for recipe_el in root.findall("RECIPE"):
            name = text(recipe_el, "NAME")
            if not name:
                continue
            fname = OUTPUT_DIR / f"{slug(name)}.md"
            fname.write_text(process_recipe(recipe_el), encoding="utf-8")
            print(f"  wrote {fname}")


if __name__ == "__main__":
    main()
