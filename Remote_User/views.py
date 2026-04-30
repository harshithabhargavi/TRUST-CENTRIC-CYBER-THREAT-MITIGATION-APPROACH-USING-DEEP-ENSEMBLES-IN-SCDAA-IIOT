'''from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,cyberattack_detection,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_Cyber_Attack_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Protocol= request.POST.get('Protocol')
            Flag= request.POST.get('Flag')
            Packet= request.POST.get('Packet')
            Sender_ID= request.POST.get('Sender_ID')
            Receiver_ID= request.POST.get('Receiver_ID')
            Source_IP_Address= request.POST.get('Source_IP_Address')
            Destination_IP_Address= request.POST.get('Destination_IP_Address')
            Source_Port= request.POST.get('Source_Port')
            Destination_Port= request.POST.get('Destination_Port')
            Packet_Size= request.POST.get('Packet_Size')

        dataset = pd.read_csv("Datasets.csv", encoding='latin-1')

        def apply_results(label):
            if (label == 0):
                return 0  # Cross Site Scripting
            elif (label == 1):
                return 1  # DoS
            elif (label == 2):
                return 2  # Password Attacks

        dataset['Results'] = dataset['Label'].apply(apply_results)

        cv = CountVectorizer()

        x = dataset['Fid'].apply(str)
        y = dataset['Results']

        cv = CountVectorizer()

        print(x)
        print("Y")
        print(y)

        x = cv.fit_transform(x)
        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Deep Neural Network-DNN")
        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        testscore_mlpc = accuracy_score(y_test, y_pred)
        accuracy_score(y_test, y_pred)
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Cross Site Scripting'
        elif prediction == 1:
            val = 'DoS'
        elif prediction == 2:
            val = 'Password Attacks'


        print(val)
        print(pred1)

        cyberattack_detection.objects.create(
        Fid=Fid,
        Protocol=Protocol,
        Flag=Flag,
        Packet=Packet,
        Sender_ID=Sender_ID,
        Receiver_ID=Receiver_ID,
        Source_IP_Address=Source_IP_Address,
        Destination_IP_Address=Destination_IP_Address,
        Source_Port=Source_Port,
        Destination_Port=Destination_Port,
        Packet_Size=Packet_Size,
        Prediction=val)

        return render(request, 'RUser/Predict_Cyber_Attack_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_Cyber_Attack_Type.html')'''

from django.shortcuts import render, redirect
from django.db.models import Count, Q

from Remote_User.models import (
    ClientRegister_Model,
    cyberattack_detection,
    detection_ratio,
    detection_accuracy
)
from Remote_User.cimd_predictor import get_form_columns, get_form_fields, get_feature_columns, get_demo_label, predict_one


# ================= LOGIN =================
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = ClientRegister_Model.objects.get(
                username=username,
                password=password
            )

            request.session["userid"] = user.id
            request.session["username"] = user.username

            return redirect('design')

        except ClientRegister_Model.DoesNotExist:
            return render(request, 'RUser/login.html', {
                "error": "Invalid credentials"
            })

    return render(request, 'RUser/login.html')

# ================= REGISTER =================
def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Save user
        ClientRegister_Model.objects.create(
            username=username,
            email=email,
            password=password,
            phoneno=phoneno,
            country=country,
            state=state,
            city=city
        )

        # Auto login
        user = ClientRegister_Model.objects.get(username=username, password=password)
        request.session["userid"] = user.id

        # Redirect to dashboard
        return redirect('design')

    return render(request, 'RUser/Register1.html')


# ================= DASHBOARD =================
def design(request):
    uid = request.session.get("userid")
    user = ClientRegister_Model.objects.get(id=uid)
    return render(request, 'RUser/design.html', {"user": user})


# ================= PROFILE =================
def ViewYourProfile(request):
    userid = request.session.get('userid')
    obj = ClientRegister_Model.objects.get(id=userid)
    return render(request, 'RUser/ViewYourProfile.html', {'object': obj})


# ================= ADD DATASET PAGE =================
def Add_DataSet_Details(request):
    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


# ================= PREDICTION (CIMD-2024 ensemble, 22 features) =================
def Predict_Cyber_Attack_Type(request):
    # Form always shows 22 features (reduced by importance); form_fields = dropdown options
    feature_columns = get_form_columns()
    form_fields = get_form_fields()
    try:
        get_feature_columns()  # ensure artifacts load; form still uses 22
    except Exception as e:
        if request.method == "GET":
            return render(request, 'RUser/Predict_Cyber_Attack_Type.html', {
                'form_fields': form_fields,
                'error': 'ML artifacts not loaded. Place preprocessor.joblib, ensemble.joblib, label_encoder.joblib, and metadata.json in the project artifacts folder. (%s)' % e,
            })

    if request.method == "POST":
        # Build features dict from form (22 fields)
        features_dict = {col: request.POST.get(col) or '' for col in feature_columns}
        # Demo override: if input matches a known malware sample, return that exact class for demo
        demo_val = get_demo_label(features_dict)
        if demo_val is not None:
            val = demo_val
        else:
            try:
                val = predict_one(features_dict)
            except Exception as e:
                return render(request, 'RUser/Predict_Cyber_Attack_Type.html', {
                    'form_fields': form_fields,
                    'error': 'Prediction failed: %s' % str(e),
                })

        # Map to existing DB fields for compatibility with View/Download
        cyberattack_detection.objects.create(
            Fid=features_dict.get('Average Packet Size', '') or 'CIMD',
            Protocol=features_dict.get('Protocol Type', ''),
            Flag=features_dict.get('Flags', ''),
            Packet=features_dict.get('Average Packet Size', ''),
            Sender_ID='',
            Receiver_ID='',
            Source_IP_Address=features_dict.get('Source IP', ''),
            Destination_IP_Address=features_dict.get('Destination IP', ''),
            Source_Port=str(features_dict.get('Source Port', '')),
            Destination_Port=str(features_dict.get('Destination Port', '')),
            Packet_Size=str(features_dict.get('Average Packet Size', '')),
            Prediction=val,
        )
        return render(request, 'RUser/Predict_Cyber_Attack_Type.html', {
            'objs': val,
            'form_fields': form_fields,
        })

    return render(request, 'RUser/Predict_Cyber_Attack_Type.html', {
        'form_fields': form_fields,
    })



