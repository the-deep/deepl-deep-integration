import os
import requests
from enum import Enum
import logging
try:
    from wget import download
except ImportError:
    from .wget import download

logging.getLogger().setLevel(logging.INFO)


class UrlTypes(str, Enum):
    HTML = 'html'
    PDF = 'pdf'
    DOCX = 'docx'
    PPTX = 'pptx'
    PPT = 'ppt'
    MSWORD = 'doc'
    XLSX = 'xlsx'
    XLS = 'xls'
    IMG = 'img'


class ExtractContentType:
    def __init__(self):
        self.content_types_pdf = ('application/pdf', 'pdf')
        self.content_types_html = ('text/html', 'text/html; charset=utf-8', 'text/html;charset=UTF-8',
                                   'text/html; charset=UTF-8', 'text/html;charset=utf-8', 'text/plain')
        self.content_types_docx = ('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.content_types_doc = ('application/msword')
        self.content_types_pptx = ('application/vnd.openxmlformats-officedocument.presentationml.presentation')
        self.content_types_ppt = ('application/vnd.ms-powerpoint')
        self.content_types_xlsx = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.content_types_xls = ('application/vnd.ms-excel')
        self.content_types_img = ('image/jpeg', 'image/gif', 'image/png', 'image/svg+xml', 'image/webp', 'image/bmp', 'image/tiff')

    def get_content_type(self, url, req_headers):
        try:
            response = requests.head(url, headers=req_headers)
            content_type = response.headers['Content-Type']

            logging.info(f'The content type of {url} is {content_type}')

            if url.endswith(".pdf"):
                return UrlTypes.PDF.value
            elif content_type in self.content_types_pdf:
                return UrlTypes.PDF.value
            elif content_type in self.content_types_html:
                return UrlTypes.HTML.value
            elif url.endswith(".docx") or content_type in self.content_types_docx:
                return UrlTypes.DOCX.value
            elif url.endswith(".doc") or content_type in self.content_types_doc:
                return UrlTypes.MSWORD.value
            elif url.endswith(".xlsx") or content_type in self.content_types_xlsx:
                return UrlTypes.XLSX.value
            elif url.endswith(".xls") or content_type in self.content_types_xls:
                return UrlTypes.XLS.value
            elif url.endswith(".pptx") or content_type in self.content_types_pptx:
                return UrlTypes.PPTX.value
            elif url.endswith(".ppt") or content_type in self.content_types_ppt:
                return UrlTypes.PPT.value
            elif (content_type in self.content_types_img or 
                any([
                    url.endswith(f".{extension}") for extension in [
                        "jpg", "jpeg", "png", "gif", "bmp"
                    ]
                ])
            ):
                return UrlTypes.IMG.value
            else:
                try:
                    temp_filepath = download(url, out="/tmp/")
                except Exception as e:
                    logging.error(f"Error while downloading the file from {url} to check the file extension.")
                    return None
                EXTENSION_TO_ENUM_MAP = {
                    "pdf": UrlTypes.PDF,
                    "docx": UrlTypes.DOCX,
                    "doc": UrlTypes.MSWORD,
                    "xlsx": UrlTypes.XLSX,
                    "xls": UrlTypes.XLS,
                    "pptx": UrlTypes.PPTX,
                    "ppt": UrlTypes.PPT,
                    # Images
                    "jpg": UrlTypes.IMG,
                    "jpeg": UrlTypes.IMG,
                    "png": UrlTypes.IMG,
                    "gif": UrlTypes.IMG,
                    "bmp": UrlTypes.IMG,
                }
                file_extension = temp_filepath.split(".")[-1]
                if file_extension not in EXTENSION_TO_ENUM_MAP:
                    logging.warn(f"Could not determine the content-type of the {url}")
                    return None
                return EXTENSION_TO_ENUM_MAP[file_extension].value
        except requests.exceptions.RequestException as e:
            logging.error(f"Exception occurred: {str(e)}. Could not determine the content-type of the {url}.", exc_info=True)
            return None
