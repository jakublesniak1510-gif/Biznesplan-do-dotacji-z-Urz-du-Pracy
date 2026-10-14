"""pup_gen – silnik usługi „Biznesplan do dotacji z Urzędu Pracy”.

Przebieg: kwestionariusz (JSON) -> arkusz finansowy (LibreOffice) -> prompty z `szablony/`
-> model (Claude albo atrapa) -> kontrola jakości -> DOCX dla klienta + raport dla właściciela.
"""

import os
from pathlib import Path

__version__ = "0.1.0"

# Katalog repozytorium (szablony, model finansowy, baza PUP). Pakiet leży w <repo>/generator/pup_gen.
KATALOG_REPO = Path(os.environ.get("PUP_GEN_REPO", Path(__file__).resolve().parents[2]))
KATALOG_SZABLONOW = KATALOG_REPO / "szablony"
PLIK_MODELU = KATALOG_REPO / "model-finansowy" / "model-finansowy-pup.xlsx"
PLIK_BAZY_PUP = KATALOG_REPO / "baza-pup" / "regulaminy-pup-2026.csv"
KATALOG_PRZYKLADOW = Path(__file__).resolve().parents[1] / "przyklady"
KATALOG_WYNIKOW = Path(os.environ.get("PUP_GEN_WYNIKI", KATALOG_REPO / "wyniki"))
