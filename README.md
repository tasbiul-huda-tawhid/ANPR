# Automated Number Plate Recognition (ANPR) System

A Python learning project that uses OpenCV to detect candidate number plates in webcam frames and Tesseract to extract text. The script saves the OCR output to local text files. The current setup uses Windows-specific paths and has not been validated for Australian plates.

## Prerequisites

- Python 3
- OpenCV and pytesseract (see [`requirements.txt`](ANPR_sys_1.0/requirements.txt))
- Tesseract OCR installed separately
- A webcam and the bundled Haar cascade file

The repository currently includes [machine-specific Windows notes](ANPR_sys_1.0/ReadMeToRunProject.txt). They are not a portable setup guide.

Author: Tasbiul Huda Tawhid
