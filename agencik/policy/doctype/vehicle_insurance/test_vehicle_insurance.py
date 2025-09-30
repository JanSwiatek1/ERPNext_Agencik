# Copyright (c) 2025, Jan and Contributors
# See license.txt

# import frappe
from frappe.tests.utils import FrappeTestCase

import frappe
import unittest
from frappe.utils import today, add_years

class TestVehicleInsurance(unittest.TestCase):
    def setUp(self):
        #  Tworzenie nowego Vehicle Insurance do testów
        self.insurance = frappe.get_doc({
            "doctype": "Vehicle Insurance",
            "brand": "Test Brand",
            "model": "Test Model",
            "year": 2020,
            "plate_no": "TEST123",

        }).insert()

    def tearDown(self):
        # Sprzątanie po testach
        frappe.delete_doc("Vehicle Insurance", self.insurance.name)

    def test_create_vehicle_insurance(self):
        # Test poprawnego tworzenia ubezpieczenia
        self.assertEqual(self.insurance.brand, "Test Brand")
        self.assertEqual(self.insurance.model, "Test Model")
        self.assertEqual(self.insurance.year, 2020)
        self.assertEqual(self.insurance.plate_no, "TEST123")


    def test_duplicate_plate_number_validation(self):
        # Test walidacji unikalności numeru rejestracyjnego
        duplicate_insurance = frappe.get_doc({
            "doctype": "Vehicle Insurance",
            "brand": "Different Brand",
            "model": "Different Model",
            "year": 2021,
            "plate_no": "TEST123",  

        })

        self.assertRaises(frappe.DuplicateEntryError, duplicate_insurance.insert)

if __name__ == '__main__':
    unittest.main()