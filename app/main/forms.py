from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    title = StringField('Comment title', validators = [Required()])
    comment = TextAreaField('Pitch comment')
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    category = SelectField('Category', choices=[('', ''), ('pickup lines', 'Pickup Lines'), ('technology', 'Technology Pitches'), ('product', 'Product Pitches'), ('innovative', 'Innovative Pitches'), ('jokes', 'Jokes')], validators = [Required()])
    title = StringField('Pitch title', validators = [Required()])
    pitch = TextAreaField('Pitch', validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us a bit about yourself.', validators = [Required()])
    submit = SubmitField('Submit')