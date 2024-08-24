import unittest
import numpy as np
import os
from fastmrz import FastMRZ

fast_mrz = FastMRZ()

class TestFastMRZMethods(unittest.TestCase):

    def test_process_image(self):
        image_path = os.path.abspath("data/td3.jpg")
        processed_image = fast_mrz._process_image(image_path)
        self.assertIsInstance(processed_image, np.ndarray)
        self.assertEqual(processed_image.shape, (1, 256, 256, 3))

    def test_get_roi(self):
        output_data = np.random.rand(1, 256, 256, 1)
        image_path = os.path.abspath("data/td3.jpg")
        roi = fast_mrz._get_roi(output_data, image_path)
        self.assertIsInstance(roi, str)

    def test_cleanse_roi(self):
        raw_text = "P<UTOERIKSSON<<ANNA<MARIA<<< <<<<<<<<<  <<<<<<<\n\nL898902C36UTO7408122F1204159ZE184226B<<<<<10\n"
        cleansed_text = fast_mrz._cleanse_roi(raw_text)
        self.assertIsInstance(cleansed_text, str)

    def test_get_final_check_digit(self):
        input_string = (
            "'I<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<\nD231458907UTO7408122F1204159<<<<<<<6"
        )
        input_type = "TD2"
        final_check_digit = fast_mrz._get_final_check_digit(input_string, input_type)
        self.assertIsInstance(final_check_digit, str)

    def test_get_check_digit(self):
        input_string = "'I<UTOERIKSSON<<ANNA< MARIA<<<<< <<<<<<\nD231458907UTO7408122F1204159<<<<<<<6\n\n"
        check_digit = fast_mrz._get_check_digit(input_string)
        self.assertIsInstance(check_digit, str)

    def test_format_date(self):
        input_date = "220101"
        formatted_date = fast_mrz._format_date(input_date)
        self.assertIsInstance(formatted_date, str)

    def test_read_raw_mrz(self):
        image_path = os.path.abspath("data/td2.jpg")
        raw_mrz = fast_mrz.get_mrz(image_path, raw=True)
        self.assertIsInstance(raw_mrz, str)

    def test_read_mrz(self):
        image_path = os.path.abspath("data/td3.jpg")
        mrz_data = fast_mrz.get_mrz(image_path)
        self.assertIsInstance(mrz_data, dict)
        self.assertIn("status", mrz_data.keys())

    def test_read_mrz_nomrz(self):
        image_path = os.path.abspath("data/nomrz.jpg")
        mrz_data = fast_mrz.get_mrz(image_path)
        self.assertIsInstance(mrz_data, dict)
        self.assertIn("status", mrz_data.keys())

if __name__ == "__main__":
    unittest.main()
