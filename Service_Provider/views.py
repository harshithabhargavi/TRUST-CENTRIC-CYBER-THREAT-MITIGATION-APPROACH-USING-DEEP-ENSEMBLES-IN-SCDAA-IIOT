from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlwt
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression

from Remote_User.models import (
    ClientRegister_Model,
    cyberattack_detection,
    detection_ratio,
    detection_accuracy
)


# ================= ADMIN LOGIN =================
def serviceproviderlogin(request):
    if request.method == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password == "Admin":
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')
    return render(request, 'SProvider/design1.html')


# ================= VIEW RATIO (FIXED) =================
def View_Cyber_Attack_Type_Ratio(request):
    detection_ratio.objects.all().delete()

    # CIMD-2024 labels (same as notebook output)
    attack_types = [
        'Benign',
        'Botnet',
        'Ransomware',
        'Spyware',
        'Trojan',
        'Worm',
    ]

    # ONLY VALID DATA (NO EMPTY INPUT PREDICTIONS)
    valid_data = cyberattack_detection.objects.exclude(
        Fid__isnull=True
    ).exclude(
        Fid=""
    )

    total = valid_data.count()

    for attack in attack_types:
        count = valid_data.filter(Prediction=attack).count()
        if total > 0 and count > 0:
            ratio = (count / total) * 100
            detection_ratio.objects.create(names=attack, ratio=ratio)

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Cyber_Attack_Type_Ratio.html', {'objs': obj})


# ================= VIEW USERS =================
def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})


# ================= CHARTS =================
def charts(request, chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts.html", {'form': chart1, 'chart_type': chart_type})


def charts1(request, chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts1.html", {'form': chart1, 'chart_type': chart_type})


# ================= VIEW PREDICTIONS (CIMD-2024) =================
def View_Prediction_Of_Cyber_Attack_Type(request):
    # Exclude empty/invalid entries; newest first
    obj = cyberattack_detection.objects.exclude(
        Fid__isnull=True
    ).exclude(
        Fid=""
    ).order_by('-id')

    message = request.session.pop('prediction_message', None)

    return render(
        request,
        'SProvider/View_Prediction_Of_Cyber_Attack_Type.html',
        {'list_objects': obj, 'message': message}
    )


def Clear_Prediction_Data(request):
    """Delete all prediction records so the admin panel shows only fresh results."""
    if request.method == "POST":
        count, _ = cyberattack_detection.objects.all().delete()
        request.session['prediction_message'] = 'All prediction data cleared. You will only see new results.'
    return redirect('View_Prediction_Of_Cyber_Attack_Type')


# ================= LIKE CHART =================
def likeschart(request, like_chart):
    charts = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/likeschart.html", {'form': charts, 'like_chart': like_chart})


# ================= DOWNLOAD DATA =================
def Download_Predicted_DataSets(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Predicted_Data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    obj = cyberattack_detection.objects.exclude(Fid__isnull=True).exclude(Fid="")

    row_num = 0
    for my_row in obj:
        row_num += 1
        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Protocol, font_style)
        ws.write(row_num, 2, my_row.Flag, font_style)
        ws.write(row_num, 3, my_row.Packet, font_style)
        ws.write(row_num, 4, my_row.Sender_ID, font_style)
        ws.write(row_num, 5, my_row.Receiver_ID, font_style)
        ws.write(row_num, 6, my_row.Source_IP_Address, font_style)
        ws.write(row_num, 7, my_row.Destination_IP_Address, font_style)
        ws.write(row_num, 8, my_row.Source_Port, font_style)
        ws.write(row_num, 9, my_row.Destination_Port, font_style)
        ws.write(row_num, 10, my_row.Packet_Size, font_style)
        ws.write(row_num, 11, my_row.Prediction, font_style)

    wb.save(response)
    return response


# ================= TRAIN MODEL =================
def train_model(request):
    detection_accuracy.objects.all().delete()

    dataset = pd.read_csv("Datasets.csv", encoding='latin-1')

    dataset['Results'] = dataset['Label']

    cv = CountVectorizer()
    x = dataset['Fid'].astype(str)
    y = dataset['Results']

    x = cv.fit_transform(x)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

    # DNN
    mlpc = MLPClassifier().fit(X_train, y_train)
    y_pred = mlpc.predict(X_test)
    detection_accuracy.objects.create(
        names="Deep Neural Network-DNN",
        ratio=accuracy_score(y_test, y_pred) * 100
    )

    # SVM
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    svm_pred = lin_clf.predict(X_test)
    detection_accuracy.objects.create(
        names="SVM",
        ratio=accuracy_score(y_test, svm_pred) * 100
    )

    # Logistic Regression
    reg = LogisticRegression(max_iter=1000)
    reg.fit(X_train, y_train)
    log_pred = reg.predict(X_test)
    detection_accuracy.objects.create(
        names="Logistic Regression",
        ratio=accuracy_score(y_test, log_pred) * 100
    )

    # Decision Tree
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    dt_pred = dtc.predict(X_test)
    detection_accuracy.objects.create(
        names="Decision Tree Classifier",
        ratio=accuracy_score(y_test, dt_pred) * 100
    )

    dataset.to_csv("Labled_data.csv", index=False)

    obj = detection_accuracy.objects.all()
    return render(request, 'SProvider/train_model.html', {'objs': obj})
