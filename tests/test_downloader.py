import pytest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../Uge-4-PDFDownloader")))
from models.Downloader import Downloader
from models.Report import PDFReport
from utils.utils import append_to_csv
from requests.exceptions import SSLError, HTTPError


@patch("models.Downloader.append_to_csv")
def test_log_status_count(mock_append_to_csv):
    downloader = Downloader()
    downloader.log_status_count(200)
    downloader.log_status_count(404)
    downloader.log_status_count(200)

    # Verify the results dictionary is updated correctly
    assert downloader.results == {200: 2, 404: 1}

    # Verify append_to_csv is called with the correct arguments
    mock_append_to_csv.assert_any_call(
        "output/status_codes_count.csv",
        [{"Result": 200, "Count": 2}, {"Result": 404, "Count": 1}],
        "w"
    )


def test_set_reports():
    downloader = Downloader()
    reports = [PDFReport("123", "http://example.com", "http://backup.com")]
    downloader.set_reports(reports)

    # Verify the reports are set correctly
    assert downloader.pdf_reports == reports


@patch("os.path.getsize", return_value=True)
@patch("os.path.exists", return_value=True)
@patch("models.Downloader.PDClient")
@patch("models.Downloader.requests.Session")
def test_download_report_success(mock_session, mock_pdclient, mock_exists, mock_getsize):
    # Mock the response from the session
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/pdf"}
    mock_response.iter_content = MagicMock(return_value=[b"PDF content"])
    mock_session.return_value.get.return_value.__enter__.return_value = mock_response

    # Mock the PDClient's update_status method
    mock_pdclient_instance = mock_pdclient.return_value

    # Create a Downloader instance
    downloader = Downloader()

    # Mock the file system
    with patch("builtins.open", mock_open()) as mock_file:
        report = PDFReport("123", "http://example.com", None)
        downloader.download_report(report)

        # Verify the file was written
        mock_file.assert_any_call("downloads\\123.pdf", "wb")
        mock_file().write.assert_any_call(b"PDF content")

        # Verify the status was updated
        mock_pdclient_instance.update_status.assert_called_once_with("123", True, 200)


@patch("models.Downloader.Downloader.log_status_count")
@patch("models.Downloader.PDClient")
@patch("models.Downloader.requests.Session")
def test_download_report_ssl_error(mock_session, mock_pdclient, mock_logger):
    # Mock the session to raise an SSLError
    mock_session.return_value.get.side_effect = SSLError("SSL Error")

    # Mock the PDClient's update_status method
    mock_pdclient_instance = mock_pdclient.return_value

    # Create a Downloader instance
    downloader = Downloader()

    # Mock the logger
    with patch("models.Downloader.logger.warning") as mock_logger:
        report = PDFReport("123", "http://example.com", None)
        downloader.download_report(report)

        # Verify the logger was called
        mock_logger.assert_called_once_with(
            "Retrying http://example.com with SSL verification disabled due to SSL error."
        )

        # Verify the status was updated with "SSL Error"
        mock_pdclient_instance.update_status.assert_called_once_with("123", False, "SSL Error")


@patch("models.Downloader.Downloader.log_status_count")
@patch("models.Downloader.PDClient")
@patch("models.Downloader.requests.Session")
def test_download_report_http_error(mock_session, mock_pdclient, mock_logger):
    # Mock the session to raise an HTTPError
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_session.return_value.get.return_value.__enter__.return_value = mock_response
    mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")

    # Mock the PDClient's update_status method
    mock_pdclient_instance = mock_pdclient.return_value

    # Create a Downloader instance
    downloader = Downloader()

    report = PDFReport("123", "http://example.com", None)
    downloader.download_report(report)

    # Verify the status was updated with 404
    mock_pdclient_instance.update_status.assert_called_once_with("123", False, 404)



def test_download():

    # Create a Downloader instance
    downloader = Downloader()
    reports = [PDFReport("123", "http://example.com", None)]
    downloader.set_reports(reports)

    downloader.download()
