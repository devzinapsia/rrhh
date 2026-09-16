# Part of hr_ar_base. See LICENSE file for full copyright and licensing details.

{
    "name": "RRHH Base Argentina",
    "summary": "Base module for Argentina-specific HR features, starting with employee CUIT/CUIL",
    "version": "19.0.1.0.0",
    "category": "Human Resources",
    "license": "AGPL-3",
    "author": "Zinapsia",
    "website": "https://www.zinapsia.com",
    "depends": [
        "hr",
        "base_vat",
    ],
    "data": [
        "views/hr_employee_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
