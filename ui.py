
import mesop as me
from uploader import Uploader, FileState




class UI:
    @staticmethod
    def header_text():
        with me.box(
            style=me.Style(
                padding=me.Padding(
                    top=64,
                    bottom=36,
                ),
            )
        ):
            me.text(
                "Mesop Chatbot",
                style=me.Style(
                    font_size=36,
                    font_weight=700,
                    background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                    color="transparent",
                ),
            )

    @staticmethod
    def footer():
        with me.box(
            style=me.Style(
                position="sticky",
                bottom=0,
                padding=me.Padding.symmetric(vertical=16, horizontal=16),
                width="100%",
                background="#F0F4F9",
                font_size=14,
            )
        ):
            me.html(
                "Made with <a href='https://google.github.io/mesop/'>Mesop</a>",
            )
        
    @staticmethod
    def upload():
        with me.box(style=me.Style(padding=me.Padding.all(15))):
            me.uploader(
                label="Upload File",
                accepted_file_types=["image/jpeg", "image/png", ".txt", ".pdf"],
                on_upload=Uploader._handle_upload,
                type="flat",
                color="primary",
                style=me.Style(font_weight="bold"),
            )

            state = me.state(FileState)
            if state.file.size:
                with me.box(style=me.Style(margin=me.Margin.all(10))):
                    me.text(f"File name: {state.file.name}")
                    me.text(f"File size: {state.file.size}")
                    me.text(f"File type: {state.file.mime_type}")