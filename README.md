# PDF-Downloader-Testing

## Description
This repository aims to test an existing project, this being the Uge-4-PDFDownloader made by prismicious


## Getting started

### Instaling

#### Python libraries
```
pip install -r requirements.txt
```

#### Git submodules
To get the submodule (original codebase) do:
```
git submodule init
git submodule update
```

#### Changes
For the utils.utils file in Uge-4-PDFDownloader the data.values() need to be wrapped in list() same goes for row.values()

### Executing Program
To run the tests use command `pytest`


