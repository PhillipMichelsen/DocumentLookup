from io import BytesIO

import defusedxml.ElementTree
import httpx

from app.config import settings
from app.utils.minio_utils import minio_utils


def grobid_fulltext_pdf(bucket_name, object_name) -> str:
    file_obj = minio_utils.minio.get_object(bucket_name, object_name)
    file_content = file_obj.read()

    data = {'consolidateHeader': '1',
            'consolidateCitations': '1'}
    files = {'input': (object_name, BytesIO(file_content), 'application/pdf')}

    response = httpx.post(settings.grobid_fulltext_endpoint, data=data, files=files, timeout=500)

    if response.status_code == 200:
        return response.text
    raise Exception(f'Failed to process PDF with GROBID. Status code: {response.status_code}')


def process_header_pdf(raw_payload: dict) -> dict:
    # TODO: Implement process_header_pdf
    raise NotImplementedError('process_header_pdf not implemented')


def parse_grobid_output(grobid_output):
    """This function parses the output of GROBID and returns the divs and paragraphs.

    :param grobid_output:
    """
    parsed = defusedxml.ElementTree.fromstring(grobid_output)

    paragraphs = parsed.findall('.//tei:p', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    paragraphs = [' '.join(p.itertext()) for p in paragraphs]

    divs = parsed.findall('.//tei:div', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    divs = [' '.join(div.itertext()) for div in divs]

    return divs, paragraphs
