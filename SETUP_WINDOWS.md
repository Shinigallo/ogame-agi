# OGameAGI - Setup Completo per Windows

## Prerequisiti

- **Python 3.10+** installato
- **Chrome** installato (per Playwright)
- **Git** (per clonare il repo)

---

## Setup Rapido (PowerShell)

```powershell
# 1. Apri PowerShell nella cartella OGameAGI
cd OGameAGI

# 2. Crea virtual environment
python -m venv venv

# 3. Attiva venv
.\venv\Scripts\activate

# 4. Installa dipendenze
pip install -r requirements.txt

# 5. Installa Playwright + Browser
playwright install
playwright install chromium

# 6. Copia env file
copy .env.windows .env

# 7. MODIFICA .env con le tue credenziali!
#    - OGAAME_USERNAME = la tua email
#    - OGAME_PASSWORD = la tua password
#    - GEMINI_API_KEY = la tua chiave (o usa quella di default)

# 8. Esegui il test
python tests/test_playwright_fase1.py
```

---

## Cosa Fa il Test

1. **Lancia Chrome in headless** (o visibile se `HEADLESS=false`)
2. **Naviga** a `https://lobby.ogame.gameforge.com/`
3. **Accetta cookie** se presente
4. **Login** con credenziali da `.env`
5. **Seleziona universo** Scorpius
6. **Estrae risorse** dal DOM
7. **Salva screenshot** in `logs/fase1_test.png`
8. **Salva sessione** in `data/session.json` (prossimi login più veloci)

---

## Struttura File

```
OGameAGI/
├── src/
│   └── automation/
│       ├── ogame_selectors.py     # Selettori CSS/XPath per OGame
│       ├── ogame_login.py         # Gestione login e sessione
│       ├── ogame_resources.py     # Parsing risorse dal DOM
│       └── playwright_interface.py
├── tests/
│   └── test_playwright_fase1.py  # Test completo login+resources
├── logs/                         # Screenshot e log
├── data/                         # Sessioni salvate
├── .env.windows                  # Template configurazione
└── requirements.txt
```

---

## Risoluzione Problemi

### Errore: "Chromium not found"
```powershell
playwright install chromium
```

### Errore: "Missing credentials"
Apri `.env` e verifica di aver compilato:
- `OGAME_USERNAME`
- `OGAME_PASSWORD`

### Vuoi vedere il browser (non headless)
Modifica `.env`:
```
HEADLESS=false
```

### Vuoi solo testare la connessione (no login)
```powershell
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); print('✅ Browser funziona!'); b.close(); p.stop()"
```

---

## Prossimi Step

Dopo Phase 1:
- **Phase 2:** Building automation (coda costruzioni)
- **Phase 3:** Fleet dispatch (inviare flotte)
- **Phase 4:** Research automation
- **Phase 5:** Integrazione AI brain Gemini