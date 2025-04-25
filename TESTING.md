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

1. Git Push Rejected – Remote Contains Work That You Do Not Have Locally

When attempting to push the initial project commit to GitHub,  the following error occurred:

`failed to push some refs to 'https://github.com/Keszi94/pawgress.git'`

`Updates were rejected because the remote contains work that you do not have locally.error: failed to push some refs to 'https://github.com/Keszi94/pawgress.git'`

* Cause:

This happened because I had created a GitHub repository first (without cloning it), then committed the files locally, including the README.md. Both the remote and local repositories had separate commit histories, so Git couldn't automatically merge them.

* Solution:

To resolve the issue, I used the following command to allow unrelated histories to merge:

`git pull origin main --allow-unrelated-histories`

This successfully merged the remote and local histories and I was able to push my code as expected.

[Solution found on this page](https://stackoverflow.com/questions/37937984/git-refusing-to-merge-unrelated-histories-on-rebase)

---

2. ImproperlyConfigured – Missing AccountMiddleware in MIDDLEWARE

When running the initial database migration after installing django-allauth, the following error occurred:

`django.core.exceptions.ImproperlyConfigured: allauth.account.middleware.AccountMiddleware must be added to settings.MIDDLEWARE`

* Cause:

I was unaware that the recent version of Django AllAuth requires AccountMiddleware to be included in the MIDDLEWARE list in settings.py. 

* Solution:

To resolve the isuue, I added the following line to the MIDDLEWARE list in settings.py:

`'allauth.account.middleware.AccountMiddleware',`

After this I ran the `python manage.py migrate`command and it worked as expected.

[Solution found on this page](https://stackoverflow.com/questions/77012106/django-allauth-modulenotfounderror-no-module-named-allauth-account-middlewar?utm_source=chatgpt.com)

---

3. DeserializationError – Category ForeignKey in fixture requires integer, not string

* Cause:

While trying to run `python manage.py loaddata courses`, a ValidationError was raised because the category values were provided as strings ("Puppy Training"), rather than integer primary keys that are expected by Django's ForeignKey.

* Solution:

I have created a separate categories.json fixture, where I assigned each category it's own integer primary key. I than ran:

`python manage.py loaddata categories`
`python manage.py loaddata courses`

After this, all course data was successfully imported into the database.

Solution found on these pages: [reddit](https://www.reddit.com/r/django/comments/10zift2/help_me_understand_how_to_load_data_into_the/), [Dev.to](https://dev.to/documendous/using-django-fixtures-with-foreign-keys-without-hardcoded-ids-1pa0)

---

4. Images in Admin Panel Show 404 Error (/media/media/...)

When clicking on images linked to courses on the Admin page, the following error displayed: "Page Not Found (404)".

* Cause:

I have incorrectly set the ImageField in the Course model to `upload_to='media/'`,  which caused Django to create duplicate paths (media/media/). After I updated that Course model, the error still displayed. That’s when I realised that I have also included `”media/` at the start of the “image” paths (`"media/puppy_leash.jpg"`) in the course.json file, which led to the same issue.

* 	Solution:

First, I have updated the Course model so that the ImageField doesn't add an extra "media/": `image = models.ImageField(upload_to='', blank=True, null=True)`. 
After that I’ve removed all “media/” prefixes from the “image” fields in courses.json and then re-ran `python manage.py loaddata categories` and `python manage.py loaddata courses`.

---
