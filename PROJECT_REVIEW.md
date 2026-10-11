# Project Review and Changes

## What was improved
- Replaced repeated notebook code with one reusable Python pipeline.
- Added a proper README, requirements file, `.gitignore`, MIT license, project report, and unit tests.
- Removed the placeholder personal email from the Wikipedia API user-agent.
- Added a configurable `WIKIPEDIA_USER_AGENT` environment variable.
- Added command-line arguments for article title and output directory.
- Added validation for missing pages and missing spaCy model.
- Added per-page error handling and a default cap on linked-page requests (`MAX_LINKED_PAGES=100`).
- Exported article attributes, named entities, person mentions, all outgoing links, candidate link edges, and linked-page attributes as separate CSV files.
- Cleared notebook outputs so the notebook is lightweight and reruns cleanly.

## Known limitations
- Regex-based birth/death attributes are approximate and should be checked manually.
- The title heuristic for people can produce false positives and false negatives.
- Wikipedia API data changes over time.
- The live extraction has not been run here because it requires network access and may take time. Unit tests cover helper functions, not the live Wikipedia API.
- Update the user-agent to include a real contact method before running a large-scale crawl, and follow Wikimedia's API guidance.

## Before publishing
1. Install requirements and the spaCy model.
2. Run `pytest`.
3. Run `python -m src.analyze_wikipedia`.
4. Inspect CSV outputs and add verified example outputs only if appropriate.
5. If this builds on research data, document data provenance and review the relevant Wikipedia licensing terms.
