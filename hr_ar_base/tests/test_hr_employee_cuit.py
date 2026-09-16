# Part of hr_ar_base. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrEmployeeCuil(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env.company
        cls.company_b = cls.env["res.company"].create({"name": "Other Company"})
        # Computed and verified with stdnum.ar.cuit (the same module Odoo
        # uses for res.partner.vat on Argentina): valid check digit for
        # prefix 20 and base number 05536168.
        cls.valid_cuil = "20055361682"

    def test_valid_cuil_saves(self):
        employee = self.env["hr.employee"].create({
            "name": "Valid Employee",
            "l10n_ar_cuil": "20-05536168-2",
        })
        self.assertEqual(employee.l10n_ar_cuil, self.valid_cuil, "Should be stored compact, without dashes")

    def test_invalid_checksum_raises(self):
        with self.assertRaises(ValidationError):
            self.env["hr.employee"].create({
                "name": "Bad Checksum Employee",
                "l10n_ar_cuil": "20055361680",
            })

    def test_invalid_format_raises(self):
        with self.assertRaises(ValidationError):
            self.env["hr.employee"].create({
                "name": "Bad Format Employee",
                "l10n_ar_cuil": "ABC12345",
            })

    def test_duplicate_same_company_warns_but_does_not_block(self):
        first = self.env["hr.employee"].create({
            "name": "First Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        second = self.env["hr.employee"].new({
            "name": "Second Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        result = second._onchange_l10n_ar_cuil_duplicate()
        self.assertTrue(result and result.get("warning"), "Onchange should warn about the duplicate")
        self.assertIn(first.name, result["warning"]["message"])

        # create/write must not be blocked by the duplicate.
        second_saved = self.env["hr.employee"].create({
            "name": "Second Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        self.assertEqual(second_saved.l10n_ar_cuil, self.valid_cuil)

    def test_duplicate_other_company_does_not_warn(self):
        self.env["hr.employee"].create({
            "name": "First Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        other_company_employee = self.env["hr.employee"].new({
            "name": "Employee In Other Company",
            "company_id": self.company_b.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        result = other_company_employee._onchange_l10n_ar_cuil_duplicate()
        self.assertFalse(result, "No warning expected across different companies")

    def test_duplicate_detection_includes_archived_employees(self):
        archived = self.env["hr.employee"].create({
            "name": "Archived Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        archived.active = False

        new_employee = self.env["hr.employee"].new({
            "name": "New Employee",
            "company_id": self.company_a.id,
            "l10n_ar_cuil": self.valid_cuil,
        })
        result = new_employee._onchange_l10n_ar_cuil_duplicate()
        self.assertTrue(result and result.get("warning"), "Archived employees must count for duplicate detection")

    def test_field_present_in_views(self):
        views = {
            "form": self.env.ref("hr.view_employee_form"),
            "kanban": self.env.ref("hr.hr_kanban_view_employees"),
            "list": self.env.ref("hr.view_employee_tree"),
            "search": self.env.ref("hr.view_employee_filter"),
        }
        for view_type, view in views.items():
            with self.subTest(view_type=view_type):
                result = self.env["hr.employee"].get_view(view_id=view.id, view_type=view_type)
                self.assertIn("l10n_ar_cuil", result["models"]["hr.employee"], "Field missing from %s view" % view_type)
