import requests
from enum import Enum


class UrlTypes(str, Enum):
    HTML = 'html'
    PDF = 'pdf'
    DOCX = 'docx'
    PPTX = 'pptx'
    MSWORD = 'doc'


class ExtractContentType:
    def __init__(self):
        self.content_types_pdf = ('application/pdf', 'pdf')
        self.content_types_html = ('text/html', 'text/html; charset=utf-8', 'text/plain')

    def get_content_type(self, url):
        try:
            response = requests.head(url)
            content_type = response.headers['Content-Type']

            print(f'The content type of {url} is {content_type}')

            if url.endswith(".pdf"):
                return UrlTypes.PDF.value
            elif content_type in self.content_types_pdf:
                return UrlTypes.PDF.value
            elif content_type in self.content_types_html:
                return UrlTypes.HTML.value
            else:
                print(f'Could not determine the content-type of the {url}')
                return None
        except requests.exceptions.RequestException:
            print(f'Exception occurred. Could not determine the content-type of the {url}')
            return None
