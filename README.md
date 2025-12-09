# uxscores

## Purpose

This application is an educational project created and developped by [Paul AMAT, UX designer with data skills](https://paulamatdesign.github.io/), designed to help students, researchers, and practitioners compute scores from multiple UX questionnaires. It is built with **Python** using **Streamlit**.

## Limitations

This app is provided “as is,” without any warranty of any kind. While care has been taken to implement scoring formulas as accurately as possible:

- No guarantee is given regarding the correctness, completeness, or reliability of the results.
- This tool must not be used as the sole basis for professional, academic, legal, or commercial decisions.
- The author cannot be held liable for any consequences resulting from the use of this application.
- If you require certified results, validation, or statistical guarantees, please rely on professional software or manual verification.

## Methodology

The implemented scoring algorithms are based on the publicly available definitions of the respective questionnaires (e.g., SUS, UMUX-Lite). However, implementation errors, interpretation differences, or future updates of scoring standards may lead to discrepancies.

## Data Privacy

- This app does not store questionnaire responses permanently.
- All computations are performed locally and temporarily for the duration of the session.
- No data is sold, shared, or analyzed beyond the displayed results.
- If you later add storage or analytics, this section should be updated accordingly.

## Licence Notice & Attribution

Both the app and its source code are distributed under the **MIT Licence**, allowing anyone to reuse, modify, and adapt them freely.

Please note that while **the app and its code** are MIT-licensed, **the UX questionnaires themselves are not mine**. Each questionnaire (e.g., SUS, UMUX-Lite, UEQ-S) may have its own licence, terms of use, or citation requirements.

Users must check the **original authors’ licences** before employing any questionnaire in a study, publication, or product.

All questionnaires remain the intellectual property of their respective authors. This application only provides automated scoring and does not claim ownership of any scale.

## Versioning

This application may be updated at any time. Results obtained from different versions of the tool may differ slightly due to bug fixes or methodological improvements.

## Feedback & Contact

If you find a bug, calculation issue, or would like to suggest a new questionnaire, feel free to contact:

[paul.amat@live.fr](paul.amat@live.fr)

## Permissions From Original Authors

This section lists the explicit permissions obtained directly from the authors of specific questionnaires.  

- UEQ-S: Permission granted by Martin Schrepp by email (December 2, 2025).
- UMUX-Lite: Permission granted by James Lewis by email (December 3, 2025).
- SUS: Author is retired.

---

## GitHub Notice

### Mac Starter Commands

- python3 -m venv .venv
- source .venv/bin/activate
- which pip
- pip install -r requirements.txt
- streamlit run Home.py
- pip freeze > requirements.txt

### Windows Starter Commands

- python3 -m venv .venv
- .\.venv\Scripts\activate.bat
- where pip
- pip install -r requirements.txt
- streamlit run Home.py
- pip freeze > requirements.txt
