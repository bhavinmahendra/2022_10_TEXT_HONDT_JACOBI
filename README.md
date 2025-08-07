This project is divided in three parts:
 - Text format: given a string (cadeia) and a width (n), it formats the text, justifiying the text. To use it, run the function justifica_texto(cadeia, n).
 - Hondt's Method: it gives us in order the elected political parties, given a dictionary that stores the number of deputies, the parties and the votes for a given place. The dictionary has to in the form:
    data = {’Endor’: {’deputados’: 7, ’votos’: {’A’:12000, ’B’:7500, ’C’:5250, ’D’:3000}},
            ’Hoth’: {’deputados’: 6, ’votos’: {’B’:11500, ’A’:9000, ’E’:5000, ’D’:1500}},
            ’Tatooine’: {’deputados’: 3, ’votos’: {’A’:3000, ’B’:1900}}}
   To use it, run obtem_resultado_eleicoes(data).
 - Jacobi's Method: given a matrix and a vector (both in tuples), it solves it using Jacobi's Method. To use it, run the function resolve_sistema(A, c, e), with A the coeffiencts matrix, c the independent terms vector and e a really small value (since it is a tolerance).

Note: This is an academic project. The idea of the project came from Albert Abad (Instituto Superior Técnico, Lisbon, Portugal)
