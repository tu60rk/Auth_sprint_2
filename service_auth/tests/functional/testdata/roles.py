from http import HTTPStatus


GETROLES_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2, 'full_return': {
                'admin': 'admin',
                'user': 'user'
            }
        }
    )
]

GETROLES_NEGATIVE_DATA = [
    (
        {},
        {
            'status': HTTPStatus.UNAUTHORIZED, 'msg': 'Access token is expired'
        }
    )
]

CREATEROLE_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test1', 'description': 'test1'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2, 'full_return': {
                'name': 'test1'
            }
        }
    )
]

CREATEROLE_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test1', 'description': 'test1'
        },
        {
            'status': HTTPStatus.BAD_REQUEST, 'msg': 'This role exists'
        }
    ),
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'nam': 'test1', 'description': 'test1'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'msg': 'field required'
        }
    )
]

CHANGEROLE_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test1', 'new_name': 'test2', 'new_description': 'test2'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    )
]

CHANGEROLE_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test1', 'new_name': 'test2', 'new_description': 'test2'
        },
        {
            'status': HTTPStatus.BAD_REQUEST, 'msg': "This role doesn't exist"
        }
    ),

]

DELETEROLE_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test2'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    )
]

DELETEROLE_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name': 'test2'
        },
        {
            'status': HTTPStatus.BAD_REQUEST, 'msg': "This role doesn't exist"
        }
    ),
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'name3': 'test2'
        },
        {
            'status': HTTPStatus.BAD_REQUEST, 'msg': "This role doesn't exist"
        }
    ),
]

SET_USER_ROLE_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'role_name': 'admin'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2, 'full_return': [
                {
                    'name': 'user',
                    'description': 'user'
                },
                {
                    'name': 'admin',
                    'description': 'admin'
                }
            ]
        }
    )
]

SET_USER_ROLE_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'role_name': 'test2'
        },
        {
            'status': HTTPStatus.BAD_REQUEST, 'msg': "Role is not exist"
        }
    )
]

DELETE_USER_ROLE_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring',
            'role_name': 'admin'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1, 'full_return': {
                'status': 'success'
            }
        }
    )
]