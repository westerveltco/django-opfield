# django-opfield

[![PyPI](https://img.shields.io/pypi/v/django-opfield)](https://pypi.org/project/django-opfield/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-opfield)
![Django Version](https://img.shields.io/badge/django-4.2%20%7C%205.0-%2344B78B?labelColor=%23092E20)
<!-- https://shields.io/badges -->
<!-- django-4.2 | 5.0-#44B78B -->
<!-- labelColor=%23092E20 -->

A custom Django field that integrates with the 1Password `op` CLI to securely access secrets via the [`op://` secret reference URI](https://developer.1password.com/docs/cli/secret-references/).

## Requirements

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Django 4.2, 5.0
- [1Password CLI](https://developer.1password.com/docs/cli) and a [1Password Service Account](https://developer.1password.com/docs/service-accounts/)

## Getting Started

1. Install the package from PyPI:

   ```bash
   python -m pip install django-opfield
   ```

2. Install the [1Password `op` CLI tool](https://developer.1password.com/docs/cli/get-started), making sure it is callable from wherever your application is running.

3. Create a [1Password service account](https://developer.1password.com/docs/service-accounts/get-started) and make the service account's token available to your application.

   Choose one option:

   - Set the `OP_SERVICE_ACCOUNT_TOKEN` environment variable
   - Configure in your application's `settings.py`:

     ```python
     # settings.py
     DJANGO_OPFIELD = {
         # Explicitly set here only as an example
         # Use whatever configuration/environment library you prefer
         # (`python-dotenv`, `django-environs`, `environs`, etc.)
         "OP_SERVICE_ACCOUNT_TOKEN": "super-secret-token",
     }
     ```

## Usage

`OPField` allows Django models to securely access secrets stored in a 1Password vault, enabling the integration of sensitive data without exposing it directly in your codebase. Secrets are stored using the `op://` URI scheme and can be retrieved dynamically using a corresponding model attribute, `<field_name>_secret`.

### Defining a model

First, let's define a model that includes the `OPField`. This field will store the reference to the secret in 1Password, not the secret itself.

```python
from django.db import models

from django_opfield.fields import OPField


class APIService(models.Model):
    name = models.CharField(max_length=255)
    api_key = OPField()

    def __str__(self):
        return self.name
```

### Accessing the secret

Assume you have a secret API key stored in a 1Password vault named "my_vault" under the item "my_api" with the field "api_key". Here's how you can store and access this secret within your Django project:

```pycon
>>> from example.models import APIService
>>> my_api = APIService.objects.create(
...     name="My API", api_key="op://my_vault/my_api/api_key"
... )
>>> print(my_api)
<APIService: My API>
>>> print(my_api.name)
'My API'
>>> print(my_api.api_key)
'op://my_vault/my_api/api_key'
>>> # Retrieving the actual secret value is done using the automatically generated '_secret' attribute
>>> print(my_api.api_key_secret)
'your_super_secret_api_token_here'
```

### Storing references, not secrets

Only the URI reference to the secret is ever stored and exposed in the Django admin interface and the database. The actual secret itself is never stored and is only retrieved dynamically when accessed. This approach enables secure management and access to secrets throughout your Django application, safeguarding against potential security vulnerabilities associated with direct exposure.

## Documentation

Please refer to the [documentation](https://django-opfield.westervelt.dev/) for more information.

## License

`django-opfield` is licensed under the MIT license. See the [`LICENSE`](LICENSE) file for more information.
