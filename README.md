# RapidAPI: A FastAPI Learning Project

Welcome to **RapidAPI** – a small project built with **FastAPI** as a way to learn and experiment with modern backend development.

## Tech Stack

- **FastAPI** (0.111.0) – High-performance, async web framework
- **SQLAlchemy** (2.0.29) – ORM for database management
- **Pydantic** (2.7.1) – Data validation and settings management
- **bcrypt** & **PyJWT** – Secure authentication & encryption
- **dotenv** – Environment configuration

## Features

- JWT-based authentication
- Database integration with SQLAlchemy
- Secure password hashing with bcrypt
- Environment variable management
- FastAPI-powered RESTful API

## Setup & Run

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/rapidapi.git
   cd rapidapi
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Run the FastAPI server:

   ```bash
   poetry run uvicorn main:app --reload
   ```

4. Open your browser and test the API at:

   ```
   http://127.0.0.1:8000/docs
   ```

## Why FastAPI?

- Asynchronous & Fast
- Auto-generated OpenAPI & Swagger UI
- Type safety with Pydantic
- Great for learning and building modern backends

---

### Connect with me on [LinkedIn](https://www.linkedin.com/in/yourprofile)!

Built as a learning project with FastAPI & Python.
