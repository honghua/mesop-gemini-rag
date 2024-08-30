import mesop as me

from model import Model
from ui import UI
from dataclasses import dataclass


@dataclass
class Conversation:
    input: str
    output: str=""


@me.stateclass
class State:
    input: str
    output: str
    history: list[Conversation]
    in_progress: bool

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
            chat_input()
            output()
    UI.footer()

def chat_input():
    state = me.state(State)
    with me.box(
        style=UI.chat_style()
    ):
        with me.box(
            style=me.Style(
                flex_grow=1,
            )
        ):
            me.native_textarea(
                value=state.input,
                autosize=True,
                min_rows=4,
                placeholder="Enter your prompt",
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    background="white",
                    outline="none",
                    width="100%",
                    overflow_y="auto",
                    border=me.Border.all(
                        me.BorderSide(style="none"),
                    ),
                ),
                on_blur=textarea_on_blur,
            )
        with me.content_button(type="icon", on_click=click_send):
            me.icon("send")

def textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.input = e.value

def click_send(e: me.ClickEvent):
    state = me.state(State)
    if not state.input:
        return
    state.in_progress = True
    input_text = state.input
    state.input = ""
    state.output = ""  # Clear previous output
    yield

    for chunk in Model.call_api(input_text):
        state.output += chunk
        yield
    state.history.append(Conversation(input_text, state.output))
    state.in_progress = False
    yield

def output():
    state = me.state(State)
    if state.output or state.in_progress:
        with me.box(
            style=me.Style(
                background="#F0F4F9",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin(top=36),
            )
        ):
            if state.output:
                for converation in state.history:
                    me.markdown(converation.input)
                    me.markdown(converation.output)
            if state.in_progress:
                with me.box(style=me.Style(margin=me.Margin(top=16))):
                    me.progress_spinner()
