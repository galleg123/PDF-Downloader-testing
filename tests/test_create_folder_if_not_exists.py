from unittest.mock import patch, mock_open, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Uge-4-PDFDownloader")))
from utils.utils import create_folder_if_not_exists
import pytest



@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
def test_create_folder_if_not_exists_doesnt_exist(mock_exists, mock_makedirs):
    create_folder_if_not_exists("test_folder")
    mock_exists.assert_called_once_with("test_folder")
    mock_makedirs.assert_called_once_with("test_folder")


@patch("os.makedirs")
@patch("os.path.exists", return_value=True)
def test_create_folder_if_not_exists_already_exists(mock_exists, mock_makedirs):
    create_folder_if_not_exists("test_folder")
    mock_exists.assert_called_once_with("test_folder")
    mock_makedirs.assert_not_called()