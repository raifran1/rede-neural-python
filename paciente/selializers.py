from rest_framework import serializers

from paciente.models import Paciente


class RedeNeuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        exclude = ['infectado']