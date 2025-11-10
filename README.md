# AniXapi
An anime platform RESTful API

## Tech Stack
- **FastAPI**
- **MySQL**
- **SQLalchemy**
- **JWT**
- **argon2**
- **pydantic**

---

## Installation
1. **Clone the Repository**
```
git clone https://github.com/OmarSenpai/AniXapi
```

2. **Navigate to the project root**
```
cd AniXapi
```

3. **Create & activate a virtual environment**
```
python -m venv .venv
or
uv venv

source .venv/bin/activate
```

4. **Install required dependencies (python 3.13+)**
```
pip install requirements.txt
or
uv pip install -r pyproject.toml
```

5. **Setting up environment variables**
```dotenv
JWT_SECRET=YOUR JWT SECRET HERE
DB_URL=YOUR DATABASE URL
PORT=YOUR PORT

ALGORITHM=ENCODING ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=YOUR PREFERRED TOKEN DURATION
```

## Project Structure

```bash
   tree -A
```

## Schemas Explained
1 - **USER SCHEMA** <br>
This schema defines a model called "User" with various fields and their associated attributes.

- `user_uuid`: A binary field that serves as the primary key for identifying users.
- `username`: A string field for the user's display name.
- `email`: A string field for the user's email address, marked as unique.
- `password`: A string field for the user's hashed password.
- `created_at`: A datetime field for the date and time the user account was created.
- `role`: An enum field representing the user's role on the platform, such as 'user' or 'admin'.
- `ratings`: A relation to the "Ratings" model, representing the ratings given by the user.
- `reviews`: A relation to the "Reviews" model, representing the reviews written by the user.
- `favorites`: A relation to the "Favorites" model, representing the anime titles the user has favorited.

This schema outlines the structure and relationships of a user entity within a database, including various attributes and associations commonly found in user management systems.

---

2 - **ANIME SCHEMA** <br>
This schema defines a model called "Anime" with various fields and their associated attributes.

- `anime_uuid`: A binary field that serves as the primary key for identifying anime titles.
- `name`: A string field representing the main title of the anime.
- `jp_name`: A string field representing the Japanese title of the anime.
- `episodes`: An integer field representing the total number of episodes in the series.
- `format`: An enum field for the type of anime, such as 'TV' or 'Movie'.
- `start_date`: A date field for the release start date.
- `end_date`: A date field for the release end date.
- `studio`: A string field representing the studio that produced the anime.
- `ratings`: A relation to the "Ratings" model, representing the ratings received by the anime.
- `reviews`: A relation to the "Reviews" model, representing the reviews written about the anime.
- `favorites`: A relation to the "Favorites" model, representing the users who have favorited the anime.

---

3 - **STUDIO SCHEMA** <br>
This schema defines a model called "Studio" with various fields and their associated attributes.

- `studio_uuid`: A binary field that serves as the primary key for identifying anime studios.
- `name`: A string field for the name of the studio.
- `anime`: A relation to the "Anime" model, representing the anime titles produced by this studio.

---

4 - **RATINGS SCHEMA** <br>
This schema defines a model called "Ratings" with various fields and their associated attributes.

- `rating_uuid`: A binary field that serves as the primary key for identifying individual ratings.
- `user`: A binary field representing the user ID associated with the rating.
- `anime`: A binary field representing the anime ID associated with the rating.

---

5 - **REVIEWS SCHEMA** <br>
This schema defines a model called "Reviews" with various fields and their associated attributes.

- `rev_uuid`: A binary field that serves as the primary key for identifying individual reviews.
- `user`: A binary field representing the user ID associated with the review.
- `anime`: A binary field representing the anime ID associated with the review.

---

6 - **FAVORITES SCHEMA** <br>
This schema defines a model called "Favorites" with various fields and their associated attributes.

- `user`: A binary field representing the user ID who added the favorite.
- `anime`: A binary field representing the anime ID that was favorited.
- `user_anime_pk`: A composite primary key on user and anime to ensure uniqueness.

