'''
Bhavin Mahendra Gulab
Projeto - Formatacao de Texto, Metodo de Hondt (Eleicoes) e 
Metodo de Jacobi (Sistemas de Equacoes Lineares, com diagonal dominante)
'''

####################################### Formatacao de Texto #######################################

def limpa_texto(cadeia):
    '''
    str -> str
    limpa uma cadeia
    '''
    lst = cadeia.split()
    cad_limpa = ' '.join(lst)
    return cad_limpa

def corta_texto(lst, n):
    '''
    cad caracteres x int -> cad caracteres x cad caracteres
    inseres espacos entre palavras
    '''

    if len(lst) <= n:
        return lst, ''
    
    while n > 0 and lst[n] != ' ':
        n -= 1

    return lst[:n], lst[n+1:]

def insere_espacos(cadeia, n):
    '''
    cad caracteres x int -> cad caracteres
    inseres espacos entre palavras
    '''
    x = cadeia.split()
    if len(x) == 1:
        while len(cadeia) < n:
            cadeia += ' '
        return cadeia
    new = ''
    i = 1
    while len(new) < n:
        new = (i * ' ').join(x)
        i += 1
    a = len(new)-1
    while a >= 0 and len(new) > n:
        if new[a] == ' ' and new[a-1] != ' ':
            new = new[:a] + new[a+1:]
        a -= 1
    return new

def justifica_texto(cadeia, n):
    '''
    cad caracteres x int -> tuplo
    usa as funcoes anteriores para limpar um texto e depois corta essa cadeia limpa
    e insere espacos entre as palavras para justificar o texto
    '''
    if (not isinstance(cadeia, str)) or (not isinstance(n, int)) or (n <= 0) or (len(cadeia) == 0):
        raise ValueError('justifica_texto: argumentos invalidos')
    
    texto_limpo = limpa_texto(cadeia)
    palavras = texto_limpo.split()

    for i in palavras:
        if len(i) > n:
            raise ValueError('justifica_texto: argumentos invalidos')

    final = ()
    cadeia = limpa_texto(cadeia)
    while len(cadeia) > n:
        x = corta_texto(cadeia, n)
        x_justificado = insere_espacos(x[0], n)
        cadeia = x[-1]
        final += (x_justificado,)
    
    preenche = n - len(cadeia)
    final += (cadeia + ' ' * preenche,)

    return final

######################################### Metodo de Hondt #########################################

def calcula_quocientes(dicionario, n):
    '''
    dict x int -> dict
    calcula quocientes para cada partido de um circulo eleitoral
    '''
    final = {}
    lista = []
    for i in dicionario:
        j = 1
        while j <= n:
            lista.append(int(dicionario[i])/j)
            j += 1
        final[i] = lista
        lista = []
    return final

def atribui_mandatos(dicionario, n):
    '''
    dict x int -> list
    analisa atraves da funcao antes descrita a quem deve atribuir os mandatos
    de acordo com o inteiro de entrada
    '''
    quocientes = calcula_quocientes(dicionario, n)
    lista_completa = []
    lista = []
    for i in quocientes:
        for j in quocientes[i]:
            lista_completa.append([j, i])
    lista_completa.sort()
    lista_completa.reverse()
    for i in lista_completa:
        lista.append(i[1])
        if len(lista) == n:
            break
    return lista

def obtem_partidos(dicionario):
    '''
    dict -> list
    devolve todos os partidos participantes numa eleicao
    '''
    lista = []
    for i in dicionario:
        for j in dicionario[i]['votos']:
            if j not in lista:
                lista.append(j)
    lista.sort()
    return lista
    
def obtem_resultado_eleicoes(dicionario):
    '''
    dict -> list
    recorre as funcoes anteriores para calcular o resultado de umas eleicoes
    atrasves do metodo de hondt
    '''
    if type(dicionario) != dict or len(dicionario) == 0:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    
    for i in dicionario:
        if type(i) != str or len(dicionario[i]) == 0:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        for j in dicionario[i]:
            if j not in ('deputados', 'votos'):
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            if type(dicionario[i]['deputados']) != int or type(dicionario[i]['votos']) != dict or dicionario[i]['deputados'] < 0 or len(dicionario[i]['votos']) == 0:
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            for k in dicionario[i]['votos']:
                if type(k) != str or type(dicionario[i]['votos'][k]) != int or dicionario[i]['votos'][k] < 0:
                    raise ValueError('obtem_resultado_eleicoes: argumento invalido')

    lista = []
    lista_tuplo = []
    n = 0
    soma = 0
    partidos = obtem_partidos(dicionario)
    for i in partidos:
        for j in dicionario:
            if 'deputados' not in dicionario[j]:
                raise ValueError('obtem resultado eleicoes: argumento invalido')
            if 'votos' not in dicionario[j]:
                raise ValueError('obtem resultado eleicoes: argumento invalido')
            if i in dicionario[j]['votos']:
                soma += dicionario[j]['votos'][i]
            k = atribui_mandatos(dicionario[j]['votos'], dicionario[j]['deputados'])
            for l in k:
                if l == i:
                    n += 1
            pre_tuplo = [n, soma, i]
        lista.append(pre_tuplo)
        n = 0
        soma = 0
    lista.sort()
    lista.reverse()
    for a in lista:
        x = a[-1]
        a.pop(-1)
        a.insert(0, x)
    for b in lista:
        tuplo = ()
        for c in b:
            tuplo += (c,)
        lista_tuplo.append(tuplo)
    return lista_tuplo

######################################### Metodo de Jaobi #########################################

def produto_interno(t1, t2):
    '''
    tuplo x tuplo -> real
    calcula o produto interno de dois vetores
    '''
    soma = 0
    for i in range(len(t1)):
        soma += t1[i]*t2[i]
    return float(soma)

def verifica_convergencia(A, c, x, e):
    '''
    tuplo x tuplo x tuplo x real -> booleano
    verifica a convergencia de uma solucao de um sistema de equacoes
    com recurso a uma formula
    '''
    tuplo = ()
    soma = 0
    for l in A:
        soma = produto_interno(l, x)
        tuplo += (soma,)
    for i in range(len(tuplo)):
        if not (abs(tuplo[i] - c[i]) < e):
            return False
    return True

def retira_zeros_diagonal(A, c):
    '''
    tuplo x tuplo -> tuplo x tuplo
    retira zeros da diagonal de uma matriz fazendo troca de linhas
    '''
    A = list(A)
    c = list(c)
    for i in range(len(A)):
        if A[i][i] == 0:
            for j in range(len(A[i])):
                if A[j][i] != 0 and A[i][j] != 0:
                    A[i], A[j] = A[j], A[i]
                    c[i], c[j] = c[j], c[i]
                    break

    return tuple(A), tuple(c)

def eh_diagonal_dominante(A):
    '''
    tuplo x booleano
    verifica se uma matriz e diagonalmente dominante
    '''
    for i in range(len(A)):
        soma = 0
        for j in range(len(A[i])):
            if j != i:
                soma += abs(A[i][j])
            elif j == i:
                v = A[i][j]
        if abs(v) < soma:
            return False
    return True

def resolve_sistema(A, c, e):
    '''
    tuplo x tuplo x real -> tuplo
    resolve o sistema utilizando o metodo de jacobi
    '''
    if type(A) != tuple or type(c) != tuple or type(e) != float or e < 0:
        raise ValueError("resolve_sistema: argumentos invalidos")
    
    for i in range(len(A)):
        if type(A[i]) != tuple or len(A[i]) != len(A) or len(c) != len(A):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for j in range(len(A[i])):
            if type(A[i][j]) != float and type(A[i][j]) != int:
                raise ValueError("resolve_sistema: argumentos invalidos")
        if type(c[i]) != float and type(c[i]) != int:
            raise ValueError("resolve_sistema: argumentos invalidos")

    A, c = retira_zeros_diagonal(A, c)
    if not eh_diagonal_dominante(A):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")

    x = [0] * len(c)
    x_new = [0] * len(c)
    
    for _ in range(int(1/e)): 
        for i in range(len(c)):
            pi = produto_interno(A[i], tuple(x)) - A[i][i] * x[i]
            x_new[i] = (c[i] - pi)/A[i][i]
        
        if verifica_convergencia(A, c, tuple(x_new), e):
            return tuple(x_new)
        
        x = x_new.copy()
    return tuple(x)
