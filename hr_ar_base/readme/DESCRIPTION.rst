This module is the base for Argentina-specific HR functionality at
Zinapsia. It currently adds a CUIT/CUIL field to the Employees form, and
is expected to grow with further Argentina-specific HR fields and
features over time, all living inside this same module.

CUIT/CUIL field
================

Adds a **CUIT/CUIL** field to the employee form, validated with the same
check-digit algorithm and stored/displayed in the same format (compact,
no separators) that Odoo already uses for the VAT field of Argentine
Customers/Vendors (``res.partner.vat``). That validation is reused
directly from the ``base_vat`` module (``res.partner._check_vat_number``/
``_format_vat_number``), which in turn relies on the ``stdnum.ar.cuit``
library, so no validation logic is reimplemented here.

If another active or archived employee in the same company already has
the same CUIT/CUIL, a non-blocking warning is shown; the same number can
legitimately repeat across different companies of the same group.
