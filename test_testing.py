from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Uge-4-PDFDownloader")))
from models.Report import PDFReport
from models.PDClient import PDClient
from models.Downloader import Downloader




@patch("pandas.read_excel")
def test_parse_excel_to_reports(mock_read_excel):
    mock_df = pd.DataFrame({
        "Pdf_URL": ["http://example.com"],
        "Report Html Address": ["http://backup.com"]
    })
    mock_df.index = ["123"]
    mock_read_excel.return_value = mock_df

    client = PDClient()
    reports = client.parse_excel_to_reports()

    assert len(reports) == 1
    assert isinstance(reports[0], PDFReport)

@patch("pandas.read_excel")
@patch("models.PDClient.append_to_csv")
def test_update_status(mock_append_to_csv, mock_read_excel):
    mock_read_excel.return_value = ""

    client = PDClient()
    client.update_status("123", True, 200)

    mock_append_to_csv.assert_called_once_with(
        'output/downloaded_reports.csv', 
        {'BRnum': '123', 'Downloaded': "Yes", 'Status Code': 200}
    )


@patch("models.Downloader.PDClient")
def test_set_reports(mock_pdclient):
    downloader = Downloader()
    reports = [PDFReport("123", "http://example.com", "http://backup.com")]
    downloader.set_reports(reports)
    assert downloader. pdf_reports == reports


@patch("Main.Downloader")
@patch("Main.PDClient")
@patch("utils.utils.create_folder_if_not_exists")
def test_run(mock_create_folder, mock_pdclient, mock_downloader):
    mock_pdclient_instance = mock_pdclient.return_value
    mock_downloader_instance = mock_downloader.return_value

    from Main import Main
    main = Main()
    main.run()

    mock_create_folder.assert_any_call("downloads")
    mock_create_folder.assert_any_call("output")
    mock_pdclient_instance.parse_excel_to_reports.assert_called_once()
    mock_downloader_instance.download.assert_called_once()