#!-*- coding: utf8 -*-

import pandas as pd
from collections import Counter
import numpy as np
from sklearn.cross_validation import cross_val_score
import nltk
import log_writer as log

# classificacoes = pd.read_csv('forums_rand_multilabel.csv', encoding = 'utf-8')
classificacoes = pd.read_csv('forums_rand.csv', encoding = 'utf-8')


textosPuros = classificacoes['email'] #num,email,categoria


frases = textosPuros.str.lower()
textosQuebrados = [nltk.tokenize.word_tokenize(frase) for frase in frases]


stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()

dicionario = set()


for lista in textosQuebrados:
    validas = [stemmer.stem(palavra) for palavra in lista if palavra not in stopwords and len(palavra) > 2]
    dicionario.update(validas)

#print(dicionario)

totalDePalavras = len(dicionario)
tuplas = zip(dicionario, range(totalDePalavras))
tradutor = {palavra:indice for palavra, indice in tuplas}
print (totalDePalavras)

def vetorizar_texto(texto, tradutor):
    vetor = [0] * len(tradutor)
    for palavra in texto:
        if len(palavra) > 0:
            raiz = stemmer.stem(palavra)
            if raiz in tradutor:
                posicao = tradutor[raiz]
                vetor[posicao] += 1

    return vetor

vetoresDeTexto = [vetorizar_texto(texto, tradutor) for texto in textosQuebrados]
#marcas = classificacoes['categoria1','categoria2','categoria3']
# marcas = classificacoes[['categoria1','categoria2','categoria3']]
# print (marcas)

from sklearn.preprocessing import MultiLabelBinarizer
lista_labels = classificacoes['categoria'].tolist()
marcas_aux = []
for i in lista_labels:
    marcas_aux.append([i])

print (marcas_aux)

marcas = MultiLabelBinarizer().fit_transform(marcas_aux)
print (marcas)

X = np.array(vetoresDeTexto)
#Y = np.array(marcas.tolist())
Y = np.array(marcas)

porcentagem_de_treino = 0.8

tamanho_de_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_validacao = len(Y) - tamanho_de_treino

print (tamanho_de_treino)

treino_dados = X[0:tamanho_de_treino]
treino_marcacoes = Y[0:tamanho_de_treino]

validacao_dados = X[tamanho_de_treino:]
validacao_marcacoes = Y[tamanho_de_treino:]

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes):
    k = 10
    scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv = k)
    taxa_de_acerto = np.mean(scores)
    msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
    print (msg)
    return taxa_de_acerto

def teste_real(modelo, validacao_dados, validacao_marcacoes):
    resultado = modelo.predict(validacao_dados)

    acertos = resultado == validacao_marcacoes

    total_de_acertos = sum(acertos)
    total_de_elementos = len(validacao_marcacoes)

    taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

    msg = "Taxa de acerto do vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_de_acerto)
    print(msg)

def predict_email(modelo, email_novo):
    texto_email = nltk.tokenize.word_tokenize(email_novo.lower())
    result = modelo.predict(vetorizar_texto(texto_email, tradutor))
    #log.registrar_classificacao(email_novo, result)
    print(result)
    # print(modelo.predict_proba(vetorizar_texto(texto_email, tradutor)))
    return result[0]



resultados = {}

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

# from sklearn.multiclass import OneVsOneClassifier
# modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
# resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
# resultados[resultadoOneVsOne] = modeloOneVsOne

# from sklearn.naive_bayes import MultinomialNB
# modeloMultinomial = MultinomialNB()
# resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes)
# resultados[resultadoMultinomial] = modeloMultinomial

# from sklearn.ensemble import AdaBoostClassifier
# modeloAdaBoost = AdaBoostClassifier(random_state=0)
# resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes)
# resultados[resultadoAdaBoost] = modeloAdaBoost

print (resultados)

maximo = max(resultados)
vencedor = resultados[maximo]

print ("Vencerdor: ")
print (vencedor)

vencedor.fit(treino_dados, treino_marcacoes)

teste_real(vencedor, validacao_dados, validacao_marcacoes)

# Contar as combinações diferentes, usar 
# acerto_base = max(Counter(validacao_marcacoes).values())
# taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)
# print("Taxa de acerto base: %f" % taxa_de_acerto_base)

total_de_elementos = len(validacao_dados)
print("Total de teste: %d" % total_de_elementos)

def predict_winner_email(email_novo):
    return predict_email(vencedor,email_novo)

# predict_email(vencedor, "Quero tentar realizar uma compra novamente, da primeira vez não foi reconhecido meu cartão e o pagamento foi cancelado")
#print(vencedor.predict(["Quero tentar realizar uma compra novamente, da primeira vez não foi reconhecido meu cartão e o pagamento foi cancelado"]) )