"""Collect article attributes, named entities, and candidate person-link data.

Run from the repository root:
    python -m src.analyze_wikipedia --title "Gabriela Mistral" --output-dir data
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import spacy
import wikipediaapi
from tqdm import tqdm

DEFAULT_TITLE = "Gabriela Mistral"
DEFAULT_OUTPUT = Path("data")


def clean_text(text: str) -> str:
    """Normalize newlines and repeated whitespace."""
    return re.sub(r"\s+", " ", text or "").strip()


def is_probably_person(title: str) -> bool:
    """A deliberately simple candidate filter, not a definitive person classifier."""
    title = title.strip()
    if not title or ":" in title:
        return False
    # Allows accented letters, apostrophes, periods, hyphens, and 2+ name tokens.
    tokens = title.split()
    if len(tokens) < 2:
        return False
    return all(token[:1].isupper() for token in tokens if token)


def _match(pattern: str, text: str, group: int = 1) -> str:
    found = re.search(pattern, text, flags=re.IGNORECASE)
    return found.group(group).strip(" ,.;") if found else "N/A"


def extract_biographical_attributes(text: str) -> dict[str, str]:
    """Extract approximate biographical fields with transparent regex heuristics."""
    text = clean_text(text)
    dob = _match(r"\b(?:born|birth)\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})", text)
    dod = _match(r"\b(?:died|death)\s+(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})", text)

    # Keep location capture conservative; these may still require manual review.
    pob = _match(
        r"\bborn\b.{0,100}?\bin\s+([A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ.'’ -]{1,60}?(?:,\s*[A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ.'’ -]+)?)"
        r"(?=[.;]|$)",
        text,
    )
    pod = _match(
        r"\bdied\b.{0,100}?\bin\s+([A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ.'’ -]{1,60}?(?:,\s*[A-ZÀ-ÖØ-Þ][\wÀ-ÖØ-öø-ÿ.'’ -]+)?)"
        r"(?=[.;]|$)",
        text,
    )

    return {
        "Date of Birth": dob,
        "Place of Birth": pob,
        "Date of Death": dod,
        "Place of Death": pod,
    }


def get_nlp(model: str = "en_core_web_sm"):
    try:
        return spacy.load(model)
    except OSError as exc:
        raise RuntimeError(
            f"spaCy model '{model}' is not installed. Run: "
            f"python -m spacy download {model}"
        ) from exc


def make_wikipedia_client():
    user_agent = os.getenv(
        "WIKIPEDIA_USER_AGENT",
        "GabrielaMistralEntityAnalysis/1.0 (research project; contact: update-this-before-large-scale-use)",
    )
    return wikipediaapi.Wikipedia(user_agent=user_agent, language="en")


def extract_person_attributes(wiki: wikipediaapi.Wikipedia, title: str) -> dict[str, Any] | None:
    page = wiki.page(title)
    try:
        if not page.exists():
            return None
        text = clean_text(page.text)
        if not text:
            return None
        return {
            "Title": page.title,
            "URL": page.fullurl,
            **extract_biographical_attributes(text),
        }
    except Exception as exc:  # Continue if one linked page is unavailable.
        print(f"Warning: could not process '{title}': {exc}", file=sys.stderr)
        return None


def run_analysis(title: str = DEFAULT_TITLE, output_dir: Path = DEFAULT_OUTPUT) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    wiki = make_wikipedia_client()
    page = wiki.page(title)
    if not page.exists():
        raise ValueError(f"Wikipedia page '{title}' does not exist.")

    page_text = page.text
    text = clean_text(page_text)
    if not text:
        raise ValueError(f"Wikipedia page '{title}' has no extractable text.")

    nlp = get_nlp()
    doc = nlp(text)

    # Article-level metadata and approximate biographical fields.
    article_attributes = {
        "Title": page.title,
        "Summary": page.summary,
        "URL": page.fullurl,
        "Word Count": len(text.split()),
        **extract_biographical_attributes(text),
    }
    attributes_path = output_dir / "article_attributes.csv"
    pd.DataFrame([article_attributes]).to_csv(attributes_path, index=False)

    entities = sorted({(ent.text.strip(), ent.label_) for ent in doc.ents if ent.text.strip()})
    entities_df = pd.DataFrame(entities, columns=["Entity", "Entity Type"])
    entities_path = output_dir / "named_entities.csv"
    entities_df.to_csv(entities_path, index=False)

    people = sorted({ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON" and ent.text.strip()})
    mentions_df = pd.DataFrame(
        [{"Source": page.title, "Target": name, "Relation Type": "text_mention", "Source URL": page.fullurl}
         for name in people]
    )
    mentions_path = output_dir / "people_mentions.csv"
    mentions_df.to_csv(mentions_path, index=False)

    all_link_titles = sorted(page.links.keys())
    outgoing_links_df = pd.DataFrame(
        [{"Source": page.title, "Target": link_title, "Target URL": page.links[link_title].fullurl}
         for link_title in all_link_titles]
    )
    outgoing_links_path = output_dir / "outgoing_links.csv"
    outgoing_links_df.to_csv(outgoing_links_path, index=False)

    candidate_titles = [t for t in all_link_titles if is_probably_person(t)]
    link_edges = [
        {"Source": page.title, "Target": t, "Relation Type": "outgoing_link", "Source URL": page.fullurl,
         "Target URL": page.links[t].fullurl}
        for t in candidate_titles
    ]
    mention_edges = [
        {"Source": page.title, "Target": name, "Relation Type": "text_mention", "Source URL": page.fullurl,
         "Target URL": ""}
        for name in people
    ]
    edges_df = pd.DataFrame(link_edges + mention_edges)
    if not edges_df.empty:
        edges_df = edges_df.drop_duplicates(subset=["Source", "Target", "Relation Type"]).reset_index(drop=True)
    edges_path = output_dir / "people_link_edges.csv"
    edges_df.to_csv(edges_path, index=False)

    linked_people: list[dict[str, Any]] = []
    # Avoid overly aggressive requests: limit candidate pages by default.
    max_pages = int(os.getenv("MAX_LINKED_PAGES", "100"))
    for person_title in tqdm(candidate_titles[:max_pages], desc="Fetching candidate linked pages"):
        result = extract_person_attributes(wiki, person_title)
        if result:
            linked_people.append(result)
    linked_path = output_dir / "linked_people_attributes.csv"
    pd.DataFrame(linked_people, columns=[
        "Title", "URL", "Date of Birth", "Place of Birth", "Date of Death", "Place of Death"
    ]).to_csv(linked_path, index=False)

    outputs = {
        "article_attributes": attributes_path,
        "named_entities": entities_path,
        "people_mentions": mentions_path,
        "outgoing_links": outgoing_links_path,
        "people_link_edges": edges_path,
        "linked_people_attributes": linked_path,
    }
    print(f"\nArticle: {page.title} ({page.fullurl})")
    print(f"Detected {len(entities_df)} unique named entities, {len(people)} person mentions, "
          f"{len(all_link_titles)} outgoing links, and {len(linked_people)} candidate linked pages.")
    print("CSV files written:")
    for path in outputs.values():
        print(f"  - {path}")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default=DEFAULT_TITLE, help="English Wikipedia article title")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Directory for CSV outputs")
    args = parser.parse_args()
    run_analysis(title=args.title, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
