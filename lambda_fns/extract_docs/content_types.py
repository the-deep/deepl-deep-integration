import requests
from enum import Enum
import logging

logging.getLogger().setLevel(logging.INFO)


class UrlTypes(str, Enum):
    HTML = 'html'
    PDF = 'pdf'
    DOCX = 'docx'
    PPTX = 'pptx'
    MSWORD = 'doc'


class ExtractContentType:
    def __init__(self):
        self.content_types_pdf = ('application/pdf', 'pdf')
        self.content_types_html = ('text/html', 'text/html; charset=utf-8',
                                   'text/html; charset=UTF-8', 'text/html;charset=utf-8', 'text/plain')
        self.content_types_docx = ('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.content_types_doc = ('application/msword')

    def get_content_type(self, url):
        try:
            response = requests.head(url)
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
            else:
                logging.warn(f'Could not determine the content-type of the {url}')
                return None
        except requests.exceptions.RequestException:
            logging.error(f'Exception occurred. Could not determine the content-type of the {url}')
            return None
