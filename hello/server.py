"""
Minimal MCP server (Python, STDIO)

Tools:
- echo(text: str) -> str

Run locally with MCP Inspector (requires Node >= 18 and uv):
  uv pip install --upgrade mcp
  npx @modelcontextprotocol/inspector uv run server.py

This starts the server via STDIO under the Inspector. You can then invoke the
"echo" tool and observe JSON request/response and streaming events.
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Dict, List
from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("HelloMCP")

# ------------------------------
# Metaphors resource (English)
# ------------------------------
# We expose a resource namespace with a unique URI scheme to avoid collisions
# with the other server that uses "docs://". Here we use "metaphors://".

# Category translations (PL -> EN) as they appear under "## " headings
CAT_TRANSLATIONS: Dict[str, str] = {
    "BIOLOGIA & EWOLUCJA": "BIOLOGY & EVOLUTION",
    "FIZYKA & NAUKA": "PHYSICS & SCIENCE",
    "TECHNOLOGIA & INTERNET": "TECHNOLOGY & INTERNET",
    "SPOŁECZNOŚĆ & KOMUNIKACJA": "SOCIETY & COMMUNICATION",
    "NATURA & EKOSYSTEMY": "NATURE & ECOSYSTEMS",
    "TRANSPORT & INFRASTRUKTURA": "TRANSPORT & INFRASTRUCTURE",
    "HISTORIA & ARCHEOLOGIA": "HISTORY & ARCHAEOLOGY",
    "EKSPLORACJA KOSMICZNA": "SPACE EXPLORATION",
    "TEORIA SIECI": "NETWORK THEORY",
    "GAMING & ROZRYWKA": "GAMING & ENTERTAINMENT",
    "MEDYCYNA": "MEDICINE",
    "KRYTYCZNE SPOJRZENIA (z dyskusji developerskich)": "CRITICAL PERSPECTIVES (from developer discussions)",
}

# Exact sentence translations (PL -> EN) for the current file contents.
SENTENCE_TRANSLATIONS: Dict[str, str] = {
    'MCP jest jak RNA-posłaniec: przenosi instrukcje między jądrem wiedzy a organellami narzędzi, niezależnie od gatunku kodu.': "MCP is like messenger RNA: it carries instructions between the nucleus of knowledge and the organelles of tools, regardless of the species of code.",
    'MCP to rybosom dla AI: tłumaczy jeden uniwersalny kod genetyczny na nieskończoną różnorodność funkcjonalnych białek-narzędzi.': "MCP is a ribosome for AI: it translates a single universal genetic code into an endless diversity of functional tool-proteins.",
    'MCP to łożysko cybernetyczne – odżywia każdą "sztuczną" komórkę danymi matki-ekosystemu bez konfliktu immunologicznego.': "MCP is a cybernetic placenta—it nourishes every 'artificial' cell with the mother's-ecosystem data without an immune conflict.",
    'MCP jest jak kod HOX – zestaw genów, który organizuje różne moduły w jedno, działające "ciało" sztucznej inteligencji.': "MCP is like the HOX code—a set of genes that organizes different modules into a single functioning 'body' of artificial intelligence.",
    'MCP to horyzontalny transfer genów dla oprogramowania: zamiast pisać sterowniki, AI natychmiastowo nabywa zdolności od innego "gatunku" narzędzi.': "MCP is horizontal gene transfer for software: instead of writing drivers, AI instantly acquires capabilities from another 'species' of tools.",
    'MCP to mikoryza cyfrowa – sieć grzybni, przez którą modele i narzędzia wymieniają składniki odżywcze informacji.': "MCP is a digital mycorrhiza—a fungal network through which models and tools exchange the nutrients of information.",
    'MCP to skrzydło wczesnego archeopteryksa: pierwszy standard, który pozwolił modelom wznieść się ponad bagna silosów danych.': "MCP is the early Archaeopteryx’s wing: the first standard that let models rise above the swamps of data silos.",
    'MCP działa jak uniwersalna przeciwciało, rozpoznające i łączące modele AI z obcymi danymi, sprawiając że współpraca staje się odporna na błędy komunikacji.': "MCP acts like a universal antibody, recognizing and linking AI models with foreign data, making collaboration resilient to communication errors.",
    'MCP to układ nerwowy ośmiornicy: jedna głowa modelu, wiele autonomicznych kończyn API, ale jeden spójny impuls.': "MCP is the octopus’s nervous system: one model head, many autonomous API limbs, yet a single coherent impulse.",
    'MCP jak pszczoła-kurier: zbiera nektar z dowolnego źródła danych i dostarcza go do ula modelu, zapylając nowe wnioski.': "MCP is like a bee-courier: it collects nectar from any data source and delivers it to the model’s hive, pollinating new insights.",
    'MCP to warstwa Plancka komunikacji: najmniejsza, ale uniwersalna jednostka wymiany między wszechświatami kodu.': "MCP is the Planck layer of communication: the smallest yet universal unit of exchange between universes of code.",
    'MCP jak pryzmat – rozszczepia surowy strumień danych na kanały, które każdy model absorbuje bez strat energii.': "MCP is like a prism—it splits a raw data stream into channels that each model absorbs without energy loss.",
    'MCP to tunel kwantowy: skraca drogę między odseparowanymi domenami wiedzy, przeskakując bariery protokołów.': "MCP is a quantum tunnel: it shortens the path between isolated domains of knowledge, jumping across protocol barriers.",
    'MCP to stała kosmologiczna integracji – niewidoczna, a jednak steruje ekspansją całego ekosystemu narzędzi.': "MCP is the cosmological constant of integration—invisible, yet it steers the expansion of the entire tool ecosystem.",
    'MCP to kwantowe splątanie dla systemów: dwa odizolowane narzędzia, jeden natychmiastowo spójny stan, bez pośredniczącego sygnału.': "MCP is quantum entanglement for systems: two isolated tools, a single instantaneously coherent state, without an intermediate signal.",
    'MCP jak transformer elektromagnetyczny - przekształca różne "napięcia" danych i narzędzi w jedną, harmonijną, użyteczną wartość dla każdego modelu AI.': "MCP is like an electromagnetic transformer—it converts different 'voltages' of data and tools into a single, harmonious, useful value for any AI model.",
    'MCP funkcjonuje jak niewidzialne pole magnetyczne – przyciąga i synchronizuje każdy rozproszony element, porządkując chaos informacji.': "MCP functions like an invisible magnetic field—it attracts and synchronizes every scattered element, organizing the chaos of information.",
    'MCP to zawór serca Von Neumanna – jednocześnie pompuje i filtruje informacje, utrzymując rytm systemu.': "MCP is the Von Neumann heart valve—it simultaneously pumps and filters information, keeping the system’s rhythm.",
    'MCP jest mostem Einsteina-Rosen-API: zwija czas integracji, by model mógł od ręki sięgnąć po odległe zasoby.': "MCP is an Einstein–Rosen API bridge: it folds integration time so the model can instantly reach distant resources.",
    'MCP to USB-C dla mózgu maszyny – niezależnie od producenta, wtykasz i działa.': "MCP is USB-C for the machine’s brain—regardless of vendor, you plug it in and it just works.",
    'MCP jak HDMI między ludzką intuicją a silnikiem obliczeń – jeden kabel, pełne spektrum percepcji i akcji.': "MCP is like HDMI between human intuition and the compute engine—one cable, the full spectrum of perception and action.",
    'MCP to Docker dla połączeń: opakowuje różnorodne strumienie w standardowy kontener portu 443.': "MCP is Docker for connections: it packages diverse streams into a standard container on port 443.",
    'MCP to internet protocol dla AI - tłumaczy tysiące "dialektów" zewnętrznych narzędzi i danych na jedną płynną, uniwersalną komunikację.': "MCP is an Internet protocol for AI—it translates thousands of 'dialects' of external tools and data into one smooth, universal communication.",
    'MCP jest jak magistrala komputerowa - każdy komponent AI się podłącza i rozmawia płynnie, niezależnie od swojego pochodzenia.': "MCP is like a computer bus—every AI component connects and communicates fluidly, regardless of its origin.",
    'MCP przypomina blockchain bez kryptowaluty – nie zmienia wartości danych, tylko gwarantuje jednolity protokół ich przekazu.': "MCP resembles a blockchain without cryptocurrency—it doesn’t change the value of data, it simply guarantees a uniform protocol for its transfer.",
    'MCP to uniwersalny pilot – zamiast żonglować wieloma pilotami do różnych urządzeń, masz jeden do wszystkich źródeł danych.': "MCP is a universal remote—instead of juggling many remotes for different devices, you have one for all data sources.",
    'MCP to esperanto API – nie najpiękniejsze, lecz zrozumiałe dla każdego plemienia narzędzi.': "MCP is API Esperanto—not the most beautiful, but understandable to every tribe of tools.",
    'MCP jak protokół dyplomatyczny przy szczycie G20: różne potęgi technologiczne rozmawiają bez faux-pas.': "MCP is like a diplomatic protocol at a G20 summit: diverse technological powers converse without faux pas.",
    'MCP to wspólna waluta w miasteczku programistów – eliminuje przewalutowania adapterów i prowizje konwerterów.': "MCP is a common currency in a programmers’ town—it eliminates currency exchanges of adapters and converter fees.",
    'MCP to wynalazek pieniądza: kończy z nieskończoną złożonością barteru (niestandardowe API) na rzecz jednego, uniwersalnego nośnika wartości.': "MCP is the invention of money: it ends the endless complexity of barter (non-standard APIs) in favor of a single, universal medium of value.",
    'MCP jest lingua franca dla pokoju pełnego AI poliglotów – mostem między kulturami (źródłami danych), które nigdy nie mówiły tym samym językiem.': "MCP is a lingua franca for a room full of AI polyglots—a bridge between cultures (data sources) that never spoke the same language.",
    'MCP funkcjonuje jak uniwersalny dialekt, umożliwiający różnym narzędziom rozmowę na jednym poziomie, niczym zjednoczona sieć społeczna.': "MCP functions like a universal dialect, enabling different tools to converse on one level, like a unified social network.",
    'MCP to centralny węzeł ekosystemu, który jak symfonia natury zamienia dziką różnorodność narzędzi w harmonijną orkiestrę danych.': "MCP is the ecosystem’s central node which, like nature’s symphony, turns the wild diversity of tools into a harmonious orchestra of data.",
    'MCP to dział wodny - kanalizuje dopływy z rozproszonych strumieni danych w jeden potężny, spływny prąd dla eksploracji AI.': "MCP is a watershed—it channels inflows from scattered data streams into one powerful, navigable current for AI exploration.",
    'MCP to grzyb pozwalający drzewom (modelom AI i danym) komunikować się pod ziemią - odżywiać siebie nawzajem przez ukrytą, ustandaryzowaną sieć.': "MCP is the fungus that lets trees (AI models and data) communicate underground—nourishing each other through a hidden, standardized network.",
    'MCP to światowy dworzec centralny, gdzie agenci AI i dane przesiadają się na platformy, by połączyć się z każdym miejscem, w każdym czasie - bez biletu ani tłumaczenia.': "MCP is a global central station where AI agents and data change platforms to connect to any place, anytime—without a ticket or translation.",
    'MCP to rewolucja przemysłowa w świecie AI – maszyna, która przekształca surowy bałagan danych w uporządkowane linie produkcyjne wiedzy.': "MCP is the industrial revolution of AI—a machine that turns the raw mess of data into orderly production lines of knowledge.",
    'MCP jawi się niczym klucz archeologa, odsłaniający ukryte skarby standaryzacji w zacierającym się mroku nieuporządkowanych informacji.': "MCP appears like an archaeologist’s key, revealing hidden treasures of standardization in the fading darkness of disordered information.",
    'MCP działa jak międzygwiezdny kompas, otwierający drogę do eksploracji nieodkrytych kosmicznych przestrzeni narzędzi i danych.': "MCP works like an interstellar compass, opening the way to exploring uncharted cosmic spaces of tools and data.",
    'MCP nie buduje mostów; ujawnia, że w sieci małego świata każde narzędzie było zawsze o jeden protokół od siebie.': "MCP doesn’t build bridges; it reveals that in a small-world network every tool was always just one protocol away.",
    'MCP jak cheat code dla świata AI - nagle wszystkie poziomy (narzędzia) stają się dostępne bez grania w każdą grę osobno.': "MCP is like a cheat code for the AI world—suddenly all levels (tools) become accessible without playing each game separately.",
    'MCP jako antybiotyk szerokospektralny - leczy wszystkie infekcje niekompatybilności między systemami jednym uniwersalnym lekarstwem.': "MCP as a broad-spectrum antibiotic—it cures all infections of incompatibility between systems with a single universal medicine.",
    '"MCP to bardziej dongle USB-Claude niż prawdziwe USB-C AI" - gdzie \'C\' stanowczo znaczy Claude.': '"MCP is more a USB-Claude dongle than true AI USB‑C"—where the "C" decidedly stands for Claude.',
    'MCP obiecuje być USB-C dla AI, ale ironicznie kończy jak kolejny proprietary connector.': "MCP promises to be USB‑C for AI, but ironically ends up as yet another proprietary connector.",
}

def _slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def _load_metaphors_en() -> Dict[str, str]:
    """Parses the markdown file and returns a mapping of id -> English content."""
    repo_root = Path(__file__).resolve().parent.parent
    md_path = repo_root / "DOCS" / "mcp-metaphors-collection.md"

    if not md_path.exists():
        return {}

    current_cat_pl: str | None = None
    counters: Dict[str, int] = {}
    result: Dict[str, str] = {}

    with md_path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Capture category headings
            if line.startswith("## "):
                current_cat_pl = line[3:].strip()
                continue
            # Ignore the H1 and separators / sources footer
            if line.startswith("# ") or line.startswith("---") or line.startswith("*Źródła"):
                continue
            # Treat any other non-empty line as a metaphor sentence
            cat_en = CAT_TRANSLATIONS.get(current_cat_pl or "", (current_cat_pl or "UNSPECIFIED")).upper()
            counters.setdefault(cat_en, 0)
            counters[cat_en] += 1
            item_id = f"{_slugify(cat_en)}-{counters[cat_en]}"
            en_text = SENTENCE_TRANSLATIONS.get(line, line)
            result[item_id] = en_text

    return result

# Preload the map at startup
METAPHORS_EN: Dict[str, str] = _load_metaphors_en()

@mcp.resource(
    uri="metaphors://items",
    description="Returns a list of metaphor IDs (English).",
    mime_type="application/json",
)
def list_metaphors_ids() -> list[str]:
    return list(METAPHORS_EN.keys())

@mcp.resource(
    uri="metaphors://items/{item_id}",
    description="Returns the English content of a metaphor by ID.",
    mime_type="text/plain",
)
def get_metaphor_content(item_id: str) -> str:
    return METAPHORS_EN[item_id]

@mcp.tool(
    name="echo",
    description="Echo back the provided text.",
)
def echo(text: str = Field(description="The text to echo back")) -> str:
    return text

if __name__ == "__main__":
    mcp.run(transport="stdio")
