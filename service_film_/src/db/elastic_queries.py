FIND_ALL = {'match_all': {}}
FIND_FILMS_BY_GENRE = {
        'nested': {
            'path': 'genres',
            'query': {
                'bool': {
                    'must': [
                        {
                            'match': {
                                'genres.id': ''
                            }
                        }
                    ]
                }
            }
        }
    }
FIND_FILMS_BY_PERSON = {
    'bool': {
        'should':
            [
                {
                    'nested': {
                        'path': 'actors',
                        'query': {
                            'bool': {
                                'must': [
                                    {
                                        'match': {
                                            'actors.id': ''
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
                {
                    'nested': {
                        'path': 'writers',
                        'query': {
                            'bool': {
                                'must': [
                                    {
                                        'match': {
                                            'writers.id': ''
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
                {
                    'nested': {
                        'path': 'directors',
                        'query': {
                            'bool': {
                                'must': [
                                    {
                                        'match': {
                                            'directors.id': ''
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
    }
}

FIND_FILMS_BY_QUERY = {
     'multi_match': {
       'query': '',
       'fields': [
         'title',
         'description',
         'director',
         'actors_names',
         'writers_names'
       ]
     }
}

FIND_PERSONS_BY_QUERY = {
"multi_match" : {
        "query": "",
        "fields" : ["full_name", "full_name.raw"],
        "operator": "or"
    }
}


FIND_FILMS_BY_PERSONS = {
    "bool" : {
        "should" : [
            {
                "nested": {
                    "path": "actors",
                    "query": {
                        "terms": {
                            "actors.id": ""
                        }
                    }
                }
            },
            {
                "nested": {
                    "path": "writers",
                    "query": {
                        "terms": {
                            "writers.id": ""
                        }
                    }
                }
            },
            {
                "nested": {
                    "path": "directors",
                    "query": {
                        "terms": {
                            "directors.id": ""
                        }
                    }
                }
            }
        ]
    }
}
