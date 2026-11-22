"""Non-camera unit checks for the portable entry point."""

from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ANPR_sys_1.0"))
import number_plate


class NumberPlateTests(unittest.TestCase):
    def test_aspect_ratio_boundaries(self):
        self.assertTrue(number_plate.is_valid_plate(400, 100))
        self.assertFalse(number_plate.is_valid_plate(200, 100))
        self.assertFalse(number_plate.is_valid_plate(600, 100))
        self.assertFalse(number_plate.is_valid_plate(400, 0))

    def test_bundled_cascade_loads(self):
        self.assertTrue(number_plate.CASCADE_PATH.is_absolute())
        self.assertFalse(number_plate.load_cascade().empty())

    def test_missing_cascade_has_clear_error(self):
        path = number_plate.CASCADE_PATH.with_name("no-such-cascade.xml")
        with self.assertRaisesRegex(RuntimeError, "Haar cascade not found"):
            number_plate.load_cascade(path)

    def test_self_check_never_opens_a_camera(self):
        output = io.StringIO()
        with patch.object(number_plate.cv2, "VideoCapture") as camera:
            with patch.object(number_plate.pytesseract, "get_tesseract_version"):
                with patch.object(number_plate, "read_text", return_value="DEMO 123"):
                    with redirect_stdout(output):
                        result = number_plate.main(["--self-check"])
            camera.assert_not_called()
        self.assertEqual(result, 0)
        self.assertIn("Self-check passed", output.getvalue())

    def test_missing_tesseract_reports_error_without_opening_camera(self):
        error = io.StringIO()
        with patch.object(number_plate.cv2, "VideoCapture") as camera:
            with patch.object(number_plate.pytesseract, "get_tesseract_version",
                              side_effect=number_plate.pytesseract.TesseractNotFoundError):
                with patch.object(sys, "stderr", error):
                    self.assertEqual(number_plate.main(["--webcam"]), 1)
            camera.assert_not_called()
        self.assertIn("Tesseract was not found", error.getvalue())


if __name__ == "__main__":
    unittest.main()
