import base64
import json
from datetime import datetime
import io

from wasabi import msg

from goldenverba.components.document import Document
from goldenverba.components.interfaces import Reader
from goldenverba.components.types import FileData

class MultiModalReader(Reader):
    """
    The MultiModalReader reads .png, .jpg, .jpeg, .mp3, .mp4 and .wav files.
    """

    def __init__(self):
        super().__init__()
        self.name = "MultiModalReader"
        self.description = "Imports images, audio and video files."
        #self.requires_library = ["pypdf", "docx"]

    def load(
        self, fileData: list[FileData], textValues: list[str], logging: list[dict]
    ) -> tuple[list[Document], list[str]]:

        documents = []
        
        for file in fileData:
            msg.info(f"Loading in {file.filename}")
            logging.append({"type": "INFO", "message": f"Importing {file.filename}"})

            decoded_bytes = base64.b64decode(file.content)

            if file.extension in ["png", "jpg", "jpeg"]:
                try:
                    document = Document(
                        name=file.filename,
                        text=decoded_bytes,
                        type=self.config["document_type"].image,
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )
                    documents.append(document)

                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(
                        {
                            "type": "ERROR",
                            "message": f"Failed to load {file.filename} : {str(e)}",
                        }
                    )
            elif file.extension in ["mp3", "wav"]:
                try:
                    document = Document(
                        name=file.filename,
                        text=decoded_bytes,
                        type=self.config["document_type"].audio,
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )
                    documents.append(document)

                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(
                        {
                            "type": "ERROR",
                            "message": f"Failed to load {file.filename} : {str(e)}",
                        }
                    )
            elif file.extension in ["mp4"]:
                try:
                    document = Document(
                        name=file.filename,
                        text=decoded_bytes,
                        type=self.config["document_type"].video,
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )
                    documents.append(document)

                except Exception as e:
                    msg.warn(f"Failed to load {file.filename} : {str(e)}")
                    logging.append(
                        {
                            "type": "ERROR",
                            "message": f"Failed to load {file.filename} : {str(e)}",
                        }
                    )
            else:
                msg.warn(
                    f"{file.filename} with extension {file.extension} not supported by MultiModalReader."
                )
                logging.append(
                    {
                        "type": "WARNING",
                        "message": f"{file.filename} with extension {file.extension} not supported by MultiModalReader.",
                    }
                )


        return documents, logging