Settings
--------

Available settings:

``QA_DESCRIPTION_OPTIONAL`` This flag disables the validation applied to the 'description' field, allowing title only questions.
The default behaviour is set to ``False``, enforcing the need for a description. If set to ``True``, you will be able to create questions without descriptions.

Django-QA uses `django-hitcount <https://github.com/thornomad/django-hitcount>`_ . If you want to have a custom behaviour for the hitcounts feature, feel free to use django-hitcount settings.
