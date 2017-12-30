# treasurer_tools
A Django-based system to assist Non-Profit Organization treasurers in managing/tracking finances

## Testing Design
### Models
- Test that labels display as intended
- Test that model restrictions work as intended (e.g. max_lengths)
- Test that __str__ functions output desired content
- Test any custom functions

### Forms
- Test any custom functions

### Views
- dashboards/index pages
  - Test user authentication
  - Test user permission
  - Test that URL matches desired naming scheme
  - Test that URL name reverse lookup works
  - Test that included templates are correct
  - Test any custom functions
- forms that modify database contents
  - Test user authentication
  - Test user permission
  - Test that URL matches desired naming scheme
  - Test that URL name reverse lookup works
  - Test that included templates are correct
  - Test that submission redirect to proper page
  - Test that submission does what is intended (add, edit, or delete)
  - Test that invalid IDs have appropriate error handling
  - Test that invalid data types have appropriate error handling
  - Test any custom functions
  - Test that above also applies to any formsets

## Planning and Outlines
### Packages to Install
django-simple-history
django-allauth

## Users, Groups, and Authorizations
- Developer/Superuser
- Branch Delegate(s)
- President
  - President only one with ability to upgrade user status?
- Treasurer