# Automatic Number Plate Recognition (ANPR) Prototype

A Python computer vision learning project by Tasbiul Huda Tawhid. OpenCV uses a bundled Haar cascade to propose candidate regions in webcam frames. Tesseract reads text from those regions. It runs locally; text export is off unless explicitly enabled.

## Setup

Install Python 3 and [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) with English language data. Check that `tesseract --version` works in your terminal. From the repository root:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r ANPR_sys_1.0/requirements.txt
```

Use `python3` instead of `python` to create the virtual environment if that is how Python is installed. If Tesseract is not on your PATH, append `--tesseract "/path/to/tesseract"` with your actual executable path.

## Try it without a camera

```sh
python ANPR_sys_1.0/number_plate.py --self-check
python -m unittest discover -s tests -v
```

The self-check loads the bundled cascade, confirms a blank image yields no candidate, then runs Tesseract separately on a generated label reading `DEMO 123`. It does not use a webcam, open a window or write output files. It does not validate plate detection or end-to-end recognition accuracy.

## Optional webcam demo

Use an authorised lab setup with synthetic test material, not traffic or other people's plates. The webcam mode requires a supported desktop GUI and camera permissions.

```sh
python ANPR_sys_1.0/number_plate.py --webcam
```

Press **q** in the preview window to stop. Use `--camera-index 1` for a different camera. By default results only appear in the preview. To keep local text from a synthetic demo, add `--output-dir plate_number`; the app will not save video or images. Don't commit capture output.

## Limitations

The bundled model targets Russian-style plates. This prototype has not been validated for Australian or other real plates, variable lighting or motion, or production use. No tracking, logging backend, or deployment is included. The hardware camera and its display window were not exercised in the portability checks.
