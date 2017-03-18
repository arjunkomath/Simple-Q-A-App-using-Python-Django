Settings
--------

Available settings:

``QA_SETTINGS`` is dictionary type set of configurations to setting up django-qa, and it comes with the next structure:

.. code-block:: python

    QA_SETTINGS = {
        'qa_messages': True,
        'qa_description_optional': False,
        'reputation': {
            'CREATE_QUESTION': 0,
            'CREATE_ANSWER': 0,
            'CREATE_ANSWER_COMMENT': 0,
            'CREATE_QUESTION_COMMENT': 0,
            'ACCEPT_ANSWER': 0,
            'UPVOTE_QUESTION': 0,
            'UPVOTE_ANSWER': 0,
            'DOWNVOTE_QUESTION': 0,
            'DOWNVOTE_ANSWER': 0,
        }
    }

The dictionary must be declared inside the project's settings file, and comes with the following keys to configure:

``qa_messages``: he default behaviour is set to ``False``, enforcing the need for a description. If set to ``True``, you will be able to create questions without descriptions.
``qa_description_optional``: This flag disables the validation applied to the 'description' field, allowing title only questions.
``reputation``: is a dictionary structure to define the different values for the concepts with access to the user reputation.

Django-QA uses `django-hitcount <https://github.com/thornomad/django-hitcount>`_ . If you want to have a custom behaviour for the hitcounts feature, feel free to use django-hitcount settings.

QA_SETTINGS = {
    'qa_messages': True,
    'qa_description_optional': False,
    'reputation': {
        'CREATE_QUESTION': 0,
        'CREATE_ANSWER': 0,
        'CREATE_ANSWER_COMMENT': 0,
        'CREATE_QUESTION_COMMENT': 0,
        'ACCEPT_ANSWER': 0,
        'UPVOTE_QUESTION': 0,
        'UPVOTE_ANSWER': 0,
        'DOWNVOTE_QUESTION': 0,
        'DOWNVOTE_ANSWER': 0,
    }
}
