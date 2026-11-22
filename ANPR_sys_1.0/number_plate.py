"""Local OpenCV and Tesseract learning prototype."""

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np
import pytesseract


CASCADE_PATH = Path(__file__).resolve().parent / "model" / "haarcascade_russian_plate_number.xml"
MIN_AREA = 500


def load_cascade(path=CASCADE_PATH):
    if not path.is_file():
        raise RuntimeError(f"Haar cascade not found: {path}")
    cascade = cv2.CascadeClassifier(str(path))
    if cascade.empty():
        raise RuntimeError(f"Could not load Haar cascade: {path}")
    return cascade


def is_valid_plate(width, height):
    return height > 0 and 2.0 < width / height < 6.0


def read_text(image, config="--psm 11"):
    return pytesseract.image_to_string(image, lang="eng", config=config).strip()


def run_self_check(cascade):
    # Test asset loading and preprocessing without opening a camera.
    blank = np.zeros((480, 640), dtype=np.uint8)
    if len(cascade.detectMultiScale(blank, scaleFactor=1.8, minNeighbors=5, minSize=(40, 40))):
        raise RuntimeError("The cascade returned a detection on a blank synthetic frame.")

    # Test OCR separately; the cascade is not expected to find this artificial label.
    label = np.full((120, 520), 255, dtype=np.uint8)
    cv2.putText(label, "DEMO 123", (30, 86), cv2.FONT_HERSHEY_SIMPLEX, 2.8, 0, 5, cv2.LINE_AA)
    result = read_text(label, config="--psm 7")
    if "".join(result.split()) != "DEMO123":
        raise RuntimeError(f"Unexpected synthetic OCR result: {result!r}.")
    print("Self-check passed: bundled cascade loaded; synthetic text read as DEMO 123.")
    print("No webcam used or output files written.")


def run_webcam(cascade, camera_index, output_dir):
    cap = cv2.VideoCapture(camera_index)
    try:
        if not cap.isOpened():
            raise RuntimeError(f"Could not open camera {camera_index}. Check the index and camera permissions.")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
        count = 0

        while True:
            success, frame = cap.read()
            if not success:
                raise RuntimeError("Could not read a frame from the camera.")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            boxes = cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=5, minSize=(40, 40))
            for x, y, width, height in boxes:
                if width * height <= MIN_AREA or not is_valid_plate(width, height):
                    continue
                plate = frame[y:y + height, x:x + width]
                # OCR reads a clean crop, before preview annotations are applied.
                result = read_text(cv2.cvtColor(plate, cv2.COLOR_BGR2RGB))
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.putText(frame, result.replace("\n", " ") or "Number plate", (x, max(y - 5, 15)),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                if output_dir is not None:
                    # Avoid overwriting prior files if the output directory is reused.
                    while True:
                        path = output_dir / f"scanned_plate_{count}.txt"
                        count += 1
                        try:
                            with path.open("x", encoding="utf-8") as file:
                                file.write(result)
                        except FileExistsError:
                            continue
                        break
            cv2.imshow("Result", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-check", action="store_true", help="Use only data generated in memory.")
    mode.add_argument("--webcam", action="store_true", help="Open a webcam on an authorised lab setup.")
    parser.add_argument("--camera-index", type=int, default=0, help="OpenCV camera index (default: 0).")
    parser.add_argument("--output-dir", type=Path, help="Optional folder for local OCR text from webcam mode.")
    parser.add_argument("--tesseract", help="Explicit executable path, if Tesseract is not on PATH.")
    args = parser.parse_args(argv)
    if args.self_check and args.output_dir is not None:
        parser.error("--output-dir applies only to --webcam")
    if args.camera_index < 0:
        parser.error("--camera-index must be non-negative")

    if args.tesseract:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract
    try:
        # Fail early with a clear message before opening a camera.
        pytesseract.get_tesseract_version()
        cascade = load_cascade()
        if args.self_check:
            run_self_check(cascade)
        else:
            run_webcam(cascade, args.camera_index, args.output_dir)
        return 0
    except pytesseract.TesseractNotFoundError:
        print("Tesseract was not found. Install it and add it to PATH, or pass --tesseract.", file=sys.stderr)
    except (OSError, RuntimeError, cv2.error) as error:
        print(f"Error: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
