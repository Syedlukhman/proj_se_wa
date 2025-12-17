"""
app.py
This module implements the Flask application for an online book exchange
platform. The application allows users to register, log in, create
book listings, browse available books, and communicate with other
users via simple messages. It uses Flask for routing and templating,
Flask‑Login for session management, and SQLAlchemy (via
flask_sqlalchemy) as the ORM. All data is stored in a local SQLite
database (book_exchange.db) inside the project directory.

The application is intentionally simple to serve as a starting point
for a full‑featured marketplace. It can be extended with additional
features such as image uploads, user reviews, location‑based search,
or availability tracking.

This code is self‑contained and can be run directly with
``python app.py``. On first run it creates the SQLite database and
initializes the tables. See README.md in the project root for
instructions on installing dependencies and running the application.

Note: For demonstration purposes the SECRET_KEY is hardcoded. In
production you should use an environment variable or configuration
file to load secret settings securely.
"""

import os
from datetime import datetime
from flask import (Flask, render_template, redirect, url_for, request,
                   flash, abort)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user, UserMixin)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the Flask application. The secret key is used to
# cryptographically sign session cookies and flash messages. The
# database URI points to a SQLite file located in the project
# directory. SQLALCHEMY_TRACK_MODIFICATIONS is disabled to reduce
# overhead.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fd64356cf7310b714713d43f470765c95f5f4a1d52e0c289')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_exchange.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and login manager. The db object is used to
# define models and perform queries. The login manager handles
# user session management.
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

login_manager.init_app(app)


class User(UserMixin, db.Model):
    """Model representing a registered user.

    Attributes:
        id: Primary key.
        username: Unique username chosen by the user.
        email: Unique email address.
        password_hash: Hashed password for secure storage.
        listings: Relationship to Listing objects created by the user.
        sent_messages: Relationship to Message objects sent by the user.
        received_messages: Relationship to Message objects received by the
            user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    listings = db.relationship('Listing', backref='owner', lazy=True)
    sent_messages = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='sender', lazy=True)
    received_messages = db.relationship('Message',
                                        foreign_keys='Message.receiver_id',
                                        backref='receiver', lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and store the user's password.

        Args:
            password: Plain text password provided by the user.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check whether a plain text password matches the stored hash.

        Args:
            password: Plain text password to verify.

        Returns:
            True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


class Listing(db.Model):
    """Model representing a book listing.

    Attributes:
        id: Primary key.
        title: Title of the book.
        author: Author of the book.
        genre: Genre or category of the book.
        description: Free‑form description (e.g., summary, notes).
        condition: Physical condition of the book (e.g., New, Good, Fair).
        created_at: Timestamp when the listing was created.
        owner_id: Foreign key referencing the User who created the listing.
        messages: Relationship to Message objects associated with the listing.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    condition = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref='listing', lazy=True)


class Message(db.Model):
    """Model representing a direct message between two users about a listing.

    Attributes:
        id: Primary key.
        sender_id: Foreign key referencing the User who sent the message.
        receiver_id: Foreign key referencing the User who received the message.
        listing_id: Foreign key referencing the Listing related to the message.
        content: The body of the message.
        timestamp: Timestamp when the message was sent.
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id: str):
    """Flask‑Login user loader callback.

    Given a user ID stored in the session, return the corresponding User
    object. This allows Flask‑Login to manage user sessions across
    requests.

    Args:
        user_id: The ID of the user as a string.

    Returns:
        The User instance if found, otherwise None.
    """
    return db.session.get(User, int(user_id))


# Provide the current year to all templates for the footer
@app.context_processor
def inject_current_year():
    """Inject the current year into the template context.

    Returns a dictionary with 'current_year' set to the current year. This
    allows templates to display the year dynamically in the footer.
    """
    return {'current_year': datetime.utcnow().year}


@app.route('/')
def index():
    """Render the home page with a summary of recent listings.

    The home page shows the most recent book listings to encourage
    exploration. It also serves as a landing page with links to
    register or log in. All users (authenticated or not) can access
    this page.
    """
    recent_listings = Listing.query.order_by(Listing.created_at.desc()).limit(5).all()
    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    listings_data = []
    for listing in recent_listings:
        listings_data.append({
            'id': listing.id,
            'title': listing.title,
            'author': listing.author,
            'genre': listing.genre,
            'condition': listing.condition,
            'created_at': listing.created_at.isoformat()
        })
    return render_template('index.html', listings=listings_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.

    Presents a registration form on GET. On POST, validates the
    submitted data, ensures the username and email are unique, hashes
    the password, and creates a new user. If successful, the user is
    logged in and redirected to the home page. Error messages are
    flashed for invalid input or duplicates.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Simple validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        # Check for duplicates
        if User.query.filter_by(username=username).first() is not None:
            flash('Username already taken.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first() is not None:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        # Create the user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registration successful! Welcome to the book exchange.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.

    Displays a login form on GET. On POST, verifies the provided
    credentials. If the credentials are correct, the user is logged in
    and redirected to the next page or home. If invalid, an error
    message is flashed.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully.', 'success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log the current user out and redirect to the home page."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/listings')
def listings():
    """Display all book listings with optional search and filter.

    The page supports query parameters 'q' for search keywords, 'genre'
    to filter by genre, and 'condition' to filter by book condition.
    Results are ordered by creation time, newest first.
    """
    search_query = request.args.get('q', '', type=str)
    genre_filter = request.args.get('genre', '', type=str)
    condition_filter = request.args.get('condition', '', type=str)

    query = Listing.query

    if search_query:
        like_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(Listing.title.ilike(like_pattern),
                   Listing.author.ilike(like_pattern),
                   Listing.genre.ilike(like_pattern))
        )
    if genre_filter:
        query = query.filter(Listing.genre == genre_filter)
    if condition_filter:
        query = query.filter(Listing.condition == condition_filter)

    listings = query.order_by(Listing.created_at.desc()).all()
    # Distinct values for filter dropdowns
    genres = [row.genre for row in db.session.query(Listing.genre).distinct() if row.genre]
    conditions = [row.condition for row in db.session.query(Listing.condition).distinct() if row.condition]
    return render_template('listings.html', listings=listings,
                           genres=genres, conditions=conditions,
                           search_query=search_query,
                           genre_filter=genre_filter,
                           condition_filter=condition_filter)


@app.route('/listing/<int:listing_id>', methods=['GET', 'POST'])
def listing_detail(listing_id: int):
    """Display a single listing and handle messaging.

    For GET requests, render the listing details and any existing
    messages between the current user and the listing owner. For POST
    requests, send a new message from the current user to the listing
    owner. Only authenticated users can send messages; unauthenticated
    users are redirected to the login page.
    """
    listing = Listing.query.get_or_404(listing_id)
    owner = listing.owner
    messages = None
    if current_user.is_authenticated:
        # Fetch conversation between current user and owner for this listing
        messages = (Message.query.filter_by(listing_id=listing.id)
                    .filter(db.or_(
                        db.and_(Message.sender_id == current_user.id,
                                Message.receiver_id == owner.id),
                        db.and_(Message.sender_id == owner.id,
                                Message.receiver_id == current_user.id)))
                    .order_by(Message.timestamp.asc()).all())

        # Handle new message
        if request.method == 'POST':
            content = request.form.get('content')
            if content:
                # Determine receiver: if current user is owner, receiver is buyer? For
                # simplicity, messages can only be sent from a user to the listing owner.
                receiver_id = owner.id if current_user.id != owner.id else None
                if receiver_id is None:
                    flash('You cannot message yourself about your own listing.', 'warning')
                else:
                    new_message = Message(sender_id=current_user.id,
                                          receiver_id=receiver_id,
                                          listing_id=listing.id,
                                          content=content)
                    db.session.add(new_message)
                    db.session.commit()
                    flash('Message sent.', 'success')
                    return redirect(url_for('listing_detail', listing_id=listing.id))
    else:
        # Not authenticated: show listing details but no messages
        messages = []

    return render_template('listing_detail.html', listing=listing, messages=messages)


@app.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    """Allow authenticated users to create a new book listing."""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        description = request.form.get('description')
        condition = request.form.get('condition')
        # Validate required fields
        if not title or not author:
            flash('Title and author are required.', 'danger')
            return redirect(url_for('create_listing'))
        listing = Listing(title=title, author=author, genre=genre,
                          description=description, condition=condition,
                          owner_id=current_user.id)
        db.session.add(listing)
        db.session.commit()
        flash('Listing created successfully.', 'success')
        return redirect(url_for('listings'))

    return render_template('create_listing.html')


@app.route('/my_listings')
@login_required
def my_listings():
    """Display the listings created by the current user."""
    listings = Listing.query.filter_by(owner_id=current_user.id).order_by(
        Listing.created_at.desc()).all()
    return render_template('my_listings.html', listings=listings)


@app.route('/messages')
@login_required
def messages_overview():
    """Show all conversations for the current user.

    For each conversation (unique combination of other user and listing)
    display the most recent message. The user can click through to
    continue the conversation on the listing detail page.
    """
    # Retrieve all messages involving the user
    msgs = Message.query.filter(db.or_(Message.sender_id == current_user.id,
                                       Message.receiver_id == current_user.id))
    # Group messages by listing and partner. We'll build a dict keyed by
    # (listing_id, partner_id) storing the latest message.
    conversations = {}
    for msg in msgs:
        partner_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        key = (msg.listing_id, partner_id)
        if key not in conversations or msg.timestamp > conversations[key].timestamp:
            conversations[key] = msg
    return render_template('messages.html', conversations=conversations)


@app.errorhandler(404)
def page_not_found(e):  # pragma: no cover
    """Render a custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
