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

5. TypeError – 'NoneType' object is not iterable when trying to filter courses by category

    While trying to filter courses by category using the `?category=...` query string, I got a TypeError that said `'NoneType' object is not iterable` in this code:

    ```python
    categories = None 

    if request.GET: 
      if 'category' in request.GET:
        courses = courses.filter(category__name__in=categories)
    ```

* Cause:
  
  I was trying to filter using `category__name__in=categories`  but `categories` was still set to `None`. I hadn’t turned the query string into a list, so Django couldn’t loop through it and apply the filter. Also, I was passing in slugs (eg. "puppy-training") in the URL, but my category filtering was expecting exact category names (eg."Puppy Training"), which didn’t match.

* Solution:

  I added a slug field to my Category model:

  ```python
  slug = models.SlugField(unique=True, blank=True)
  ```

  I also updated the model’s save() method using slugify() to automatically create a slug from the name. Then I changed my view to get the category by its slug instead of name.

*	New Problem:

    After making these changes, I ran into a new issue when migrating: `IntegrityError: UNIQUE constraint failed: courses_category.slug`. This happened because my slug field had unique=True, but my database already had existing categories with no slug values.

* Final Fix:

  I removed unique=True temporarily:

  ```python
  slug = models.SlugField(blank=True, null=True)
  ```

  I then deleted the old mgration files from the courses/migrations folder and ran a migration again.

  Then, I	Backfilled all slugs via the Django shell:

  ```python
  from courses.models import Category
  from django.utils.text import slugify

  for category in Category.objects.all():
    category.slug = slugify(category.name)
    category.save()
  ```

  After I tested the website and everything worked I added `unique=True` to the models again, migrated and selected option 2 when prompted for how to handle NULLs.

  Filtering by category using `?category=slug` now works perfectly. The category dropdown links also function as they expected to.

  A few websites/threads that helped me find the solution: 
    * [Django Docs](https://docs.djangoproject.com/en/5.2/ref/models/fields/) 
    * a few threads on Stack Overflow:
    [Changing model field within the Django Shell](https://stackoverflow.com/questions/32899609/changing-model-field-within-the-django-shell) |
    [How to auto fill SlugField instead of overriding save()?](https://stackoverflow.com/questions/50615561/how-to-auto-fill-slugfield-instead-of-overriding-save) |
    [UNIQUE constraint failed on adding a new model field in django](https://stackoverflow.com/questions/58631272/unique-constraint-failed-on-adding-a-new-model-field-in-django)

---

6. `AssertionError` and `ImproperlyConfigured` errors when starting the server (django-allauth compatibility)

    After restarting my computer, I suddenly couldn’t run the development server anymore. Running `python manage.py runserver` threw an `AssertionError` related to `allauth.account.app_settings`, and later a `ModuleNotFoundError` for middleware that didn’t exist. This was strange because everything had worked the day before.

* Cause:
  
  I was using an older settings.py setup for django-allauth, which worked with older versions, but now I had installed newer versions, and these have more strict requirements.
  In particular, I had settings like:


  ```python
  ACCOUNT_LOGIN_METHODS = {"username", "email"}
  ```
  I also had an invalid middleware line: 


  ```python
  'allauth.account.middleware.AccountMiddleware'
  ```

* Solution:
  1.	I deleted the invalid middleware line from settings.py.
  2.	I have changed the incorrect login method setting to this: 
  ```python
  ACCOUNT_AUTHENTICATION_METHOD = "username_email"
  ```

  3.	Using windows PowerShell, I removed my broken virtual environment and rebuilt it to match the project dependencies:
  ```
  Remove-Item -Recurse -Force .venv
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
  
  After implementing all these changes, the server ran again with no errors.

  Documentation that helped me find the solution: 

  * [Allauth Quickstart](https://docs.allauth.org/en/dev/installation/quickstart.html?utm_source=chatgpt.com)

  * [Allauth Configuration](https://docs.allauth.org/en/dev/account/configuration.html?utm_source=chatgpt.com)
  
---