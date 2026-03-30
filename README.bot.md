# OGame Autonomous Bot

Un bot completamente autonomo per OGame che utilizza AI (Gemini) per prendere decisioni strategiche.

## 🤖 Caratteristiche

- **Completamente Autonomo**: Gioca da solo senza intervento umano
- **AI-Powered**: Usa Gemini per decisioni strategiche intelligenti 
- **Dockerizzato**: Deploy facile con Docker Compose
- **Anti-Detection**: Comportamento randomizzato e umano-simile
- **Monitoraggio**: Dashboard web per controllare lo stato
- **Configurable**: Strategie e comportamenti personalizzabili
- **Safe**: Auto-fleetsave e gestione risorse sicura

## 🚀 Quick Start

```bash
# 1. Clona e configura
git clone <repo>
cd OGameAGI
cp .env.bot .env

# 2. Modifica .env con le tue credenziali
nano .env

# 3. Lancia il bot
./launch.sh
```

## ⚙️ Configurazione

### Credenziali (Obbligatorie)
```env
OGAME_USERNAME=your_email@example.com
OGAME_PASSWORD=your_password
OGAME_UNIVERSE_URL=https://s161-en.ogame.gameforge.com/game/...
GEMINI_API_KEY=your_gemini_key
```

### Strategia Bot
```env
STRATEGIC_MODE=balanced          # conservative, balanced, aggressive
DECISION_INTERVAL=300           # secondi tra cicli decisione
RISK_TOLERANCE=low              # low, medium, high  
AUTO_FLEETSAVE=true            # fleetsave automatico
```

### Comportamento Anti-Detection
```env
ACTION_DELAY_MIN=3000          # delay minimo tra azioni (ms)
ACTION_DELAY_MAX=8000          # delay massimo tra azioni (ms)
RANDOMIZE_BEHAVIOR=true        # randomizza comportamento
HUMAN_SIMULATION=true          # simula comportamento umano
```

## 🏗️ Architettura

```
src/
├── ogame_bot.py              # Bot principale
├── agents/
│   └── gemini_brain.py       # AI Brain (Gemini)
├── automation/
│   ├── ogame_login.py        # Gestione login
│   ├── ogame_resources.py    # Parsing risorse
│   └── ogame_selectors.py    # Selettori CSS/XPath
└── monitoring/
    └── health_server.py      # Server monitoraggio
```

## 🎯 Strategia AI

Il bot usa Gemini per:
1. **Analizzare** lo stato del gioco corrente
2. **Decidere** azioni strategiche basate su knowledge base OGame
3. **Prioritizzare** azioni per obiettivi a lungo termine
4. **Adattare** strategia in base ai risultati

### Tipi di Azioni
- **Build**: Costruire/upgrade edifici
- **Research**: Ricercare tecnologie  
- **Fleet Dispatch**: Spedire flotte (raid, deploy, attack)
- **Wait**: Aspettare condizioni migliori

### Knowledge Base
Il bot include conoscenza strategica su:
- Priorità edifici per fase di gioco
- Sequenze ricerca ottimali
- Gestione risorse e ratio
- Strategie combattimento
- Tecniche fleetsaving

## 🐳 Docker Deploy

### Con Docker Compose (Raccomandato)
```bash
docker-compose -f docker-compose.bot.yml up -d
```

### Container standalone
```bash
docker build -f Dockerfile.bot -t ogame-bot .
docker run --env-file .env ogame-bot
```

## 📊 Monitoraggio

### Web Interface
Apri `http://localhost:8080` per:
- Stato bot in tempo reale
- Metriche performance 
- Logs recenti
- Stato risorse

### Endpoints API
- `GET /health` - Health check
- `GET /status` - Stato dettagliato
- `GET /metrics` - Metriche performance

### Logs
```bash
# Docker Compose
docker-compose -f docker-compose.bot.yml logs -f

# File logs
tail -f logs/ogame_bot.log
```

## 🔒 Sicurezza

### Anti-Detection Features
- **Timing Random**: Delay casuali tra azioni
- **Pattern Umani**: Simula comportamento umano
- **Session Management**: Breaks regolari 
- **Error Handling**: Gestisce disconnessioni gracefully

### Safe Defaults
- Auto-fleetsave attivo per default
- Risk tolerance basso
- Limite azioni per ciclo
- No combattimento per default

## ⚡ Performance

### Resource Usage
- **RAM**: ~1-2 GB
- **CPU**: ~0.5-1 core
- **Disk**: Minimal (logs + state)
- **Network**: Low (solo OGame requests)

### Timing
- **Ciclo decisione**: 5 minuti (configurabile)
- **Azioni per ciclo**: Max 3 (configurabile)  
- **Delay azioni**: 3-8 secondi random

## 🛠️ Sviluppo

### Test Locali
```bash
# Setup ambiente
python -m venv venv
source venv/bin/activate
pip install -r requirements.bot.txt

# Test singoli componenti
python -m pytest tests/

# Run locale (test mode)
TEST_MODE=true python src/ogame_bot.py
```

### Estendere il Bot
1. **Nuove Azioni**: Aggiungi in `ogame_bot.py`
2. **Migliorare AI**: Modifica prompt in `gemini_brain.py`
3. **Selettori**: Aggiorna `ogame_selectors.py` per nuove versioni OGame
4. **Monitoraggio**: Estendi `health_server.py`

## 📝 Logs Esempio

```
2026-03-30 10:30:15 - OGameBot - INFO - 🔄 Starting cycle 42
2026-03-30 10:30:18 - OGameBot - INFO - 📊 Resources: Metal=15.2K, Crystal=8.1K, Deuterium=3.4K  
2026-03-30 10:30:22 - GeminiBrain - INFO - AI Brain generated 2 decisions
2026-03-30 10:30:25 - OGameBot - INFO - ⚡ Executing action 1/2: build metal_mine
2026-03-30 10:30:31 - OGameBot - INFO - ✅ Started building metal_mine level 12
2026-03-30 10:30:36 - OGameBot - INFO - ⚡ Executing action 2/2: research energy_technology  
2026-03-30 10:30:42 - OGameBot - INFO - ✅ Started research energy_technology level 4
2026-03-30 10:30:45 - OGameBot - INFO - ✅ Cycle 42 completed
2026-03-30 10:30:45 - OGameBot - INFO - ⏱️ Waiting 300s for next cycle...
```

## ⚠️ Disclaimer

Questo bot è per scopi educativi. L'uso di bot potrebbe violare i ToS di OGame. Usa a tuo rischio.