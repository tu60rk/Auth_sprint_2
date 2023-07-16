from http import HTTPStatus


REGISTER_POSITIVE_DATA = [
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@test.com', 'password': '123QWEstring'},
        {
            'status': HTTPStatus.CREATED, 'length': 2,
            'full_return': {"email": "testtt1234@test.com"}
        }
    )
]

REGISTER_NEGATIVE_DATA = [
    (
        {
            'first_name': 'test1', 'last_name': 'test',
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'The first name must contain only alphabethical symbols'}
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test2',
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'The last name must contain only alphabethical symbols'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': '@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'value is not a valid email address'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'value is not a valid email address'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@mail.com', 'password': '123123123'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'The password must be have one upper letter'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@mail.com', 'password': 'ABCABCABC'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'The password must be have one lower letter'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@mail.com', 'password': '123ABCa'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'The password must be between 8 long'
        }
    ),
    (
        {
            'firstt_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@mail.com', 'password': '123ABCa'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'field required'
        }
    ),
    (
        {
            'first_name': 'test', 'lastt_name': 'test',
            'email': 'testtt1234@mail.com', 'password': '123ABCa'
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'field required'
        }
    ),
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@test.com', 'password': '123QWEstring'},
        {
            'status': HTTPStatus.CONFLICT,
            'msg': "User already registered"
        }
    )
]

LOGIN_POSITIVE_DATA = [
    (
        {
            'first_name': 'test', 'last_name': 'test',
            'email': 'testtt1234@test.com', 'password': '123QWEstring'},
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2
        }
    )
]

LOGIN_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt123456@test.com', 'password': '123QWEstring',
            'set_cookie': False},
        {
            'status': HTTPStatus.CONFLICT,
            'msg': 'User not found'
        }
    ),
    (
        {
            'email': 'testtt1234@test.com', 'password': '123WEstring',
            'set_cookie': False},
        {
            'status': HTTPStatus.UNAUTHORIZED,
            'msg': 'Invalid password'
        }
    ),
    (
        {
            'milo': 'testtt1234@test.com', 'password': '123WEstring',
            'set_cookie': False},
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'field required'
        }
    ),
    (
        {
            'milo': 'testtt1234@test.com', 'password': '123WEstring',
            'set_cookie': 123},
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'field required'
        }
    )
]

REFRESH_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring'},
        {
            'status': HTTPStatus.ACCEPTED, 'length': 2
        }
    )
]

REFRESH_NEGATIVE_DATA = [
    (
        {
            'not_refresh': '123',
        },
        {
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'msg': 'field required'
        }
    ),
    (
        {
            'refresh_token': '123',
        },
        {
            'status': HTTPStatus.UNAUTHORIZED,
            'msg': 'Refresh token is invalid'
        }
    )
]

LOGOUTME_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1
        }
    )
]

LOGOUTME_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.co', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNAUTHORIZED, 'msg': 'Access token is expired'
        }
    ),

]

LOGOUTALL_POSITIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.com', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.ACCEPTED, 'length': 1
        }
    )
]

LOGOUTALL_NEGATIVE_DATA = [
    (
        {
            'email': 'testtt1234@test.co', 'password': '123QWEstring'
        },
        {
            'status': HTTPStatus.UNAUTHORIZED, 'msg': 'Access token is expired'
        }
    ),

]