from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
console = Console()
load_dotenv(".env")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Session history store (pro Session-ID eine eigene History)
store: dict[str, BaseChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Gibt die History für eine Session zurück (und erstellt sie bei Bedarf)."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ------------------------------------------------------------
# Schöne Darstellung der Ausgabe
# -----------------------------------------------------------
def render_story(markdown_text: str) -> None:
    """
    Erwartet das feste Markdown-Format:
    ## Szene
    ...
    ## Optionen
    1) ...
    2) ...
    3) ...
    """
    text = markdown_text.strip()

    # Sehr robustes Splitten an der Überschrift "## Optionen"
    if "## Optionen" in text:
        scene_part, options_part = text.split("## Optionen", 1)
    else:
        scene_part, options_part = text, ""

    # "## Szene" entfernen (falls vorhanden)
    scene_part = scene_part.replace("## Szene", "", 1).strip()
    options_part = options_part.strip()

    # Szene-Panel
    console.print(
        Panel(
            Markdown(scene_part) if scene_part else Text("(keine Szene gefunden)"),
            title="Szene",
            expand=False,
        )
    )

    # Optionen-Panel
    if options_part:
        console.print(
            Panel(
                Markdown(options_part),
                title="Optionen",
                expand=False,
            )
        )
    else:
        console.print(
            Panel(
                Text("(keine Optionen gefunden)"),
                title="Optionen",
                expand=False,
            )
        )


# ------------------------------------------------------------
# Prompt: WICHTIG ist der MessagesPlaceholder für chat_history
# ------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Du bist ein kreativer Geschichtenerzähler.\n"
     "Ort der Geschichte: {place}\n\n"
     "WICHTIG: Antworte IMMER exakt im folgenden Markdown-Format (keine zusätzlichen Abschnitte):\n"
     "## Szene\n"
     "<2–5 kurze Sätze, Präsens, sehr prägnant>\n\n"
     "## Optionen\n"
     "1) <Option 1>\n"
     "2) <Option 2>\n"
     "3) <Option 3>\n\n"
     "Regeln:\n"
     "- Genau zwei Überschriften: '## Szene' und '## Optionen'.\n"
     "- Unter '## Optionen' genau 3 Zeilen, nummeriert 1) bis 3).\n"
     "- Keine weiteren Listen, keine Bulletpoints, kein Fließtext nach den Optionen.\n"
     "- Keine Vorrede, keine Erklärungen.\n"
     "- Der Prodagonist wird immer in der Du-Form erwähnt.\n"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


# LCEL-Kette: Prompt -> LLM
chain = prompt | llm

# RunnableWithMessageHistory: verbindet chain + History
game = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="input",         # wo steht der neue User-Text?
    history_messages_key="chat_history" # wie heißt der Placeholder im Prompt?
)

# ------------------------------------------------------------
# Spielparameter / Session
# ------------------------------------------------------------
session_id = "03"
config = {"configurable": {"session_id": session_id}}
place = "Ein dunkler Wald"

# ------------------------------------------------------------
# Startszene
# ------------------------------------------------------------
start = game.invoke(
    {"place": place, "input": "Eröffne die Abenteuergeschichte mit einer Startszene."},
    config=config
)
#console.print(Markdown(start.content))
render_story(start.content)

# ------------------------------------------------------------
# Loop: Spielerwahlen
# ------------------------------------------------------------
while True:
    player_choice = input("\nGib deine Wahl ein (1/2/3 oder Text, 'quit' zum Beenden): ").strip()
    if player_choice.lower() == "quit":
        break

    response = game.invoke(
        {"place": place, "input": f"Meine Wahl ist: {player_choice}. Setze die Geschichte fort."},
        config=config
    )
    # console.print(Markdown(response.content))
    render_story(response.content)

# Optional: Debug (zeigt dir, was wirklich in der History liegt)
history = get_session_history(session_id)
print("\n--- DEBUG: gespeicherte Messages ---")
for m in history.messages:
    print(type(m).__name__, ":", m.content[:80].replace("\n", " "), "...")
