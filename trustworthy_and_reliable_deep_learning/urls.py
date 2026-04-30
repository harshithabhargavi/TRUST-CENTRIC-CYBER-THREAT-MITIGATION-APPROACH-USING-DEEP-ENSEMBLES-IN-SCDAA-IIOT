'''from django.contrib import admin
from django.urls import path, re_path
from Remote_User import views as remoteuser
from Service_Provider import views as serviceprovider
from trustworthy_and_reliable_deep_learning import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', remoteuser.login, name="login"),
    path('Register1/', remoteuser.Register1, name="Register1"),
    path('Predict_Cyber_Attack_Type/', remoteuser.Predict_Cyber_Attack_Type, name="Predict_Cyber_Attack_Type"),
    path('ViewYourProfile/', remoteuser.ViewYourProfile, name="ViewYourProfile"),

    path('serviceproviderlogin/', serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/', serviceprovider.View_Remote_Users, name="View_Remote_Users"),

    re_path(r'^charts/(?P<chart_type>\w+)/$', serviceprovider.charts, name="charts"),
    re_path(r'^charts1/(?P<chart_type>\w+)/$', serviceprovider.charts1, name="charts1"),
    re_path(r'^likeschart/(?P<like_chart>\w+)/$', serviceprovider.likeschart, name="likeschart"),

    path('View_Cyber_Attack_Type_Ratio/', serviceprovider.View_Cyber_Attack_Type_Ratio, name="View_Cyber_Attack_Type_Ratio"),
    path('train_model/', serviceprovider.train_model, name="train_model"),
    path('View_Prediction_Of_Cyber_Attack_Type/', serviceprovider.View_Prediction_Of_Cyber_Attack_Type, name="View_Prediction_Of_Cyber_Attack_Type"),
    path('Download_Predicted_DataSets/', serviceprovider.Download_Predicted_DataSets, name="Download_Predicted_DataSets"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''

from django.contrib import admin
from django.urls import path, re_path
from Remote_User import views as remoteuser
from Service_Provider import views as serviceprovider
from trustworthy_and_reliable_deep_learning import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # =========================
    # REMOTE USER ROUTES
    # =========================
    path('', remoteuser.login, name="login"),
    path('Register1/', remoteuser.Register1, name="Register1"),
    path('ViewYourProfile/', remoteuser.ViewYourProfile, name="ViewYourProfile"),
    path('Predict_Cyber_Attack_Type/', remoteuser.Predict_Cyber_Attack_Type, name="Predict_Cyber_Attack_Type"),

    # ✅ ADD THIS (FIXES ERROR)
    path('design/', remoteuser.design, name="design"),

    # =========================
    # SERVICE PROVIDER ROUTES
    # =========================
    path('serviceproviderlogin/', serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/', serviceprovider.View_Remote_Users, name="View_Remote_Users"),

    re_path(r'^charts/(?P<chart_type>\w+)/$', serviceprovider.charts, name="charts"),
    re_path(r'^charts1/(?P<chart_type>\w+)/$', serviceprovider.charts1, name="charts1"),
    re_path(r'^likeschart/(?P<like_chart>\w+)/$', serviceprovider.likeschart, name="likeschart"),

    path('View_Cyber_Attack_Type_Ratio/', serviceprovider.View_Cyber_Attack_Type_Ratio, name="View_Cyber_Attack_Type_Ratio"),
    path('train_model/', serviceprovider.train_model, name="train_model"),
    path('View_Prediction_Of_Cyber_Attack_Type/', serviceprovider.View_Prediction_Of_Cyber_Attack_Type, name="View_Prediction_Of_Cyber_Attack_Type"),
    path('Clear_Prediction_Data/', serviceprovider.Clear_Prediction_Data, name="Clear_Prediction_Data"),
    path('Download_Predicted_DataSets/', serviceprovider.Download_Predicted_DataSets, name="Download_Predicted_DataSets"),
]

# Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

