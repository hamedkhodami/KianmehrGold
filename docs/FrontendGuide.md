# 🎨 Frontend Development Guide

## Purpose

This document helps frontend developers identify:

- Active pages
- Templates
- Components
- UI priorities
- Current implementation status

---
## TailwindCSS version

- TailwindCSS: 3.2.7
- Autoprefixer: 10.4.14
- PostCSS: 8.4.21

# Current Status

---

## accounts

- Login page  
  → `templates/account/login.html`  
  **Status:** ❌ 

- Registration page  
  → `templates/account/signup.html`  
  **Status:** ❌ 

- Forgot password pages  
  → `templates/account/password/get_phone.html`  
  → `templates/account/password/reset_pass_confirm.html`  
  → `templates/account/password/reset_pass_complete.html`  
  **Status:** ❌ 

- Personal information page  
  → `templates/account/profile.html`  
  **Status:** ❌ 

- Bank information page  
  → `templates/account/bank_account.html`  
  **Status:** ❌ 

- Admin user detail page  
  → `templates/account/user_detail.html`  
  **Status:** ❌ 

---

## wallet

- Wallet dashboard page  
  → `templates/wallet/wallet.html`  
  **Status:** ❌ 

- Wallet withdrawal request page  
  → `templates/wallet/withdraw_request.html`  
  **Status:** ❌ 

- Wallet transaction details page  
  → `templates/wallet/wallet_transaction_detail.html`  
  **Status:** ❌ 

- Admin withdrawal requests list page  
  → `templates/wallet/admin/withdraw_request_list.html`  
  **Status:** ❌ 

- Admin withdrawal request detail page  
  → `templates/wallet/admin/withdraw_request_detail.html`  
  **Status:** ❌ 

- Withdrawal review table partial  
  → `templates/wallet/partials/withdraw_requests_table.html`  
  **Status:** ❌ 

---

## product

- Product list page  
  → `templates/product/product_list.html`  
  **Status:** ❌ 

- Product detail page  
  → `templates/product/product_detail.html`  
  **Status:** ❌ 

- Coin list page  
  → `templates/product/coin_list.html`  
  **Status:** ❌ 

---

## order

- Invoice list page  
  → `templates/order/invoice_list.html`  
  **Status:** ❌ 

- Invoice detail page  
  → `templates/order/invoice_detail.html`  
  **Status:** ❌ 

- Sell melted gold list (admin)  
  → `templates/order/sell_melted_gold_list.html`  
  **Status:** ❌ 

- Sell melted gold list (user)  
  → `templates/order/user_sell_melted_gold_list.html`  
  **Status:** ❌ 

- Invoice PDF  
  → `templates/order/invoice/invoice_pdf.html`  
  **Status:** ❌ 

---

## payment

- Fake gateway page  
  → `templates/payment/gateway.html`  
  **Status:** ❌ Backend Not Started – ❌ Frontend Not Started

---

## dashboard

- Customer dashboard  
  → `templates/dashboard/dashboard_customer.html`  
  **Status:** ❌ 

- Admin dashboard  
  → `templates/dashboard/dashboard_admin.html`  
  **Status:** ❌ 

- Dashboard main  
  → `templates/dashboard/dashboard.html`  
  **Status:** ❌ 

---

## public

- Homepage  
  → `templates/public/index.html`  
  **Status:** ❌ 

- About us  
  → `templates/public/about.html`  
  **Status:** ❌ 

- Article list  
  → `templates/public/article_list.html`  
  **Status:** ❌ 

- Article detail  
  → `templates/public/article_detail.html`  
  **Status:** ❌

---

## Main Template Structure

templates/

- base/
- public/
- account/
- dashboard/
- wallet/
- product/
- order/

---