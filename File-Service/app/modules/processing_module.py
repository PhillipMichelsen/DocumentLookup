import httpx
import re
import xml.etree.ElementTree
from io import BytesIO
from typing import List, Tuple
from app.config import service_endpoints


def grobid_fulltext_pdf(presigned_url_download: str) -> bytes:
    file = httpx.get(presigned_url_download)

    files = {'input': BytesIO(file.content), 'segmentSentences': '1'}
    response = httpx.post(url=service_endpoints.process_fulltext_grobid, files=files, timeout=60)

    return response.content


def process_header_pdf(raw_payload: dict) -> dict:
    raise NotImplementedError('process_header_pdf not implemented')


def parse_grobid_output(grobid_output):
    parsed = xml.etree.ElementTree.fromstring(grobid_output)

    paragraphs = parsed.findall('.//tei:p', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    paragraphs = [' '.join(p.itertext()) for p in paragraphs]

    sentences = parsed.findall('.//tei:s', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    sentences = [sentence.text for sentence in sentences]

    return paragraphs, sentences
