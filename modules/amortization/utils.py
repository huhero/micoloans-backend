

def calculate_amortization_amount(amount: int, interest: float, period: int):
    '''
    Calcular el monto de la cuota a pagar cada mes.

    R: es la renta, es decir, el monto de la cuota a pagar cada mes, y el cual hay que calcular.
    A: es el monto del crédito adquirido.
    i: es la tasa de interés mensual que se debe pagar por el crédito.
    n: es el número de meses durante los cuales se debe cancelar el crédito.

    Formula:
    R = A * i / (1 - (1 / (1 + i) )^n)
    '''
    x = amount * interest
    R = x / (1 - (1 / (1 + interest))**period)
    return round(R, 2)


def amortization_schedule(principal: int, interest_rate: float, period: int):
    '''
    Periodo (primera columna): son los distintos lapsos de tiempo en los que se debe hacer el pago de cada cuota del crédito, que generalmente es cada mes, pero también puede ser trimestral, semestral, etc.
    Cuota (segunda columna): es el monto que se debe ir pagando en cada periodo, y se forma por la suma de los intereses más el monto de amortización.
    Interés (tercera columna): es el porcentaje de interés que se debe pagar dentro de cada cuota por el crédito adquirido.
    Amortización (cuarta columna): es el monto que se devuelve del crédito en cada periodo, pero sin tener en cuenta los intereses.
    Saldo (quinta columna): es el monto total del crédito que falta por pagar, y que se va reduciendo después de cada periodo hasta llegar a 0.
    '''
    amortization_amount = calculate_amortization_amount(
        principal, interest_rate, period
    )
    number = 1
    balance = principal
    while number <= period:
        interest = round(balance * interest_rate, 2)
        principal = round(amortization_amount - interest, 2)
        balance = round(balance - principal, 2)
        yield {
            "number": number,
            "amortization_amount": amortization_amount,
            "interest": interest,
            "principal": principal,
            "balance": balance
        }
        number += 1


# if __name__ == "__main__":
#     A = 15000
#     n = 5
#     i = 0.05

#     results = amortization_schedule(A, i, n)
#     for result in results:
#         print(result)
