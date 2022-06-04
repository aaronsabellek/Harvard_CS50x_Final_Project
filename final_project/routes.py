from flask import flash, redirect, render_template, url_for, abort, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from final_project import app, db
from final_project.forms import LoginForm, RegisterForm, UpdateAccountForm, PostForm, ContactForm, EmptyForm, RequestResetForm, ResetPasswordForm
from final_project.helpers import confirm_token, generate_confirmation_token, save_picture, send_email
from final_project.models import User, Post


# Display index site with all posts related to current user
@app.route("/")
@login_required
def index():

    # Get posts of current user and the ones he follows and paginate them
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page=page, per_page=10)
    
    return render_template("index.html", posts=posts)

# Update profile
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Save new picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Update new user info in db
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.info = form.info.data
        db.session.commit()
        flash("Profile has been updated successfully!", "success")
        return redirect(url_for('account'))

    # Display current user info from db
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.info.data = current_user.info

    # Get name of image file
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", form=form, image_file=image_file)

# Confirm registration via token in mail
@app.route("/confirm_email/<token>")
def confirm_email(token):

    # Try to confirm token
    try:
        email = confirm_token(token)
    except:
        flash("Confirmation link is not valid", "danger")

    # Get user who confirmed the mail
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login.", "info")
    else:
        # Update confirmation in db
        user.confirmed = True
        db.session.add(user)
        db.session.commit()

        # Login user
        login_user(user)
        flash("Confirmed Account successfully!", "success")
    return redirect(url_for('index'))

# Contact other user
@app.route("/contact/<int:post_id>", methods=["GET", "POST"])
def contact(post_id):
    form = ContactForm()

    # Get data of post
    post = Post.query.get_or_404(post_id)
    username = post.author.username
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        # Get data for email
        #user = User.query.filter_by(username=username).first()
        email = user.email

        # Create email
        subject = "{} responded to your post '{}'!".format(current_user.username, post.title)
        html = render_template("message.html", sender_name=current_user.username, sender_address=current_user.email, subject=subject, message=form.message.data)
        
        # Send email
        send_email(email, subject, html)
        flash("Your message has been sent!", "info")
        return redirect(url_for("index"))

    # Fill data for recipient and subject of mail
    form.recipient.data = username
    form.post.data = post.title

    return render_template("contact.html", form=form, user=user, legend="Contact")

# Login user
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if username exists in db
        user = User.query.filter_by(username=form.username.data).first()
        if user:

            # Check if password matches the username in db
            if check_password_hash(user.password, form.password.data):

                # Login user
                login_user(user, remember=form.remember.data)
                flash("Login successfull!", "success")
                return redirect("/")

        flash("Invalid username or password", "warning")
        return redirect("/login")

    return render_template("login.html", form=form, legend="Login")

# Logout user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successfull!", "success")
    return redirect("/login")

# Create new post
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        # Add post to db
        post = Post(title=form.title.data, content=form.content.data, task=form.task.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('index'))

    return render_template("create_post.html", form=form, legend="New Post")

# Delete post
@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)

    # Check if current user is author of the post
    if post.author != current_user:
        abort(403)

    # Delete post
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for('index'))

# Update post
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    # Get post by id
    post = Post.query.get_or_404(post_id)

    # Check if current user is author of the post
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        # Update data from form in db
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('index'))

    # Display current content of post
    form.title.data = post.title
    form.content.data = post.content

    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

# Register new user
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        
        # Get email and pw from form
        email = form.email.data
        password = form.password.data

        # Check pw for digit
        if not any(i.isdigit() for i in password):
            flash("Password must contain at least one number", "warning")
            return redirect("/register")

        # Check pw for letter
        elif not any(i.isalpha() for i in password):
            flash("Password must contain at least one letter", "warning")
            return redirect("/register")

        # Check pw for special character
        elif not any(not i.isalnum() for i in password):
            flash("Password must contain at least one special character", "warning")
            return redirect("/register")
        
        # Hash pw
        hashed_password = generate_password_hash(form.password.data, method="sha256")

        # Add user to db
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, confirmed=False)
        db.session.add(new_user)
        db.session.commit()

        # Create token and send confirmation mail
        token = generate_confirmation_token(email)
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template("activate.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html)

        flash("A confirmation email has been sent via email", "info")
        return redirect(url_for("login"))
    
    return render_template("register.html", form=form, legend="Register")

# Update password with confirmation token
@app.route("/reset_request/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Confirm token
    try:
        email = confirm_token(token)
    except:
        flash("Confirmation Link is not valid", "danger")

    # Get user by email
    user = User.query.filter_by(email=email).first_or_404()
    if user is None:
        flash('Token is invalid or expired', "danger")
        return redirect(url_for('reset_request'))

    # Display reset form
    form = ResetPasswordForm()

    if form.validate_on_submit():

        # Get new pw
        password = form.password.data

        # Check pw for digit
        if not any(i.isdigit() for i in password):
            flash("Password must contain at least one number", "warning")
            return redirect("/register")

        # Check pw for letter
        elif not any(i.isalpha() for i in password):
            flash("Password must contain at least one letter", "warning")
            return redirect("/register")

        # Check pw for special character
        elif not any(not i.isalnum() for i in password):
            flash("Password must contain at least one special character", "warning")
            return redirect("/register")

        # Hash password
        hashed_password = generate_password_hash(form.password.data, method="sha256")

        # Add hashed password to db
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated', "success")
        return redirect(url_for('login'))

    return render_template('reset_token.html', form=form, legend="Reset password")

# Search user by username
@app.route("/search")
def search():
    users = db.engine.execute("SELECT * FROM user WHERE username LIKE ?", "%" + request.args.get("q") + "%")
    return render_template("search.html", users=users)

# Display certain user and related posts and users
@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    # All posts related to user
    posts = user.followed_posts().paginate(page=page, per_page=5)

    # Only posts from the user
    own = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc())

    # All users the user follows
    followed = user.followed

    # All users who follow the user
    follower_raw = db.engine.execute("SELECT follower_id FROM followers WHERE followed_id = ?", user.id)
    follower_id = [x[0] for x in follower_raw]
    follower = [User.query.filter_by(id=x).first() for x in follower_id]

    return render_template('user.html', user=user, form=form, posts=posts, own=own, followed=followed, follower=follower)

# Follow certain user
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        # Check if user exists in db
        if user is None:
            flash('User {} not found.'.format(username), "warning")
            return redirect(url_for('index'))

        # Check if user is current user
        if user == current_user:
            flash('You cannot follow yourself!', "warning")
            return redirect(url_for('user', username=username))

        # Follow user
        current_user.follow(user)
        db.session.commit()

        # Create post with info about the new follower
        post = Post(title='{} is following {} now!'.format(current_user.username, user.username), task='Info', author=user, content='')
        db.session.add(post)
        db.session.commit()

        flash('You are following {}!'.format(username), "success")
        return redirect(url_for('user', username=username))

    else:
        return redirect(url_for('index'))

# Unfollow certain user
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        # Check if user exists in db
        if user is None:
            flash('User {} not found.'.format(username), "warning")
            return redirect(url_for('index'))

        # Check if user is current user
        if user == current_user:
            flash('You cannot unfollow yourself!', "warning")
            return redirect(url_for('user', username=username))

        # Unfollow user
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username), "success")
        return redirect(url_for('user', username=username))

    return redirect(url_for('index'))

# Request password reset
@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():

    # Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RequestResetForm()

    if form.validate_on_submit():

        # Get data from form
        email = form.email.data
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists
        if user:

            # Generate confirmation token
            token = generate_confirmation_token(email)
            confirm_url = url_for("reset_token", token=token, _external=True)

            # Generate and send confirmation email
            html = render_template("reset.html", confirm_url=confirm_url)
            subject = "Please confirm email"
            send_email(email, subject, html)
            
            flash('A confirmation email has been sent via email', "info")
            return redirect(url_for('login'))

        flash('No user with that email', "warning")
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form, legend="Reset Password")