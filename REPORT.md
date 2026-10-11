# Gabriela Mistral: Wikipedia Entity and Link Analysis

**Project report**  
**Author:** Danish Touseeq

## Abstract
This project explores a lightweight NLP pipeline for analyzing the English Wikipedia article about Gabriela Mistral. It retrieves article text and links, applies spaCy named entity recognition (NER), identifies candidate person names, and exports structured CSV files for subsequent inspection or graph analysis.

## 1. Objectives
The project aims to (1) retrieve a Wikipedia biography programmatically, (2) extract named entities, (3) collect outgoing links, (4) represent mentions and links as an edge list, and (5) collect basic attributes from candidate linked pages.

## 2. Tools
- Python for the pipeline and data handling.
- Wikipedia-API for retrieving article text, metadata, and outgoing links.
- spaCy `en_core_web_sm` for named entity recognition.
- pandas for structured CSV export.
- pytest for testing utility functions.

## 3. Method
The script retrieves the selected article, normalizes whitespace, and processes the text with spaCy. Unique entity spans are saved with their entity labels. Person-labelled spans are exported as text mentions. Outgoing links are saved separately; a simple name-pattern heuristic identifies candidate person pages. The script then retrieves a bounded number of candidate pages and extracts approximate birth/death fields using regular expressions.

## 4. Output artifacts
The pipeline writes six CSV files: article attributes, named entities, person mentions, outgoing links, person-link edges, and candidate linked-page attributes. Keeping these files separate makes it easier to inspect data quality and use the results in downstream graph analysis.

## 5. Results and interpretation
No live extraction results are claimed in this report because the project has not been run against the live Wikipedia API in this packaging step. Counts and CSV contents depend on the article revision and API response at execution time. After running the pipeline, report the actual counts of entities, mentions, links, and successfully retrieved candidate pages.

## 6. Limitations
spaCy NER identifies likely entity spans but does not resolve identity or prove a relationship. A two-or-more-token name heuristic is not a reliable person classifier. Regex extraction can fail when article wording differs from expected patterns or when a sentence mentions multiple locations. The extracted attributes therefore require validation before being used as research evidence.

## 7. Ethics, provenance, and reproducibility
Wikipedia content changes over time. For reproducibility, record the run date, article URL, and ideally the revision identifier if extending the project. Respect Wikimedia API usage guidance and use an informative user-agent with a valid contact method for large-scale access. Review the license and attribution requirements for any redistributed article text.

## 8. Conclusion
The project provides a reproducible starting point for extracting entities and link-based candidate relationships from a Wikipedia biography. The resulting CSV files can support manual validation and further graph analysis, provided that heuristic outputs are treated as candidates rather than verified facts.

## Running the project
Install `requirements.txt`, download the spaCy model using `python -m spacy download en_core_web_sm`, then run `python -m src.analyze_wikipedia`. See `README.md` for complete setup instructions.
