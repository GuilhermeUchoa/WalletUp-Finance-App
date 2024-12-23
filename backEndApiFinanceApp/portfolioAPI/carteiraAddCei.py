from . models import PortfolioModels as Carteira
from django.contrib.auth.models import User
import pandas as pd


# Preciso melhorar esse codigo
def carteiraAddCei(request, arquivo):
    
    xls = pd.ExcelFile(arquivo)
    dictAtivo = {}
    listaCarteiraDF = []
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(arquivo, sheet_name=sheet_name).dropna()
        dictAtivo[sheet_name] = df
    

    for chave, valor in dictAtivo.items():

        for i in range(len(valor)):

            if chave == 'Tesouro Direto':

                ativo = valor['Produto'].loc[i]

            else:
                ativo = valor['Código de Negociação'].loc[i]

            # Add para lista de carteiras que tem no DataFrame
            listaCarteiraDF.append(ativo)

            try:

                if Carteira.objects.filter(ativo=ativo, usuario=request.user).get().ativo == ativo and chave != 'Tesouro Direto':
                    carteira = Carteira.objects.filter(ativo=ativo,usuario=request.user).get()
                    carteira.quantidade = valor['Quantidade'].loc[i]
                    carteira.usuario = request.user
                    carteira.save()
                    print(f'Ativo {ativo} atualizado')
                else:
                    carteira = Carteira.objects.filter(
                        ativo=ativo, usuario=request.user).get()
                    carteira.quantidade = float(valor['Quantidade'].loc[i])
                    carteira.cotacao = float(
                        valor['Valor Atualizado'].loc[i]/valor['Quantidade'].loc[i])
                    carteira.valor = float(valor['Valor Atualizado'].loc[i])
                    carteira.precoMedio = 0
                    carteira.usuario = request.user
                    carteira.save()
                    print(f'Ativo do tipo RendaFixa {ativo} atualizado')

            except:

                if chave == 'Tesouro Direto':
                    print(valor['Quantidade'].loc[i])
                    carteira = Carteira(
                        ativo=ativo,
                        quantidade=valor['Quantidade'].loc[i],
                        cotacao=valor['Valor Atualizado'].loc[i] /
                        valor['Quantidade'].loc[i],
                        valor=valor['Valor Atualizado'].loc[i],
                        tipo=chave
                    )
                else:
                    carteira = Carteira(
                        ativo=ativo,
                        quantidade=valor['Quantidade'].loc[i],
                        cotacao=0,
                        valor=0,
                        tipo=chave
                    )
                carteira.usuario = request.user
                carteira.save()

                print(f'novo ativo {ativo} adicionado a carteira')

    # Compara a carteira da B3 com a do APP se tiver algo a mais na carteira do APP significa que me desfiz do ativo na corretora e entao ele exclui o ativo da Carteira do app
    listaCarteiraBD = [i.ativo for i in Carteira.objects.all()]
    listaDeExclusao = list(
        set(listaCarteiraBD).difference(set(listaCarteiraDF)))
    for i in listaDeExclusao:

        carteira = Carteira.objects.filter(ativo=i,usuario=request.user).delete()
        print(f'Ativo {i} foi excluido da carteira')


def precoMedioAnual(arquivo):
    df = pd.read_excel(arquivo, sheet_name=0)

    for i in df['Código de Negociação'].unique():
        valorMedio = round(float(df[df['Código de Negociação'] == i]['Valor'].sum(
        ) / df[df['Código de Negociação'] == i]['Quantidade'].sum()), 2)

        if i[-1] == 'F':
            ativo = i[0:-1]
        else:
            ativo = i

        try:
            carteira = Carteira.objects.filter(ativo=ativo).get()
            carteira.precoMedio = valorMedio
            print(
                f'Ativo {ativo} teve seu preco medio atualizado para {valorMedio}')

            carteira.save()
        except:
            pass
