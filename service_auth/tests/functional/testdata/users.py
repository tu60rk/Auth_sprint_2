from http import HTTPStatus


GETME_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2, 'full_return': {
                'email': 'testtt1234@test.com'
            }
        }
    )
]

CHANGE_PASSWORD_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'current_password': '123QWEstring',
            'new_password': '12QWEstring',
            'repeat_password': '12QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    ),
    (
        {
            'email': 'testtt1234@test.com', 'password': '12QWEstring',
            'current_password': '12QWEstring',
            'new_password': '123QWEstring',
            'repeat_password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    )
]

CHANGE_EMAIL_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com',
            'new_email': 'testtt12345@test.com',
            'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    ),
    (
        {
            'email': 'testtt12345@test.com',
            'new_email': 'testtt1234@test.com',
            'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    )
]