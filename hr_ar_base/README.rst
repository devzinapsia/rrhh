====================
RRHH Base Argentina
====================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

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

**Table of contents**

.. contents::
   :local:

Configuration
=============

No configuration is needed. Installing the module is enough for the
CUIT/CUIL field to appear on the employee form, kanban card, list and
search views.

Usage
=====

#. Go to *Employees > Employees* and open an employee.
#. On the *Personal* tab, under *Citizenship*, fill in the **CUIT/CUIL**
   field.
#. The value is validated and normalized (dashes/spaces removed) on
   save. An invalid CUIT/CUIL blocks saving with an error.
#. If another employee in the same company already has the same
   CUIT/CUIL (including archived employees), a warning is shown, but
   saving is still allowed.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/devzinapsia/rrhh/issues>`_.

Credits
=======

Authors
-------

* Zinapsia
