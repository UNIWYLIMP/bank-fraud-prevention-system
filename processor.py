import random
import datetime


# Bank Processing


def create_bank_account(gmail, password, phone_number, home_address, authentication, fullname, bvn, nationality,
                        account_type):
    # userId
    # Bank Account

    authentication_value = "simple"
    if len(str(gmail)) == 0 or len(str(password)) == 0 or len(str(phone_number)) == 0 or len(
            str(home_address)) == 0 or len(
        str(fullname)) == 0 or len(str(bvn)) == 0 or len(str(nationality)) == 0:
        return "453", "Invalid Account Creation Request"
    if authentication == "2SV":
        authentication_value = "complex"
    else:
        pass

    if account_type == "personal" or account_type == "business":
        pass
    else:
        return "422", "Invalid Account Type"

    back_account = str("704") + str(random.randrange(1111111, 9999999))
    user_id = str(random.randrange(111111111111, 999999999999))

    file_list = open("user_list.db", "a")
    file_list.write(f"{gmail}~{fullname}~{password}~{back_account}~{user_id}~{home_address}~{bvn}~{phone_number}~"
                    f"{nationality}~{authentication_value}~{account_type}\n")
    file_list.close()

    new_single_record = open(f"./user_accounts/account_status/{user_id}.db", "w")
    new_single_record.write("0")
    new_single_record.close()

    new_single_record = open(f"./user_accounts/transactions/{user_id}.db", "w")
    new_single_record.write("")
    new_single_record.close()

    new_single_record = open(f"./user_accounts/account_limit/{user_id}.db", "w")
    new_single_record.write("10000000")
    new_single_record.close()

    new_single_record = open(f"./user_accounts/loans_savings/{user_id}.db", "w")
    new_single_record.write("")
    new_single_record.close()

    new_single_record = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
    new_single_record.write("ACTIVE")
    new_single_record.close()

    new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
    new_single_record.write("0")
    new_single_record.close()


def read_all_transaction_record(user_id):
    new_single_record = open(f"./user_accounts/transactions/{user_id}.db", "r")
    list_of_record = new_single_record.read().split("\n")
    transactions = []
    for single_transaction in list_of_record:
        y = single_transaction.split("~")
        # id date transaction_type description credit debit balance
        data = {
            "id": y[0], "date": y[1], "transaction_type": y[2], "description": y[3], "credit": y[4], "debit": y[5],
            "balance": y[6]
        }
        transactions.append(data)

    return transactions


def read_specific_user_account(user_id):
    new_single_record = open(f"user_list.db", "r")
    list_of_record = new_single_record.read().split("\n")
    user_data = []
    for single_user in list_of_record:
        y = single_user.split("~")
        user_id_index = user_index("user_id")

        if y[user_id_index] == user_id:
            user_data = y
            return user_data, status
        else:
            return 0, 0


def user_index(value):
    data_index = {
        "gmail": 0, "fullname": 1, "password": 2, "bank_account": 3, "user_id": 4, "home_address": 5, "bvn": 6,
        "phone_number": 7, "nationality": 8, "authentication_value": 9, "account_type": 10
    }
    try:
        return data_index.get(value)
    except NameError:
        return 55881
    except KeyError:
        return 55882
    except ValueError:
        return 55883


def authenticator(amount, transaction_type, transaction_code, user_id, password):
    time_obj = datetime.datetime.now()
    time_by_hour = time_obj.hour

    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "r")
    activation_status = file.read()

    if activation_status == "BANNED":
        return 99999, "User Account Banned"
    else:
        pass
    file.close()

    file = open("user_list.db", "r")
    records = file.read()
    get_user = []
    if transaction_code == "v1":
        read_file = open(f"./user_accounts/account_limit/{user_id}.db", "r")
        account_limit = int(read_file.read())
        read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
        account_balance = int(read_file.read())

        if (int(account_balance) + int(amount)) > int(account_limit):
            file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
            file.write("BANNED")
            return 3465, "Account Limit Exceeded."

        else:
            return 1, "Proceed"

    if transaction_code == "v2":
        read_file = open(f"./user_accounts/account_limit/{user_id}.db", "r")
        account_limit = int(read_file.read())
        read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
        account_balance = int(read_file.read())

        if (int(account_balance) + int(amount)) > int(account_limit):
            file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
            file.write("BANNED")
            return 3466, "Account Limit Exceeded."

        else:
            return 1, "Proceed"

    if transaction_code == "v3":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3467, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3467, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if hour > 5 and hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3467, "Unusual Activity Detected on Account."

    if transaction_code == "v4":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3468, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3468, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if hour > 5 and hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3468, "Unusual Activity Detected on Account."

    if transaction_code == "v5":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3469, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3469, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if hour > 5 and hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3469, "Unusual Activity Detected on Account."

    if transaction_code == "v6":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3470, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3470, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if hour > 5 and hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3470, "Unusual Activity Detected on Account."

    if transaction_code == "v7":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3471, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3471, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if hour > 5 and hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3471, "Unusual Activity Detected on Account."

    if transaction_code == "v8":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3472, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3472, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if 5 < hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3472, "Unusual Activity Detected on Account."

    if transaction_code == "v9":
        user_transactions = read_all_transaction_record(user_id)
        if len(user_transactions) < 150:
            return 1, "proceed"

        else:
            # check for average transaction amount
            # check for usual transaction time
            # check for unusual account activity (Sudden Increase in Transaction volume)
            average_volume = 0
            total_volume = 0
            counter = 0
            for single_transaction in user_transactions.reverse()[150]:
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 0:
                return 1, "proceed"
            else:
                average_volume = total_volume / counter
                super_size = (average_volume * 10) + 450000

                new_single_record = open(f"./user_accounts/single_withdrawal_limit/{user_id}.db", "w")
                new_single_record.write(f"{super_size}")
                new_single_record.close()

                if super_size < amount:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3473, "Unusual Transaction Volume."

            for single_transaction in user_transactions.reverse():
                withdrawal = int(single_transaction.get("debit"))
                if withdrawal == 0:
                    pass
                else:
                    total_volume += withdrawal
                    counter += 1
            if counter < 100:
                return 1, "proceed"
            else:
                first_half_transaction_volume = 0
                second_half_transaction_volume = 0
                for single_transaction in user_transactions.reverse()[:49]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        first_half_transaction_volume += withdrawal
                for single_transaction in user_transactions.reverse()[49:99]:
                    withdrawal = int(single_transaction.get("debit"))
                    if withdrawal == 0:
                        pass
                    else:
                        second_half_transaction_volume += withdrawal

                if (first_half_transaction_volume * 20) < second_half_transaction_volume:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3473, "Unusual Spending Activities Detected In Account."

            hour = int(f"{datetime.datetime.hour}")
            counter = 0
            if 5 < hour < 22:
                return 1, "proceed"
            else:
                for single_transaction in user_transactions.reverse()[:150]:
                    value_x = str(single_transaction.get("date")).split(" ")[1]
                    hour_compared = int(f"{value_x[0]}{value_x[1]}")
                    if hour_compared == hour:
                        counter += 1
                    else:
                        pass
                if counter < 3:
                    file = open(f"./user_accounts/account_activation_state/{user_id}.db", "w")
                    file.write("BANNED")
                    return 3473, "Unusual Activity Detected on Account."


# Deposit
def cash_deposit(amount, password, user_id, description):
    authenticate, message = authenticator(amount,  "credit",  "v1", user_id, password)
    if authenticate == 3465:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "cash_deposit"
    credit = amount
    debit = 0
    account_balance += amount

    read_new_file.write(f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{ account_balance}")
    read_file.close()

    return 1, "proceed"


def direct_deposit(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "credit", "v2", user_id, password)
    if authenticate == 3466:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "direct_deposit"
    credit = amount
    debit = 0
    account_balance += amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


# Withdrawals
def atm_withdrawal(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v3", user_id, password)
    if authenticate == 3467:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "atm_withdrawal"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def cash_withdrawal(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v4", user_id, password)
    if authenticate == 3468:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "cash_withdrawal"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def electronic_withdrawal(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v5", user_id, password)
    if authenticate == 3469:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "electronic_withdrawal"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


# Transfers
def internal_transfer(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v6", user_id, password)
    if authenticate == 3470:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "internal_transfer"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def external_transfer(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v7", user_id, password)
    if authenticate == 3471:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "external_transfer"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


# Payments
def debit_card_payment(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v8", user_id, password)
    if authenticate == 3472:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "debit_card_payment"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def loan_payment(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v8", user_id, password)
    if authenticate == 3472:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "loan_payment"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def bill_payment(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v8", user_id, password)
    if authenticate == 3472:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "bill_payment"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


# Interest And Fees
def interest_earned(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v9", user_id, password)
    if authenticate == 3473:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "bill_payment"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def interest_charged(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v9", user_id, password)
    if authenticate == 3473:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "interest_charged"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def service_fees(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v9", user_id, password)
    if authenticate == 3473:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "service_fees"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


def overdraft_fees(amount, password, user_id, description):
    authenticate, message = authenticator(amount, "debit", "v9", user_id, password)
    if authenticate == 3473:
        return authenticate, message

    # id date transaction_type description credit debit balance

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "r")
    account_balance = int(read_file.read())

    read_new_file = open(f"./user_accounts/transactions/{user_id}.db", "a")
    if account_balance < amount:
        return 4383, "Insufficient Account Balance"

    transaction_id = str(random.randrange(1111111111111, 9999999999999))
    date = datetime.datetime.now()
    transaction_type = "overdraft_fees"
    credit = 0
    debit = amount
    account_balance -= amount

    read_new_file.write(
        f"{transaction_id}~{date}~{transaction_type}~{description}~{credit}~{debit}~{account_balance}\n")
    read_new_file.close()

    read_file = open(f"./user_accounts/account_status/{user_id}.db", "w")
    read_file.write(f"{account_balance}")
    read_file.close()

    return 1, "proceed"


response = create_bank_account("uniwylimp@gmail.com", "34b4531gg", "+2348053996040",
                               "6b Akintola Odeyemi Street", "2SV",
                               "Aderibigbe Ayomide Oluwabusayo", "3563854920", "Nigerian", "personal")
