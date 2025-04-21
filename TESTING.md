# Testing - Pawgress

## Contents

  - [Automated Testing](#automated-testing)
  - [Manual Testing](#manual-testing)
    - [Navigation](#navigation)
    - [Responsiveness](#responsiveness)
    - [Authentication](#authentication)
    - [CRUD Functionality](#crud-functionality)
  - [Validator Testing](#validator-testing)
    - [PEP8](#pep8)
    - [W3C](#w3c)
    - [JSHint](#jshint)
  - [Accessibility \& Performance](#accessibility--performance)
    - [WAVE](#wave)
    - [Lighthouse](#lighthouse)
  - [Bugs \& Bug Fixes](#bugs--bug-fixes)


## Automated Testing


## Manual Testing

### Navigation
### Responsiveness
### Authentication
### CRUD Functionality 


## Validator Testing

### PEP8
### W3C
### JSHint


## Accessibility & Performance

### WAVE
### Lighthouse


## Bugs & Bug Fixes

**1. Git Push Rejected – Remote Contains Work That You Do Not Have Locally**

When attempting to push the initial project commit to GitHub,  the following error occurred:

`failed to push some refs to 'https://github.com/Keszi94/pawgress.git'`

`Updates were rejected because the remote contains work that you do not have locally.error: failed to push some refs to 'https://github.com/Keszi94/pawgress.git'`

**Cause:**

This happened because I had created a GitHub repository first (without cloning it), then committed the files locally, including the README.md. Both the remote and local repositories had separate commit histories, so Git couldn't automatically merge them.

**Solution:**

To resolve the issue, I used the following command to allow unrelated histories to merge:

`git pull origin main --allow-unrelated-histories`

This successfully merged the remote and local histories and I was able to push my code as expected.

[Solution found on this page](https://stackoverflow.com/questions/37937984/git-refusing-to-merge-unrelated-histories-on-rebase)

---

**2. ImproperlyConfigured – Missing AccountMiddleware in MIDDLEWARE**

When running the initial database migration after installing django-allauth, the following error occurred:

`django.core.exceptions.ImproperlyConfigured: allauth.account.middleware.AccountMiddleware must be added to settings.MIDDLEWARE`

**Cause:**

I was unaware that the recent version of Django AllAuth requires AccountMiddleware to be included in the MIDDLEWARE list in settings.py. 

**Solution:**

To resolve the isuue, I added the following line to the MIDDLEWARE list in settings.py:

`'allauth.account.middleware.AccountMiddleware',`

After this I ran the `python manage.py migrate`command and it worked as expected.

[Solution found on this page](https://stackoverflow.com/questions/77012106/django-allauth-modulenotfounderror-no-module-named-allauth-account-middlewar?utm_source=chatgpt.com)

---
