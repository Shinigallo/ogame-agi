# OGame AGI - Autonomous Gaming Intelligence

Un sistema di bot AI per OGame con due modalità: **Full Autonomous** e **Smart Token-Efficient**.

## 🎯 Modalità Disponibili

### 1. Full Autonomous Bot
Bot completo con decisioni AI continue (per testing e sviluppo).

### 2. Smart Bot (Raccomandato)
Bot intelligente event-driven che minimizza l'uso di token AI.

## 🚀 Quick Start

```bash
git clone https://github.com/your-username/OGameAGI.git
cd OGameAGI

# Setup credenziali
cp .env.example .env
nano .env

# Lancia Smart Bot (raccomandato)
./launch_smart.sh
```

## 📁 Struttura Progetto

```
OGameAGI/
├── src/
│   ├── smart_ogame_bot.py        # Smart bot (token-efficient)
│   ├── ogame_bot.py              # Full autonomous bot
│   ├── automation/               # Playwright automation
│   │   ├── ogame_login.py        # Login management
│   │   ├── ogame_resources.py    # Resource parsing
│   │   └── ogame_selectors.py    # Game selectors
│   ├── agents/
│   │   └── gemini_brain.py       # AI decision engine
│   └── monitoring/
│       └── health_server.py      # Health monitoring
├── tests/                        # Playwright tests
├── knowledge/                    # OGame knowledge base
├── docker-compose.smart.yml      # Smart bot deployment
├── docker-compose.bot.yml        # Full bot deployment
└── launch_smart.sh               # Smart launcher
```

## 🧠 Smart Bot Features

### Event-Driven Architecture
- **Quick checks** ogni 60s senza AI
- **AI decisions** solo quando necessario
- **Cron scheduling** per timing precisi
- **90% riduzione** uso token

### Trigger Intelligenti
```bash
# Eventi che attivano AI
- Building/research completed
- Resources exceed thresholds  
- Fleet returns detected
- Emergency situations
```

### Rule-Based Fallbacks
```python
# Azioni semplici senza AI
if metal > 50000:
    quick_build('metal_mine')
elif crystal > 25000:
    quick_build('crystal_mine') 
```

## ⚙️ Configurazione

### Credenziali (Obbligatorie)
```env
OGAME_USERNAME=your_email
OGAME_PASSWORD=your_password
OGAME_UNIVERSE_URL=https://...
GEMINI_API_KEY=your_key
```

### Smart Bot Settings
```env
QUICK_CHECK_INTERVAL=60          # Quick checks (no AI)
AI_DECISION_INTERVAL=1800        # AI decisions (30min)
METAL_THRESHOLD=50000            # Resource alerts
CRYSTAL_THRESHOLD=25000
DEUTERIUM_THRESHOLD=12500
```

## 🐳 Deployment

### Docker Compose (Raccomandato)
```bash
# Smart Bot
docker-compose -f docker-compose.smart.yml up -d

# Full Bot  
docker-compose -f docker-compose.bot.yml up -d
```

### Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.smart.txt
playwright install chromium

python src/smart_ogame_bot.py
```

## 📊 Monitoring

### Web Dashboard
```bash
http://localhost:8080/health    # Health check
http://localhost:8080/status    # Detailed status  
http://localhost:8080/metrics   # Performance metrics
```

### Logs
```bash
# Docker logs
docker-compose -f docker-compose.smart.yml logs -f

# File logs
tail -f logs/smart_bot.log
```

## 🔒 Sicurezza

### Anti-Detection
- Timing randomizzato
- Session breaks regolari
- Comportamento human-like
- Auto-fleetsave integrato

### Safe Defaults
- Risk tolerance: LOW
- Combat: DISABLED
- Max session time: 1 hour
- Auto-logout attivo

## 🎮 Strategia AI

### Knowledge Base
Il bot include expertise su:
- Priorità edifici per fase gioco
- Sequenze ricerca ottimali  
- Gestione risorse (ratio 3:2:1)
- Tecniche fleetsaving
- Strategie combattimento

### Decision Engine
```python
# Gemini analizza stato e decide
context = {
    "resources": {"metal": 45000, "crystal": 22000},
    "strategy": "balanced",
    "risk_tolerance": "low"
}

decisions = await brain.analyze_and_decide(context)
# Returns: [{"type": "build", "target": "metal_mine", ...}]
```

## 🧪 Testing

### Phase 1 Tests
```bash
# Test login + resource parsing
python tests/test_playwright_fase1.py

# Windows setup
./setup_windows.ps1
```

### Test Mode
```bash
TEST_MODE=true python src/smart_ogame_bot.py
```

## 📈 Performance

### Resource Usage
- **Memory**: ~512MB-1GB
- **CPU**: ~0.2-0.5 cores  
- **Network**: Minimal
- **Tokens**: 90% less than full bot

### Efficiency Comparison
| Metric | Full Bot | Smart Bot |
|--------|----------|-----------|
| AI Calls | Every 5min | Every 30min |
| Token Usage | High | Minimal |
| Resource Usage | 2GB RAM | 512MB RAM |
| Uptime | 100% active | Event-driven |

## 🔧 Estensioni

### Nuove Features
1. **Custom Strategies**: Modifica `gemini_brain.py`
2. **New Selectors**: Aggiorna per nuove versioni OGame
3. **Additional Events**: Estendi event detection
4. **Enhanced AI**: Migliora decision prompts

### Plugin System
```python
# Aggiungi nuovi event handlers
async def handle_custom_event(self, event: GameEvent):
    # Custom logic here
    pass
```

## ⚠️ Disclaimer

Questo progetto è per scopi **educativi e di ricerca**. L'uso di bot automatizzati potrebbe violare i Termini di Servizio di OGame. Utilizzare a proprio rischio e responsabilità.

## 🤝 Contributi

1. Fork il repository
2. Crea feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)  
5. Apri Pull Request

## 📄 Licenza

Distributed under the MIT License. See `LICENSE` for more information.

---

**Built with ❤️ for the OGame community**