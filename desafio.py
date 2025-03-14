statement = []
WITHDRAW_LIMIT = 3
WITHDRAW_MAX_VALUE = 500
withdraw_times_today = 0


def deposit(value):
    if value > 0:
        statement.append("+" + str(value))

def check_statement():
    formatted_statement = "\n".join(f" R$ {value[0]}{float(value[1:]):.2f}" for value in statement)
    print(formatted_statement)

def calc_balance():
    balance = 0.0
    for value in statement:
        if "+" in value:
            balance += float(value[1:])
        elif "-" in value:
            balance -= float(value[1:])
    return balance

def withdraw(value):
        global withdraw_times_today
        if calc_balance() >= value and value > 0 and value <= WITHDRAW_MAX_VALUE and withdraw_times_today < WITHDRAW_LIMIT:
            statement.append("-" + str(value))
            withdraw_times_today += 1
        else:
            if withdraw_times_today == 3:
                print("Limite de saque excedido!")
            elif value > WITHDRAW_MAX_VALUE:
                print(f"Valor máximo para saque é R$ {WITHDRAW_MAX_VALUE}")
            else:
                print(f"Operação inválida! Saldo da conta: [R$ {calc_balance():.2f}]")

def solve():
    while True:
        op = input("""
=============================
    (1) Depósito
    (2) Saque
    (3) Extrato
    (4) Sair
=============================
> """)
        
        if op == "1":
            value = input("Digite o valor do depósito: ")
            if not value.isdigit():
                continue
            deposit(float(value))
        elif op == "2":
            global withdraw_times_today
            if withdraw_times_today == WITHDRAW_LIMIT:
                print("Limite de saques diário excedido!")
                continue
            value = input("Digite o valor do saque: ")
            if not value.isdigit():
                continue
            withdraw(float(value))
        elif op == "3":
            check_statement()
        elif op == "4":
            quit()
        else:
            print("Opção inválida!")

solve()