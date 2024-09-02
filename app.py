import mesop as me
import mesop.labs as mel

from datastore import DataStoreGenerator
from ui import UI

@me.page(path="/chatbot")
def page():
    with me.box(
        style=me.Style(
            background="#fff",
            min_height="calc(100% - 48px)",
            padding=me.Padding(bottom=16),
        )
    ):
        with me.box(
            style=me.Style(
                width="min(720px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto"),
                padding=me.Padding.symmetric(
                    horizontal=16,
                ),
            )
        ):
            UI.header_text()
            UI.upload()
            mel.chat(transform, title="Mesop Demo Chat", bot_user="Mesop Bot")

    UI.footer()

def transform(input: str, history: list[mel.ChatMessage]):
    yield DataStoreGenerator.retriever.process_query(input)
