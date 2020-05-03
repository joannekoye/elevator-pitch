from flask import render_template, request, redirect, url_for, abort
from app import app
from .models import Comment
from .forms import CommentForm

@app.route('/')
def index():
    '''
    returns index and data
    '''
    title = 'Home - Elevator Pitch'
    return render_template('index.html', title = title)


@app.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).order_by(Pitch.posted.desc())

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, pitches = pitches)

@app.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form,user=user)

@app.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('app.profile',uname=uname))

@app.route('/user/<uname>/pitch',methods= ['GET','POST'])
@login_required
def new_pitch(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = PitchForm()
    pitch = Pitch()

    if form.validate_on_submit():
        pitch.category = form.category.data
        pitch.title = form.title.data
        pitch.pitch_statement = form.pitch.data
        pitch.likes = 0
        pitch.dislikes = 0
        pitch.user_id = current_user.id

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('new_pitch.html',uname=uname, user = user, PitchForm = form)

@app.route('/pitches/<category>')
def pitches(category):
    pitches = Pitch.query.filter_by(category = category).order_by(Pitch.posted.desc())

    return render_template("pitches.html", pitches = pitches, category = category)

@app.route('/reviews/<pitch_id>')
@login_required
def reviews(pitch_id):
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    reviews = Review.query.filter_by(pitch_id = pitch.id).order_by(Review.posted.desc())

    return render_template('reviews.html', pitch = pitch, reviews = reviews)

@app.route('/reviews/<pitch_id>/like')
@login_required
def like(pitch_id):
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    reviews = Review.query.filter_by(pitch_id = pitch.id).order_by(Review.posted.desc())
    like = pitch.like()

    return render_template('reviews.html', pitch = pitch, reviews = reviews, like = like)

@app.route('/reviews/<pitch_id>/dislike')
@login_required
def dislike(pitch_id):
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    reviews = Review.query.filter_by(pitch_id = pitch.id).order_by(Review.posted.desc())
    dislike = pitch.dislike()

    return render_template('reviews.html', pitch = pitch, reviews = reviews, dislike =dislike)



@app.route('/pitch/comment/new/<pitch_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    comment = Comment()

    if form.validate_on_submit():
        comment.pitch_comment_title = form.title.data
        comment.pitch_comment = form.comment.data
        comment.pitch_id = pitch_id
        comment.user_id = current_user.id

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('comments', pitch_id=pitch.id ))

    return render_template('new_comment.html', comment_form = form)