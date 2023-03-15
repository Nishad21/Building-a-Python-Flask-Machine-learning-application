import pickle
from flask import Blueprint, render_template, request
import numpy as np
from flask_login import current_user

from models import db, UserDetails

predict_view = Blueprint('prediction', __name__, template_folder="templates")
model = pickle.load(open('model.pkl', 'rb'))  # loading the trained model


@predict_view.route('/prediction.enter_details')  # for entering details
def enter_details():
    return render_template('predict.html')


@predict_view.route('/prediction.predict', methods=['POST'])
def predict():
    """
    For rendering results on HTML GUI
    """
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    for k, v in zip(request.form.keys(), request.form.values()):
        if k == 'Gender':
            gender = 'male' if v == '1' else 'female'

        elif k == 'married':
            married = 'yes' if v == '1' else 'no'

        elif k == 'dependents':
            dependents = request.form['dependents']

        elif k == 'education':
            education = 'graduate' if v == '1' else 'not graduate'

        elif k == 'self_employed':
            self_employed = 'yes' if v == '1' else 'no'

        elif k == 'applicantincome':
            applicantincome = request.form['applicantincome']

        elif k == 'coapplicantincome':
            coapplicantincome = request.form['coapplicantincome']

        elif k == 'loanamount':
            loanamount = request.form['loanamount']

        elif k == 'loan_amount_term':
            loan_amount_term = request.form['loan_amount_term']

        elif k == 'credit_history':
            credit_history = 'yes' if v == '1' else 'no'

        elif k == 'property_area':
            if v == '0':
                property_area = 'rural'
            elif v == '1':
                property_area = 'urban'
            elif v == '2':
                property_area = 'semiurban'

    applicationStatus = 'Approved' if prediction[0] == 1 else 'Not Approved'

    my_user = UserDetails.query.filter_by(user_id=current_user.username).first()
    if my_user:
        print(my_user.gender)
        my_user.gender = gender
        my_user.married = married
        my_user.dependents = dependents
        my_user.education = education
        my_user.self_employed = self_employed
        my_user.applicantincome = applicantincome
        my_user.coapplicantincome = coapplicantincome
        my_user.loanamount = loanamount
        my_user.loan_amount_term = loan_amount_term
        my_user.credit_history = credit_history
        my_user.property_area = property_area
        my_user.applicationStatus = applicationStatus
        print(my_user.gender)
        db.session.commit()
    else:
        user_details = UserDetails(user_id=current_user.username, gender=gender, married=married, dependents=dependents,
                                   education=education, self_employed=self_employed, applicantincome=applicantincome,
                                   coapplicantincome=coapplicantincome, loanamount=loanamount,
                                   loan_amount_term=loan_amount_term,
                                   credit_history=credit_history, property_area=property_area,
                                   applicationStatus=applicationStatus)
        db.session.add(user_details)
        db.session.commit()

    # instance = UserDetails.query.filter(UserDetails.user_id == current_user.username)
    # # data = instance.update(dict(user_details))
    # db.session.commit()

    # class UpdateUserDetails(Resource):
    #     @auth_token_required
    #     def post(self):
    #         json_data = request.get_json()
    #         user_id = current_user.id
    #         try:
    #             instance = User.query.filter(User.id == user_id)
    #             data = instance.update(dict(json_data))
    #             db.session.commit()
    #             updateddata = instance.first()
    #             msg = {"msg": "User details updated successfully", "data": updateddata.serializers()}
    #             code = 200
    #         except Exception as e:
    #             print(e)
    #             msg = {"msg": "Failed to update the userdetails! please contact your administartor."}
    #             code = 500
    #         return msg

    if prediction == 0:
        return render_template('predict.html', prediction_text='Sorry:( you are not eligible for the loan ')
    else:
        return render_template('predict.html', prediction_text='Congrats!! you are eligible for the loan')
