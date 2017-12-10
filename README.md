# treasurer_tools
A Django-based system to assist Non-Profit Organization treasurers in managing/tracking finances

## Planning and Outlines
### Packages to Install
django-simple-history
django-allauth

### Apps To Create
#### Payee/Payer
- App Name: payee_payer
- Models
  - demographics
    - name
	- address
	- city
	- province
	- country 
	- postal code
	- phone
	- fax
	- email
	- status
	  - active
	  - inactive
	- history

### Documents
- App Name: documents
- Models
  - pdf
	- location
	- date_uploaded
		
### Financial Codes
- App Name: financial_codes
- Models
  - BudgetYear
	- date_start
	- date_end
  - FinancialCodeSystem
    - title
	- status
  - FinancialCodeGroup
    - title
	- description
	- status
  - FinancialCode
    - code_system FK
	- code_group FK
	- budget_year FK
	- code
	- description

### Transactions
- App Name: transactions
- Models
  - transaction
	- payee_payer.demographics FK
	- transaction type
	  - payable
	  - receivable
	- memo
	- date_submitted
	- history
  - item
	- transaction FK
	- date_item
	- description
	- amount
	- gst
	- total
	- history
  - financial code
	- item FK
	- financial code FK
	- history
  - attachments
	- transaction FK
	- documents.pdf
	- history

### Investments
App Name: investments
Models
  - investment
	- date_invested
	- name
	- amount
	- rate
	- history

### Bank Transactions
App Name: bank
Models
  - institution
	- name
	- address
	- phone
	- fax
	- history
  - account
	- institution FK
	- account_number
	- name
	- history
	- status
	  - active
	  - closed
  - statement
	- account
	- date_start
	- date_end
	- history
  - transaction
	- date_transaction
	- bank_description
	- user_description
	- debit
	- credit
	- history
  - attachments
	- statement FK
	- documents.pdf
	- history
  - reconciliation
	- transactions.transaction FK
	- transaction FK
	- history
	
## Required templates and views
Home Pages
- Submit an expense
- Login
	
Dashboard Page (on login)
- Stats
- Links to other pages
- To-do list (expenses?)

User Management
- User registration - email or social auth
- Change user group/permissions
- Delete users
	
Submit Expense
- Form to enter in expenses
  - Travel exepnes (by distance) as option
- File upload (limit to images and PDF)
- Email (populate if already logged in)
- Description of expense
	
Review Expense
- Authorized users only
- View all pending expenses
- Modify as needed
- Approve and submit (or queue)
- Assign to an payee
	
Manage Payee/Payer
- Modify links to user accounts (if available)
	
Enter Expense

Enter Revenue
	
Manage Investments

Bank Transactions

## Users, Groups, and Authorizations
- Developer/Superuser
- Branch Delegate(s)
- President
  - President only one with ability to upgrade user status?
- Treasurer