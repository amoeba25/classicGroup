from django.urls import path

from . import views

urlpatterns = [
    # Planning Urls
    path('planning/', views.salesPlanning, name="salesPlanning"),
    path('planning-add/', views.salesPlanningAdd, name="salesPlanningAdd"),
    path('planning-delete/<str:pk>/', views.salesPlanningDelete, name="salesPlanningDelete"),
    path('planning-Update/<str:pk>/', views.salesPlanningUpdate, name="salesPlanningUpdate"),
    path('planning-pdf/<str:pk>/', views.salesPlanningPDF, name="salesPlanningPDF"),

    # Branch and Product Fetch Ajax of Planning
    path('planning/fetchBranch', views.fetchSales, name="fetchData"),
    path('planning/fetchQt', views.fetchQuantity, name="fetchQt"),
    path('planning/fetchRe', views.fetchReserved, name="fetchRe"),
    path('planning/fetchAv', views.fetchAvailable, name="fetchAv"),

    # PerformaInvoice Urls
    path('performaInvoice/', views.performaInvoice, name='performaInvoice'),
    path('performaInvoice/Add/', views.performaInvoiceAdd, name='performaInvoiceAdd'),
    path('performaInvoiceUpdate/<str:pk>/', views.performaInvoiceUpdate, name='performaInvoiceUpdate'),
    path('performaInvoiceDelete/<str:pk>/', views.performaInvoiceDelete, name='performaInvoiceDelete'),
    path('performaInvoicePDF/<str:pk>/', views.performaInvoicePDF, name='performaInvoicePDF'),

    # Sales Order Urls/
    path('salesOrder/', views.salesOrder, name="salesOrder"),
    path('salesOrder/Add/', views.salesOrderAdd, name="salesOrderAdd"),
    path('salesOrderUpdate/<str:pk>/', views.salesOrderUpdate, name="salesOrderUpdate"),
    path('salesOrderDelete/<str:pk>/', views.salesOrderDelete, name="salesOrderDelete"),
    path('salesOrderPDF/<str:pk>/', views.salesOrderPDF, name="salesOrderPDF"),
]