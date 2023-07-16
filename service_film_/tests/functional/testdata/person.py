import uuid

from http import HTTPStatus

ES_PERSON_SEARCH_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'query': 'Ann', 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": 'c0b89c7f-01ef-49aa-854f-b48676b36885',
                "full_name": "Ann"
            }
        ]}
    ),
    (
        {'query': 'Ann', 'page_number': 0, 'page_size': 2},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": 'c0b89c7f-01ef-49aa-854f-b48676b36885',
                "full_name": "Ann"
            }
        ]}
    ),
    (
        {'query': 'Ann'},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": 'c0b89c7f-01ef-49aa-854f-b48676b36885',
                "full_name": "Ann"
            }
        ]}
    ),
    (
        {'query': 'Ann', 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": 'c0b89c7f-01ef-49aa-854f-b48676b36885',
                "full_name": "Ann"
            }
        ]}
    )
]

ES_PERSON_SEARCH_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'query': 'Musseti', 'page_number': -1, 'page_size': 50},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        {'query': 'Musseti', 'page_size': 1000000},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_PERSON_BY_ID_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'person_id': '407452e9-5709-4597-acc6-e2daa3c5255d'},
        {'status': HTTPStatus.OK, 'length': 3, 'full_return': {
            "id": "407452e9-5709-4597-acc6-e2daa3c5255d",
            "full_name": "Ben"
        }}
    ),
    (
        {'person_id': '93e34623-4522-41c0-83a4-a7f697671242'},
        {'status': HTTPStatus.OK, 'length': 3, 'full_return':  {
                "id": "93e34623-4522-41c0-83a4-a7f697671242",
                "full_name": "Howard"
            }
        }
    )
]

ES_PERSON_BY_ID_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'query': '456'},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'value is not a valid uuid'}
    ),
    (
        {'query': 456},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'value is not a valid uuid'}
    )
]

ES_FILMS_BY_PERSON_ID_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'person_id': '407452e9-5709-4597-acc6-e2daa3c5255d', 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.OK, 'length': 50, 'full_return': {
            "id": "1",
            "title": "The Star",
            "imdb_raiting": 8.5
        }}
    ),
    (
        {'person_id': '407452e9-5709-4597-acc6-e2daa3c5255d', 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': {
            "id": "1",
            "title": "The Star",
            "imdb_raiting": 8.5
        }}
    ),
    (
        {'person_id': '93e34623-4522-41c0-83a4-a7f697671242', 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return':  {
                "id": "1",
                "title": "The Star",
                "imdb_raiting": 8.5
            }
        }
    )
]

ES_FILMS_BY_PERSON_ID_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'person_id': '456'},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'value is not a valid uuid'}
    ),
    (
        {'person_id': '93e34623-4522-41c0-83a4-a7f697671242', 'page_number': -1, 'page_size': 50},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        {'person_id': '93e34623-4522-41c0-83a4-a7f697671242', 'page_size': 1000000},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_PERSON_SEARCH_GEN_DATA = [
    {
        'id': uuid.UUID('c0b89c7f-01ef-49aa-854f-b48676b36885'),
        'full_name': 'Ann',
    },
    {
        'id': uuid.UUID('d5fb741d-93a9-4ced-b788-e162e8567256'),
        'full_name': 'Bob',
    },
    {
        'id': uuid.UUID('407452e9-5709-4597-acc6-e2daa3c5255d'),
        'full_name': 'Ben',
    },
    {
        'id': uuid.UUID('93e34623-4522-41c0-83a4-a7f697671242'),
        'full_name': 'Howard',
    },
    {
        'id': uuid.UUID('93b712a6-d5ae-492e-8462-3512014cbf2c'),
        'full_name': 'Stan',
    },
]