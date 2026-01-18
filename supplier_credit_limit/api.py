import frappe
from frappe import _
from frappe.utils import flt


def validate_supplier_credit_limit(doc, method):
    if not doc.supplier or not doc.company:
        return

    credit_limit_row = frappe.db.get_value(
        "Supplier Credit Limit",
        {
            "parent": doc.supplier,
            "parenttype": "Supplier",
            "company": doc.company,
        },
        ["credit_limit", "bypass_credit_limit_check_at_purchase_order"],
        as_dict=True,
    )

    # No credit limit set
    if not credit_limit_row:
        return

    # Bypass enabled
    if credit_limit_row.bypass_credit_limit_check_at_purchase_order:
        return

    credit_limit = flt(credit_limit_row.credit_limit)
    if credit_limit <= 0:
        return

    # ONLY Purchase Order exposure
    outstanding = get_supplier_po_outstanding(
        supplier=doc.supplier,
        company=doc.company,
        current_po=doc.name,
    )

    total_exposure = outstanding + flt(doc.base_grand_total)

    if total_exposure > credit_limit:
        frappe.throw(
            _("Credit Limit Crossed for supplier {0} ({1} / {2})").format(
                doc.supplier,
                frappe.format(total_exposure),
                frappe.format(credit_limit),
            ),
            title=_("Credit Limit Crossed"),
        )


def get_supplier_po_outstanding(supplier, company, current_po):
    """
    Outstanding calculated ONLY from unbilled Purchase Orders
    """

    po_outstanding = frappe.db.sql(
        """
        SELECT SUM(
            base_grand_total * (1 - IFNULL(per_billed, 0) / 100)
        )
        FROM `tabPurchase Order`
        WHERE docstatus = 1
          AND supplier = %s
          AND company = %s
          AND status NOT IN ('Completed', 'Cancelled')
          AND name != %s
        """,
        (supplier, company, current_po),
    )[0][0] or 0

    return flt(po_outstanding)
