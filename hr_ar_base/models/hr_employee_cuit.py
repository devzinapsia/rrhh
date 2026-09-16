# Part of hr_ar_base. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrVersion(models.Model):
    # `identification_id`/`ssnid`/`passport_id` live here too (hr.employee
    # exposes them via `_inherits`), so the Argentine CUIT/CUIL follows the
    # same pattern instead of living directly on hr.employee.
    _inherit = "hr.version"

    l10n_ar_cuil = fields.Char(
        string="CUIT/CUIL",
        groups="hr.group_hr_user",
        tracking=True,
        inverse="_inverse_l10n_ar_cuil",
    )

    def _inverse_l10n_ar_cuil(self):
        """ Normalize using the same helper res.partner.vat relies on for
        Argentina, so the stored/displayed format is identical (compact,
        no separators). """
        partner_model = self.env["res.partner"]
        for version in self.filtered("l10n_ar_cuil"):
            version.l10n_ar_cuil = partner_model._format_vat_number("ar", version.l10n_ar_cuil)

    @api.constrains("l10n_ar_cuil")
    def _check_l10n_ar_cuil(self):
        partner_model = self.env["res.partner"]
        for version in self.filtered("l10n_ar_cuil"):
            if not partner_model._check_vat_number("ar", version.l10n_ar_cuil):
                raise ValidationError(_(
                    '"%(value)s" is not a valid CUIT/CUIL number.',
                    value=version.l10n_ar_cuil,
                ))


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.onchange("l10n_ar_cuil")
    def _onchange_l10n_ar_cuil_duplicate(self):
        """ Warn (non-blocking) when another employee in the same company
        already has this CUIT/CUIL. Archived employees are included in the
        search, other companies are not. """
        if not self.l10n_ar_cuil:
            return
        duplicate = self.env["hr.employee"].with_context(active_test=False).search([
            ("l10n_ar_cuil", "=", self.l10n_ar_cuil),
            ("company_id", "=", self.company_id.id),
            ("id", "!=", self._origin.id),
        ], limit=1)
        if duplicate:
            return {"warning": {
                "title": _("Duplicate CUIT/CUIL"),
                "message": _(
                    "Employee %(employee)s already has this CUIT/CUIL.",
                    employee=duplicate.name,
                ),
            }}
