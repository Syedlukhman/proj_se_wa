# Online Book Exchange Platform

This project is a fully functional prototype of an online book exchange
platform. It enables users to give away, trade or sell second‑hand
books within their local area. The goal is to make books more
accessible and affordable while promoting sustainability through
reuse.

## Features

- **User accounts** — New users can register with a unique username
  and email address. Passwords are hashed for secure storage. Users
  can log in, log out and manage their own listings.
- **Book listings** — Authenticated users can create listings with
  details such as title, author, genre, condition and a description.
  Listings are stored in a SQLite database and displayed on the home
  page and the browse page. Users can view listings posted by others,
  search by keywords, and filter by genre or condition.
- **Messaging** — Logged‑in users can send and receive messages about
  a listing. When viewing a listing, a conversation thread shows
  messages exchanged with the listing owner. A messages overview page
  summarizes the user’s conversations.
- **Responsive interface** — The frontend uses plain HTML, CSS and
  JavaScript for a clean and responsive user interface. Flash
  messages provide feedback on user actions.

## Technology Stack

The application is built with the following technologies:

- **Flask** — A lightweight Python web framework. Flask makes it easy
  to get started quickly while scaling to more complex applications【55412751326710†L104-L116】. It uses the
  WSGI toolkit and Jinja2 templating engine.
- **Flask‑Login** — Handles user session management, keeping
  authentication logic simple.
- **Flask‑SQLAlchemy** — Simplifies using SQLAlchemy by creating and
  managing database connections automatically【199716148332979†L11-L26】. It exposes a powerful ORM to
  define models and perform queries. The database is stored in a
  local SQLite file (`book_exchange.db`).
- **HTML, CSS, JavaScript** — The core frontend technologies. HTML
  provides the structure of each page, CSS adds styling and layout,
  and JavaScript adds minor interactivity. These technologies are the
  foundational building blocks of web development【614934937278948†L39-L68】【614934937278948†L95-L117】.

## Running the Application

1. **Install dependencies**. Ensure you have Python 3.8+ installed.
   Install the required packages using pip:

   ```bash
   pip install flask flask-login flask-sqlalchemy
   ```

2. **Run the server**. From the `book_exchange_platform` directory,
   start the development server:

   ```bash
   python app.py
   ```

   The application will create the SQLite database on first run and
   serve at `http://127.0.0.1:5000/`. You can then open this URL in
   your web browser to access the platform.

3. **Create an account**. Register a new user and begin posting
   listings, browsing existing books, and sending messages.

## Dockerization

To run the application in a Docker container, follow these steps:

1. **Build the Docker image**. From the `book_exchange_platform`
   directory, build the Docker image:

   ```bash
   docker compose up --build
   ```

2. **Run the Docker container**. Start the container and map port 5000
   to your host machine:

   ```bash
   docker compose up -d
   ```

   The application will be accessible at `http://localhost:5000/`

## Extending the Platform

This prototype is intentionally simple. You can extend it by adding
features such as:

- Image uploads for book covers or user profiles.
- Location‑based search and map integration.
- User ratings and reviews to establish trust in the community.
- Email notifications when a new message is received.
- Transaction tracking (e.g., marking books as reserved or sold).

## References

This project draws on public documentation and tutorials about the
underlying technologies:

- Flask is a lightweight and flexible web framework designed to make
  getting started with web development quick and easy while being
  powerful enough for complex applications【55412751326710†L104-L116】.
- The Flask‑SQLAlchemy extension simplifies database setup and
  management; it automatically creates and manages the SQLAlchemy
  objects and connects to a SQLite database via the
  `SQLALCHEMY_DATABASE_URI` configuration key【199716148332979†L11-L26】【199716148332979†L67-L82】.
- HTML, CSS and JavaScript are the core technologies of the web. HTML
  provides the semantic structure of a page, CSS controls the
  presentation and layout, and JavaScript adds interactivity【614934937278948†L39-L68】【614934937278948†L95-L117】. These
  languages form the basis of any web development project【614934937278948†L122-L125】.

We hope this prototype serves as a solid foundation for building a
community‑driven book exchange platform.
