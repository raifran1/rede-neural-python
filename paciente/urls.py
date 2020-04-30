from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'rede_neural', RedeNeural, basename=Paciente)
# router.register(r'treino_rede_neural', TreinoRedeNeural, basename=Paciente)

urlpatterns = [
    path('', include(router.urls)),
    path('treinar/', TreinoRedeNeural.as_view(), name='treinar'),
    path('teste/<int:paciente>/', Teste.as_view(), name='teste'),
]