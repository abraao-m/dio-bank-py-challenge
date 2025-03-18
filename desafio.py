from datetime import datetime

def deposit(value, balance, statement, operations, operations_limit, /):

    global initial_date

    if(datetime.now().strftime("%d") != initial_date.strftime("%d")):
        operations = 0
        initial_date = datetime.now()

    if operations < operations_limit:
        statement += f" | + R$ {value:<14.2f} | {datetime.now().strftime("%d-%m-%Y %H:%M"):^15} |\n"
        balance += value
        operations += 1
        print("Depósito feito com sucesso!")

    return balance, statement, operations

def withdraw(*, value, balance, statement, operations, operations_limit, withdraw_limit):

    global initial_date

    if(datetime.now().strftime("%d") != initial_date.strftime("%d")):
        operations = 0
        initial_date = datetime.now()

    if balance >= value and value > 0 and value <= withdraw_limit and operations < operations_limit:
        statement += f" | - R$ {value:<14.2f} | {datetime.now().strftime("%d-%m-%Y %H:%M"):^15} |\n"
        balance -= value
        operations += 1

    else:
        if value > withdraw_limit:
            print(f"Valor máximo para saque é R$ {withdraw_limit}")

        else:
            print(f"Operação inválida! Saldo da conta: [R$ {balance:.2f}]")

    return balance, statement, operations

def check_statement(balance, /, *, statement):
    if statement:
        # formatted_statement = "\n".join(f" | {value[0]} R$ {value[1:]}" for value in statement)
        print(f"{statement} \nSaldo: R$ {balance:.2f}")

    else:
        print("Nenhuma transação realizada.")

def create_user(users):
    cpf = input("Informe:\n\tCPF (Apenas numeros): ")

    if filter_users(users, cpf):
        print("Usuário já existe!")
        return
    
    name = input("\tNome: ")
    birth_date = input("\tData de nascimento (dd-mm-aaaa): ")
    address = input("\tEndereço (logradouro, nro - bairro - cidade/sigla estado): ")

    user = {
        "cpf": cpf,
        "name": name,
        "birth_date": birth_date,
        "address": address
    }

    users.append(user)
    print("Usuário criado com sucesso!")

def filter_users(users, cpf):
    filtered_user = [user for user in users if cpf == user["cpf"]]
    return filtered_user[0] if filtered_user else False

def create_current_account(users, accounts, branch, account_number):
    cpf = input("Informe seu CPF: ")
    filtered_user = filter_users(users, cpf)

    if filtered_user:
        account = {"branch": branch, "account_number":account_number, "user": filtered_user["name"]}
        accounts.append(account)
        account_number += 1
        print("Conta criada com sucesso!") 
    
    else:
        print("Usuário não existe!")

    return account_number

def list_accounts(accounts):
    if accounts:
        for account in accounts:
            print(f"""\
    Agência: {account["branch"]}
    Conta:   {account["account_number"]}
    Titular: {account["user"]}
            """)
    else:
        print("Não há contas no banco de dados!")

def main():

    BRANCH = "0001"
    OPERATIONS_LIMIT = 10
    WITHDRAW_LIMIT = 500
    
    balance = 0.0
    statement = ""
    operations_today = 0
    account_number = 1
    users = []
    accounts = []

    global initial_date
    initial_date = datetime.now()

    while True:
        op = input("""
===============================
 [1] Depósito
 [2] Saque
 [3] Extrato
 [4] Criar Usuário
 [5] Criar Conta
 [6] Listar Contas
 [7] Sair
===============================
> """)
        
        if op == "1":
            if operations_today == OPERATIONS_LIMIT:
                print("Limite diário de operações excedido!")
                continue

            value = input("Digite o valor do depósito: ")

            try:
                value = float(value)
                if(value <= 0):
                    print("Valor tem que ser maior que 0")
            except ValueError:
                continue
            
            balance, statement, operations_today = deposit(
                value,
                balance,
                statement,
                operations_today,
                OPERATIONS_LIMIT
            )

        elif op == "2":
            if operations_today == OPERATIONS_LIMIT:
                print("Limite diário de operações excedido!")
                continue

            value = input("Digite o valor do saque: ")

            try:
                value = float(value)
                if(value <= 0):
                    print("Valor tem que ser maior que 0")
            except ValueError:
                continue
            
            balance, statement, operations_today = withdraw(
                value=float(value),
                balance=balance,
                statement=statement,
                operations=operations_today,
                operations_limit=OPERATIONS_LIMIT,
                withdraw_limit=WITHDRAW_LIMIT
            )

        elif op == "3":
            check_statement(balance, statement=statement)

        elif op == "4":
            create_user(users)
        elif op == "5":
            account_number = create_current_account(users, accounts, BRANCH, account_number)
        elif op == "6":
            list_accounts(accounts)
        elif op == "7":
            quit()

        else:
            print("Opção inválida!")

main()