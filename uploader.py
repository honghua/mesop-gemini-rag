import base64

import mesop as me

@me.stateclass
class FileState:
    file: me.UploadedFile

class Uploader:
  @staticmethod
  def upload():
    state = me.state(FileState)
    with me.box(style=me.Style(padding=me.Padding.all(15))):
      me.uploader(
        label="Upload File",
        accepted_file_types=["image/jpeg", "image/png", ".txt", ".pdf"],
        on_upload=Uploader._handle_upload,
        type="flat",
        color="primary",
        style=me.Style(font_weight="bold"),
      )

      if state.file.size:
        with me.box(style=me.Style(margin=me.Margin.all(10))):
          me.text(f"File name: {state.file.name}")
          me.text(f"File size: {state.file.size}")
          me.text(f"File type: {state.file.mime_type}")

        with me.box(style=me.Style(margin=me.Margin.all(10))):
          me.image(src=Uploader._convert_contents_data_url(state.file))


  @staticmethod
  def _handle_upload(event: me.UploadEvent):
    state = me.state(FileState)
    state.file = event.file

  @staticmethod
  def _convert_contents_data_url(file: me.UploadedFile) -> str:
    return (
      f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
    )