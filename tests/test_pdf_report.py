from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Uge-4-PDFDownloader")))
from models.Report import PDFReport




def test_pdf_report_initialization():
    report = PDFReport("123", "http://example.com", "http://backup.com")
    assert report.brnum == "123"
    assert report.pdf_url == "http://example.com"
    assert report.backup_url == "http://backup.com"


def test_pdf_report_initialization_no_urls():
    report = PDFReport("123", "", "")
    assert report.brnum == "123"
    assert report.pdf_url == ""
    assert report.backup_url == ""

def test_pdf_report_initialization_main_url():
    report = PDFReport("123", "http://example.com", "")
    assert report.brnum == "123"
    assert report.pdf_url == "http://example.com"
    assert report.backup_url == ""


def test_pdf_report_initialization_backup_url():
    report = PDFReport("123", "", "http://backup.com")
    assert report.brnum == "123"
    assert report.pdf_url == ""
    assert report.backup_url == "http://backup.com"


def test_pdf_report_validation():
    report = PDFReport("123", "", "http://backup.com")
    assert report.pdf_url == "http://backup.com"
