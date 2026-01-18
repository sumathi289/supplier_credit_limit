# Supplier Credit Limit

Supplier Credit Limit implementation for ERPNext.

## Overview

ERPNext provides built-in credit limit validation for Customers, but it does not
enforce credit limits for Suppliers by default.

This custom app adds Supplier Credit Limit validation during Purchase Order
submission to prevent exceeding the allowed credit limit for a supplier.

## How It Works

- Credit limit is maintained per Supplier and Company
- Validation is triggered on Purchase Order submission
- Supplier outstanding amount is calculated using GL Entry
- Current Purchase Order amount is added to outstanding
- If the credit limit is exceeded, submission is blocked with an error

## Technical Implementation

- Validation logic is implemented in `supplier_credit_limit/api.py`
- Event hook is registered in `supplier_credit_limit/hooks.py`
- Purchase Order `on_submit` event is used for validation

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/sumathi289/supplier_credit_limit.git --branch develop
bench install-app supplier_credit_limit

```

