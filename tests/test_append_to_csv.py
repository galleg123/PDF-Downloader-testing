from unittest.mock import patch, mock_open, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Uge-4-PDFDownloader")))
from utils.utils import append_to_csv
import pytest

# Append to csv
## Correct, data type list, data type dict, wrong data type



@patch("builtins.open", new_callable=mock_open)
@patch("csv.writer")
def test_append_dict_to_csv(mock_csv_writer, mock_file):
    # Test appending to a CSV file
    data = {"name": "John", "age": 30}
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    append_to_csv("test.csv", data)

    # Assert that open was called twice (once for checking and once for writing)
    assert mock_file.call_count == 2

    # Assert that the file was opened in append mode for writing
    mock_file.assert_any_call("test.csv", "a", newline="")

    # Assert that the writer wrote the headers and the data
    mock_writer_instance.writerow.assert_any_call(data.keys())
    mock_writer_instance.writerow.assert_any_call(list(data.values()))

@patch("builtins.open", new_callable=mock_open)
@patch("csv.writer")
def test_append_list_of_dict_to_csv(mock_csv_writer, mock_file):
    # Test appending to a CSV file
    data = [{"name": "John", "age": 30},{"name": "Johnny", "age": 32}]
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    append_to_csv("test.csv", data)

    # Assert that open was called twice (once for checking and once for writing)
    assert mock_file.call_count == 2

    # Assert that the file was opened in append mode for writing
    mock_file.assert_any_call("test.csv", "a", newline="")

    # Assert that the writer wrote the headers and the data
    mock_writer_instance.writerow.assert_any_call(data[0].keys())
    mock_writer_instance.writerow.assert_any_call(data[1].keys())
    mock_writer_instance.writerow.assert_any_call(list(data[0].values()))
    mock_writer_instance.writerow.assert_any_call(list(data[1].values()))


@patch("builtins.open", new_callable=mock_open)
@patch("csv.writer")
def test_append_int_to_csv(mock_csv_writer, mock_file):
    # Test appending to a CSV file
    data = 30
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    with pytest.raises(ValueError):
        append_to_csv("test.csv", data)

