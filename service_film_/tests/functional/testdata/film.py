import uuid

from http import HTTPStatus


FILM_TITLE_QUERY_POS = 'The Star'
FILM_TITLE_QUERY_NEG = 'Mashed potato'
MESSAGE_SEARCH_UUID_NEG = 'value is not a valid uuid'

ES_FILM_SEARCH_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'query': FILM_TITLE_QUERY_POS, 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.OK, 'length': 50, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'query': FILM_TITLE_QUERY_POS, 'page_number': 1, 'page_size': 2},
        {'status': HTTPStatus.OK, 'length': 2, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'query': FILM_TITLE_QUERY_POS},
        {'status': HTTPStatus.OK, 'length': 50, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'query': FILM_TITLE_QUERY_POS, 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    )
]

ES_FILM_SEARCH_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'query': FILM_TITLE_QUERY_NEG, 'page_number': -1, 'page_size': 50},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        {'query': FILM_TITLE_QUERY_NEG, 'page_size': 1000000},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_FILM_SEARCH_GEN_DATA = {
        'id': '',
        'imdb_raiting': 8.5,
        'genres': [
            {'id': uuid.UUID('0fbcd2b3-2792-4468-8885-06d653f368c8'), 'name': 'Action'},
            {'id': uuid.UUID('b29306f4-e843-4f6f-96c8-0e815a504575'), 'name': 'Sci-Fi'}
        ],
        'genre': ['Action', 'Sci-Fi'],
        'title': FILM_TITLE_QUERY_POS,
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': uuid.UUID('c0b89c7f-01ef-49aa-854f-b48676b36885'), 'name': 'Ann'},
            {'id': uuid.UUID('d5fb741d-93a9-4ced-b788-e162e8567256'), 'name': 'Bob'}
        ],
        'writers': [
            {'id': uuid.UUID('407452e9-5709-4597-acc6-e2daa3c5255d'), 'name': 'Ben'},
            {'id': uuid.UUID('93e34623-4522-41c0-83a4-a7f697671242'), 'name': 'Howard'}
        ],
        'directors': [
            {'id': uuid.UUID('93b712a6-d5ae-492e-8462-3512014cbf2c'), 'name': 'Stan'},
        ],
    }

UUIDS_FILMS = [
    uuid.UUID("0ce50db6-6c9f-4ffb-99d7-089497bc0a45"),
    uuid.UUID("20e086a5-abc1-4a42-b350-d8bfc35af07c"),
    uuid.UUID("f7dc8b7a-e741-45cb-b963-942d54e420d4"),
    uuid.UUID("43c2f553-9a41-4768-8f25-415daf289c50"),
    uuid.UUID("0e402e0f-3adf-4253-b6c7-92ad6b45d46a"),
    uuid.UUID("11f1438d-d56a-45ea-b9e5-75d2092b21e3"),
    uuid.UUID("80a23f6c-13f7-41f4-8cf1-5040b5353c9e"),
    uuid.UUID("5535b1d8-e478-458b-917a-821301a19324"),
    uuid.UUID("67908152-c207-4d81-82b9-530d219c382f"),
    uuid.UUID("80c69d35-51fb-49c6-9996-dbdfd02a2697"),
    uuid.UUID("b703aa97-94e3-4f78-aa4d-31e18bbc680b"),
    uuid.UUID("ee464f44-d9d0-4991-9c58-afbf224bd519"),
    uuid.UUID("4b72f8d1-e675-48f4-92e2-745d30e48264"),
    uuid.UUID("e6303707-b651-42b8-bfa3-649eb82e7b9c"),
    uuid.UUID("e2532632-9628-48db-9b50-d7e9523eb240"),
    uuid.UUID("d03c9f5e-7caa-4d9a-92ac-68fc6a9e7f4c"),
    uuid.UUID("227df03a-0d55-4e81-99c4-0c2b1c873872"),
    uuid.UUID("2a2f6427-bc4d-423f-b029-16c306528b3f"),
    uuid.UUID("be556c1a-9e5e-4034-ba19-563183824d66"),
    uuid.UUID("8845add4-a67d-4ae5-8517-abe366431c02"),
    uuid.UUID("610016aa-8300-4fd4-9206-63ea25ebaf9a"),
    uuid.UUID("c6e8bbb4-bb4b-434e-8971-891560659ce0"),
    uuid.UUID("56f68be5-3387-4f9d-9aea-0496d942ff1d"),
    uuid.UUID("215f633d-4cb1-448e-bb3d-1fdfb29f25a7"),
    uuid.UUID("6e183ee4-b92f-4976-a79e-69e7c67cf5c6"),
    uuid.UUID("79502ec6-196e-44fc-966b-96b4b5ae9d46"),
    uuid.UUID("9e1ce46f-a581-4951-8d27-1ee944b5eb3d"),
    uuid.UUID("6b518531-355d-4a71-a198-a840170bc82c"),
    uuid.UUID("c1965b2b-a7f2-4bd2-967a-efcb5fa0efc0"),
    uuid.UUID("58992514-bd9e-4714-93c0-a07157cd942f"),
    uuid.UUID("c7062328-78b2-4646-90f1-4edfc601e08a"),
    uuid.UUID("93014428-99e0-41ff-a162-389781a1955f"),
    uuid.UUID("6ede8e73-e9f8-4173-85a3-11e3a00716d9"),
    uuid.UUID("caad126a-c1df-4405-8954-9b7a2efdb1c4"),
    uuid.UUID("970ce4ee-6474-4ded-bcfa-736a41360679"),
    uuid.UUID("3c0812e5-c2ca-401f-aa5a-ab3d54974478"),
    uuid.UUID("a403a5cc-aa78-4dae-beba-8d96ce20ecc4"),
    uuid.UUID("ffb49725-151c-42bb-a134-10d653e8b9ee"),
    uuid.UUID("e5894d59-efcd-4eb7-be83-fd31fb4d4515"),
    uuid.UUID("cf7ed583-b02e-41dc-9d20-5b3e3a925c3e"),
    uuid.UUID("36075ccc-1d23-4575-9dcb-7027f9042f74"),
    uuid.UUID("d5be37b9-05ea-4bda-bd8a-9d0c2305f3d5"),
    uuid.UUID("085bf1b4-0721-4f5e-a12b-7f641cad26bb"),
    uuid.UUID("4379ca60-008c-4c77-bc33-746748caf890"),
    uuid.UUID("e8016d32-a65d-410f-bc19-35c89da73629"),
    uuid.UUID("b4ab7fec-2bb8-4ca1-b98b-bd8f83793a3f"),
    uuid.UUID("e7dae6b9-b913-442b-a557-6f82ca02c64c"),
    uuid.UUID("ee69eff7-c70c-4f12-870e-df1402e051b5"),
    uuid.UUID("1d094b67-ec05-4bcf-8150-24f24ee0a1aa"),
    uuid.UUID("65aced5b-590a-4a17-ab25-2b4969cf250f"),
    uuid.UUID("42b338cd-f5a6-4662-9d24-f4967b89fd9c"),
    uuid.UUID("fb7d312e-7352-4b63-8937-b59fb9d5a2d9"),
    uuid.UUID("cc31969b-297d-41fe-9469-5e8b5f929f20"),
    uuid.UUID("2e39b905-055e-447e-ac68-7b32e6aa4793"),
    uuid.UUID("502f7bd5-5b72-4565-9f7d-ed574287975e"),
    uuid.UUID("b8d1a980-885d-42d9-9bc3-b914949fbe92"),
    uuid.UUID("062c68f8-5e88-4849-b642-4c00a8252ae3"),
    uuid.UUID("01bf5993-0649-4c69-aa07-6a89ee4f6e64"),
    uuid.UUID("c5a4bf67-1ae0-40ab-a6a5-3a791debf2e1"),
    uuid.UUID("e73f9c0f-56b6-4235-9a4d-6e5d733e74e8")
]

ES_FILMS_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'genre': '0fbcd2b3-2792-4468-8885-06d653f368c8', 'sort_param': '-imdb_raiting', 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.OK, 'length': 50, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'sort_param': '-imdb_raiting', 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.OK, 'length': 50, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'sort_param': '-imdb_raiting', 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'sort_param': '-imdb_raiting', 'page_number': 0, 'page_size': 2},
        {'status': HTTPStatus.OK, 'length': 2, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    ),
    (
        {'sort_param': '-imdb_raiting', 'page_number': 0, 'page_size': 1},
        {'status': HTTPStatus.OK, 'length': 1, 'full_return': [
            {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        ]}
    )]

ES_FILMS_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'genre': '123', 'page_number': 0, 'page_size': 50},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': MESSAGE_SEARCH_UUID_NEG}
    ),
    (
        {'genre': '0fbcd2b3-2792-4468-8885-06d653f368c8', 'page_number': -1, 'page_size': 50},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        {'genre': '0fbcd2b3-2792-4468-8885-06d653f368c8', 'page_size': 1000000},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_FILM_BY_ID_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'film_id': 'c5a4bf67-1ae0-40ab-a6a5-3a791debf2e1'},
        {'status': HTTPStatus.OK, 'length': 8, 'full_return' : {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        }
    ),
    (
        {'film_id': 'e73f9c0f-56b6-4235-9a4d-6e5d733e74e8'},
        {'status': HTTPStatus.OK, 'length': 8, 'full_return' : {
                "id": "1",
                "title": FILM_TITLE_QUERY_POS,
                "imdb_raiting": 8.5
            }
        }
    )
]

ES_FILM_BY_ID_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'film_id': '123'},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': MESSAGE_SEARCH_UUID_NEG}
    ),
    (
        {'film_id': 123},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1, 'msg': MESSAGE_SEARCH_UUID_NEG}
    )
]
