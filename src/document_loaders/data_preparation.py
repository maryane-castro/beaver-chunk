from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    ImageFormatOption,
    AsciiDocFormatOption,
    WordFormatOption,
)
from docling.datamodel.pipeline_options import PictureDescriptionVlmOptions
from docling.exceptions import ConversionError

from release.app.core.src.indexing.data_preparation.utils.detects_folder_or_file import (
    detects_folder_or_file,
)
from langchain_core.documents import Document

from release.app.core.src.indexing.data_preparation.graph_description_options import lms_local_options, remote_vlm_options


class DataPreparation:
    def __init__(
        self,
        repo_id="HuggingFaceTB/SmolVLM-256M-Instruct",
        prompt="Describe the image in three sentences. Be consise and accurate.",
        api_key=None,
        base_url="http://localhost:11434/chat/completions",
        model="gemma3:4b",
        provider_vlm=None
    ):
        self.pipeline_options = PdfPipelineOptions(
            enable_remote_services=True
        )
        self.pipeline_options.do_picture_description = True


        if provider_vlm == "remote":
            self.pipeline_options.picture_description_options = remote_vlm_options(
                api_key=api_key, base_url=base_url
            )
        elif provider_vlm == "local": 
            self.pipeline_options.picture_description_options = lms_local_options(
            model=model, base_url=base_url, 
        )
        else:
            self.pipeline_options.picture_description_options = PictureDescriptionVlmOptions(
                repo_id=repo_id,
                prompt=prompt,
            )

        self.pipeline_options.images_scale = 2.0
        self.pipeline_options.generate_picture_images = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.DOCX: WordFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.ASCIIDOC: AsciiDocFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.IMAGE: ImageFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
            }
        )

    def process_files(self, folder_or_file, format_output="txt"):
        """
        Converte documentos usando Docling e retorna uma lista de Documents (LangChain)
        e erros ocorridos no processo.
        """

        list_docs = []
        list_errors = []

        list_files = detects_folder_or_file(folder_or_file)

        for path_file in list_files:
            try:
                conv = self.converter.convert(path_file)
                doc = conv.document

                # Mapa de funções de exportação
                exporters = {
                    "txt": doc.export_to_text,
                    "markdown": doc.export_to_markdown,
                }

                if format_output not in exporters:
                    raise ValueError(
                        f"Formato inválido: '{format_output}'. "
                        f"Use um destes: {list(exporters.keys())}"
                    )

                # Executa exportação selecionada dinamicamente
                doc_extract = exporters[format_output]().replace("<!-- image -->", "")

                # Empacota em LangChain Document
                list_docs.append(
                    Document(
                        page_content=doc_extract,
                        metadata={"source": path_file},
                    )
                )

            except ConversionError as e:
                print(f"[ERRO] Falha ao converter {path_file}: {e}")
                list_errors.append({"file": path_file, "error": str(e)})

            except Exception as e:
                print(f"[ERRO] Erro inesperado em {path_file}: {e}")
                list_errors.append({"file": path_file, "error": str(e)})

        return list_docs, list_errors
