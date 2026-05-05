# College Match Finder

*Interactive college recommendation tool — weighted multi-criteria scoring over U.S. Department of Education data.*

**Status:** Under construction. Full documentation will be added when the app is complete.

## Data Sources

- **College Scorecard, Institution-Level Data** — U.S. Department of Education. [collegescorecard.ed.gov/data](https://collegescorecard.ed.gov/data/)
- **College Scorecard, Field of Study Data** — U.S. Department of Education.
- **Clery Act Campus Safety and Security Data** — U.S. Department of Education. [ope.ed.gov/campussafety](https://ope.ed.gov/campussafety/)

## Setup (local)

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Place raw files in data/raw/ (see DATA_DOWNLOAD.md), then:
python data_prep.py

streamlit run app.py
```

---
Built by Jonathan Nadeau · [nadeaujonny.github.io](https://nadeaujonny.github.io)
