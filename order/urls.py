from django.urls import path
from . import views
app_name = "order"

urlpatterns = [
          path('create/',views.order_create,name="create"),
          path('pay/<str:order_id>/',views.order_pay_by_vodafone,name="pay_form"),
          path('operation_successful/<str:order_id>/',views.pay_successful,name="payment_success"),
          path('admin/pdf/<str:order_id>',views.admin_order_pdf,name="admin_order_pdf"),
]