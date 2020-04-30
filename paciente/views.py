from django.http import Http404, HttpResponse
from django.shortcuts import render
import pandas as pd
from rest_framework import viewsets, authentication, permissions, status, views
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from paciente.models import Paciente
from paciente.selializers import RedeNeuralSerializer


class TreinoRedeNeural(GenericAPIView):
    def get(self, request, pk=None, var=None):
        respostas2 = Paciente.objects.all().values('infectado')
        respostas = []
        for i in respostas2:
            if i.get('infectado') == 0:
                respostas.append(0)
            else:
                respostas.append(1)

        dados2 = Paciente.objects.all().values('febreM', 'febreA', 'tosseP', 'tosseS', 'fdeAr', 'dparaResp',
                                               'pGastrico', 'diarreia')
        dados = []
        for i in dados2:
            lista = []
            for j in i:
                if i.get(j) == 1:
                    lista.append(1)
                else:
                    lista.append(0)
            dados.append(lista)

        print('respostas:', respostas)
        print('dados:', dados)
        print("Carregando dados")
        # excel_file = baseDeDados
        # base = pd.read_excel(excel_file, encoding='latin−1')
        # estão em todas as linhas da coluna 8
        # respostas = base.iloc[:, 8].values EX: [1,0,0,1,0,1,1,1,0,1,0,1]
        # estão em todas as linhas até a coluna 8
        # dados = base.iloc[:, :8].values EX: [[1,0,0,1],[0,1,1,1],[0,1,0,1]]
        # anotação exemplo
        # : ----> todos
        # 1:10--> valores de 1 até 10
        # :10---> todos os valores até 10
        # 10 ---> somente valor 10
        print("Separando dados ...")
        dadosTreinamento, dadosTeste, respostasTreinamento, respostasTeste = train_test_split(dados, respostas,
                                                                                              test_size=0.05,
                                                                                              random_state=0)
        # Rede Neural
        print("Aprendendo ...")
        # verbose= exibir_teste - Max_inter = Maximo de testes, tolerancia de erros
        classificador = MLPClassifier(verbose=False, max_iter=1000, tol=0.000010)
        # treinar
        classificador.fit(dadosTreinamento, respostasTreinamento)
        print("Concluído!")
        if var == None:
            return HttpResponse('Treino concluido')
        else:
            return classificador

class Teste(GenericAPIView):

    def get(self, request, paciente):
        paciente = get_object_or_404(Paciente, id=paciente)
        print(TreinoRedeNeural.get(self, request=request, var=1))
        paciente = paciente.values('febreM', 'febreA', 'tosseP', 'tosseS', 'fdeAr', 'dparaResp',
                                               'pGastrico', 'diarreia')
        if TreinoRedeNeural.get(self, request=request, var=1).predict(paciente.informar()):
            return HttpResponse('Paciente Infectado')
        else:
            return HttpResponse('Paciente Saudável')


class RedeNeural(viewsets.ModelViewSet):
    serializer_class = RedeNeuralSerializer
    queryset = Paciente.objects.all()