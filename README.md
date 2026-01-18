# Supplier Credit Limit

Supplier Credit Limit implementation for ERPNext.

## Overview

ERPNext provides a built-in Credit Limit feature for Customers, but it does not
enforce credit limits for Suppliers by default.

This custom app adds Supplier Credit Limit validation, similar to Customer Credit
Limit, and enforces it during Purchase Order submission.

---

## How It Works

- Credit limit is maintained per Supplier and Company
- Validation is triggered when a Purchase Order is submitted
- Supplier exposure is calculated using unbilled Purchase Orders
- Current Purchase Order amount is added to the existing exposure
- If the total exceeds the credit limit and bypass is not enabled, the system
  blocks submission with an error message

---

## Technical Implementation

- Supplier Credit Limit is stored as a child table under Supplier
- Validation logic is implemented in `supplier_credit_limit/api.py`
- Event hook is registered in `supplier_credit_limit/hooks.py`
- Validation is executed on Purchase Order `before_submit`

---

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/sumathi289/supplier_credit_limit.git --branch develop
bench install-app supplier_credit_limit
bench restart

```

Sample Supplier Setup
###########################
Supplier: ABC Traders
Company: My Company
Credit Limit: 50,000
Bypass: No

Supplier: XYZ Suppliers
Company: My Company
Credit Limit: 1,00,000
Bypass: No

Supplier: Trusted Vendor
Company: My Company
Credit Limit: 25,000
Bypass: Yes

Supplier: Smart Phone Suppliers
Company: My Company
Credit Limit: Not Configured
###########################

Test Cases
Case 1: Credit Limit Exceeded ❌

Supplier: ABC Traders
Credit Limit: 50,000
Existing Purchase Order: 45,000
New Purchase Order: 15,000
Total Exposure: 60,000 > 50,000
Result: Purchase Order submission blocked with
"Credit Limit Crossed" error


Case 2: Under Credit Limit ✅
Supplier: XYZ Suppliers
Credit Limit: 1,00,000
Purchase Orders: 95,000 + 3,000
Total Exposure: 98,000 < 1,00,000
Result: Purchase Orders submitted successfully



Case 3: Bypass Enabled ✅
Supplier: Trusted Vendor
Credit Limit: 25,000
Bypass Credit Limit Check: Enabled
Purchase Orders: 25,000 + 10,000
Result: Purchase Order allowed due to bypass setting



Case 4: No Credit Limit Configured ✅
Supplier: Smart Phone Suppliers
Credit Limit: Not configured
Result: Purchase Order allowed without validation