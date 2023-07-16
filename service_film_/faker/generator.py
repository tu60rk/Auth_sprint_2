import uuid
import pandas as pd
import random

from tqdm import tqdm
from faker import Faker


ORDER_DIRECTION = 'uuid generate'


class GeneratorMovies:

    fake = Faker()

    def g_genres(self, count: int) -> pd.DataFrame:

        randoms_uuid = {uuid.uuid4() for _ in tqdm(range(count), desc=ORDER_DIRECTION)}
        random_name = [self.fake.word() for _ in tqdm(range(count), desc="genre generate")]
        random_description = [self.fake.text(max_nb_chars=160) for _ in tqdm(range(count), desc="description genre generate")]

        df = pd.DataFrame({
            'id': list(randoms_uuid),
            'name': random_name,
            'description': random_description,
        })
        self.genres = df
        return self.genres

    def g_persons(self, count: int) -> pd.DataFrame:

        randoms_uuid = {uuid.uuid4() for _ in tqdm(range(count), desc=ORDER_DIRECTION)}
        randoms_uuid = randoms_uuid - set(self.genres.id.tolist())

        while True:
            if len(randoms_uuid) < count:
                randoms_uuid = randoms_uuid.union({uuid.uuid4() for _ in range(count - len(randoms_uuid))})
                continue
            break

        random_name = [self.fake.name() for _ in tqdm(range(count), desc="generate names")]
        df = pd.DataFrame({
                    'id': list(randoms_uuid),
                    'name': random_name,
                })
        self.persons = df
        return df

    def g_movies(self, count: int) -> pd.DataFrame:

        randoms_uuid = {uuid.uuid4() for _ in tqdm(range(count), desc=ORDER_DIRECTION)}
        randoms_uuid = randoms_uuid - set(self.genres.id.tolist()) - set(self.persons.id.tolist())

        while True:
            if len(randoms_uuid) < count:
                randoms_uuid = randoms_uuid.union({uuid.uuid4() for _ in range(count - len(randoms_uuid))})
                continue
            break

        imdb_raiting = [round(random.uniform(0.1, 10.0), 2) for _ in tqdm(range(count), desc='raiting generate')]
        title = self.fake.sentences(nb=count)
        description = [self.fake.text(max_nb_chars=160) for _ in tqdm(range(count), desc="desc generate")]

        self.ges = {v: k for k, v in zip(self.genres.id.tolist(), self.genres.name.tolist())}
        ge = self.genres.name.tolist()
        genre = [random.choices(ge, k=random.randint(1, 5)) for _ in tqdm(range(count), desc="genre gen")]
        genres = [self.common_generate(type='genres', filter_list=g) for g in tqdm(genre, desc="genre with id gen")]

        self.pes = {v: k for k, v in zip(self.persons.id.tolist(), self.persons.name.tolist())}
        pe = self.persons.name.tolist()

        director = [random.choices(pe, k=random.randint(1, 4)) for _ in tqdm(range(count), desc='director gen')]
        directors = [self.common_generate(type='persons', filter_list=g) for g in tqdm(director, desc="directors witth id gen")]

        actors_names = [random.choices(pe, k=random.randint(1, 4)) for _ in tqdm(range(count), desc="actors gen")]
        actors = [self.common_generate(type='persons', filter_list=g) for g in tqdm(actors_names, desc="actors with id gen")]

        writers_names = [random.choices(pe, k=random.randint(1, 4)) for _ in tqdm(range(count), desc="writers gen")]
        writers = [self.common_generate(type='persons', filter_list=g) for g in tqdm(writers_names, desc="writers with id gen")]

        return pd.DataFrame({
            'id': list(randoms_uuid),
            'raiting':  imdb_raiting,
            'genre': genre,
            'title': title,
            'description': description,
            'director': director,
            'actors_names': actors_names,
            'writers_names': writers_names,
            'actors': actors,
            'writers': writers,
            'directors': directors,
            'genres': genres,
        })

    def common_generate(self, type: str, filter_list: list) -> list:
        if type == 'genres':
            return [{'id': self.ges.get(name), 'name': name} for name in filter_list]
        if type == "persons":
            return [{'id': self.pes.get(name), 'name': name} for name in filter_list]

    def generate(self, type: str, count: int):
        if type == "genres":
            return self.g_genres(count=count)
        if type == "persons":
            return self.g_persons(count=count)
        if type == "movies":
            return self.g_movies(count=count)
