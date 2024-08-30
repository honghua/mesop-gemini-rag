import base64

import mesop as me
from datastore import DataStoreGenerator

@me.stateclass
class FileState:
    file: me.UploadedFile

class Uploader:
  @staticmethod
  def _handle_upload(event: me.UploadEvent):
    state = me.state(FileState)
    state.file = event.file
    files = []
    files.append(state.file)
    DataStoreGenerator.process_files(files, overwrite=True)
    

  @staticmethod
  def _convert_contents_data_url(file: me.UploadedFile) -> str:
    return (
      f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
    )