from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[])
    caption = StringField('Caption', validators=[])
    submit = SubmitField()