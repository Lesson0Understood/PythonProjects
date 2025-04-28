from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField , SubmitField , HiddenField, PasswordField
from wtforms.validators import DataRequired, Email, Length  


# ============================================== Pothole Forms ==============================================================


class CreateForm(FlaskForm):
    location = StringField("Location",validators=[DataRequired()])
    severity = TextAreaField("Severity",validators=[DataRequired()])
    image = StringField("Image",validators=[DataRequired()])
    submit = SubmitField("Create Pothole")
    
    
class UpdateForm(FlaskForm):
    location = StringField("Location",validators=[DataRequired()])
    severity = TextAreaField("Severity",validators=[DataRequired()])
    image = StringField("Image",validators=[DataRequired()])
    submit = SubmitField("Update Pothole")
    
    
    def set_default_values(self, pothole):
        self.location.data = pothole.location
        self.severity.data = pothole.severity
        self.image.data = pothole.image

        
class DeleteForm(FlaskForm):
    id = HiddenField()
    location = StringField("Location", render_kw={'readonly': True})
    severity = TextAreaField("Severity", render_kw={'readonly': True})
    image = StringField("Image", render_kw={'readonly': True})
    submit = SubmitField("Delete Pothole")


    def __init__(self, pothole,*args, **kwargs):
        self.pothole = pothole
        super(DeleteForm, self).__init__(*args, **kwargs)
        if pothole:
            self.id.data = pothole.id
            self.location.data = pothole.location
            self.severity.data = pothole.severity
            self.image.data = pothole.image


# ============================================== Authentication Forms ==============================================================

 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(LoginForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')
            
            
