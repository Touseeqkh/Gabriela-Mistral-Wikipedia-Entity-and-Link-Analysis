# Gabriela Mistral: Wikipedia Entity and Link Analysis

A Python NLP project that retrieves the English Wikipedia article for Gabriela Mistral, extracts named entities with spaCy, collects outgoing Wikipedia links that look like person names, and exports structured CSV files for further analysis.

## Features

- Retrieves the Gabriela Mistral article through the Wikipedia API.
- Extracts basic article metadata and heuristic biographical attributes.
- Uses spaCy Named Entity Recognition (NER) to collect people, organizations, places, and other entities.
- Builds an edge list for outgoing links and person-name mentions.
- Collects basic attributes for linked pages that pass a simple name heuristic.
- Exports results as CSV files in `data/`.

## Project structure

```text
gabriela-mistral-wikipedia-entity-analysis/
├── README.md
├── REPORT.md
├── report.pdf
├── requirements.txt
├── .gitignore
├── LICENSE
├── PROJECT_REVIEW.md
├── notebooks/
│   └── gabriela_mistral_wikipedia_analysis.ipynb
├── src/
│   ├── __init__.py
│   └── analyze_wikipedia.py
├── tests/
│   └── test_helpers.py
└── data/
    └── .gitkeep
```

## Requirements

- Python 3.10 or newer recommended
- Internet access for Wikipedia API requests and the initial spaCy model download

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run the analysis

From the project root:

```bash
python -m src.analyze_wikipedia
```

By default, outputs are written to `data/`. You can provide a different article title or output folder:

```bash
python -m src.analyze_wikipedia --title "Gabriela Mistral" --output-dir data
```

### 4. Run the notebook

Open `notebooks/gabriela_mistral_wikipedia_analysis.ipynb` in Jupyter or Google Colab. Run cells from top to bottom. If running locally, install the dependencies first.

## Output files

| File | Contents |
|---|---|
| `data/article_attributes.csv` | Article URL, summary, and heuristic biographical fields |
| `data/named_entities.csv` | Unique spaCy entities and entity labels |
| `data/people_mentions.csv` | Person entities mentioned in the article |
| `data/outgoing_links.csv` | All outgoing article links |
| `data/people_link_edges.csv` | Candidate person links and text-mention edges |
| `data/linked_people_attributes.csv` | Basic attributes extracted from candidate linked pages |

The script may not find every person or biographical attribute. These are heuristic extractions from article text, not authoritative structured facts.

## Methodology and limitations

- **NER is not a knowledge graph:** spaCy detects entity spans but does not establish the real-world relationship between entities.
- **Person-link filtering is heuristic:** the initial name pattern can miss single-word names, names with initials, non-English diacritics, and titles that are not people. It can also include non-person pages. Validate candidates before research use.
- **Biographical regexes are approximate:** article wording varies. `N/A` means the pattern did not match; it does not mean the information is unknown.
- **Wikipedia changes over time:** the exported results depend on the article revision available when you run the project.
- **Be respectful of the API:** the script uses a descriptive user-agent and handles per-page errors, but large-scale collection should follow Wikimedia API policies and rate limits.

## Data and attribution

Wikipedia text is available under the license shown on the relevant article page (generally CC BY-SA for article text). If you redistribute extracted text or substantial adaptations, check the applicable license and attribution requirements. This repository contains code, not a bundled copy of Wikipedia article text.

## Author

Danish Touseeq
