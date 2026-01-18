import frappe
from frappe import _
from frappe.utils import flt


def validate_supplier_credit_limit(doc, method):
    supplier = doc.supplier
    company = doc.company

    if not supplier or not company:
        return

    credit_limit_row = frappe.db.get_value(
        "Supplier Credit Limit",
        {
            "parent": supplier,
            "parenttype": "Supplier",
            "company": company,
        },
        ["credit_limit", "bypass_credit_limit_check_at_purchase_order"],
        as_dict=True,
    )

    if not credit_limit_row:
        return

    if credit_limit_row.bypass_credit_limit_check_at_purchase_order:
        return

    credit_limit = flt(credit_limit_row.credit_limit)

    outstanding = get_supplier_outstanding(supplier, company)
    outstanding += flt(doc.base_grand_total)

    if credit_limit > 0 and outstanding > credit_limit:
        frappe.throw(
            _("Credit limit has been crossed for supplier {0} ({1} / {2})").format(
                supplier, outstanding, credit_limit
            ),
            title=_("Credit Limit Crossed"),
        )


def get_supplier_outstanding(supplier, company):
    outstanding = frappe.db.sql(
        """
        SELECT SUM(credit) - SUM(debit)
        FROM `tabGL Entry`
        WHERE party_type = 'Supplier'
        AND party = %s
        AND company = %s
        AND is_cancelled = 0
        """,
        (supplier, company),
    )

    return flt(outstanding[0][0]) if outstanding and outstanding[0][0] else 0
