import grpc

import prime_pb2
import prime_pb2_grpc


channel = grpc.insecure_channel("localhost:50051")
stub = prime_pb2_grpc.PrimeServiceStub(channel)

while True:
    print("\n--- MENU ---")
    print("1. Verifier si un nombre est premier")
    print("2. Afficher les N premiers nombres premiers")
    print("0. Quitter")

    choice = input("Votre choix : ")

    if choice == "1":
        n = int(input("Entrer un nombre : "))

        response = stub.IsPrime(prime_pb2.PrimeRequest(n=n))

        if response.is_prime:
            print(response.message)
        else:
            if response.factors:
                factors = " * ".join(map(str, response.factors))
                print(f"{response.message} : {n} = {factors}")
            else:
                print(response.message)

    elif choice == "2":
        count = int(input("Combien de nombres premiers ? "))

        if count < 0:
            print("Veuillez entrer un nombre positif ou nul.")
            continue

        responses = stub.FirstPrime(
            prime_pb2.FirstPrimeRequest(count=count)
        )

        print("Nombres premiers :")
        for response in responses:
            print(response.value, end=" ")

        print()

    elif choice == "0":
        break

    else:
        print("Choix invalide.")

channel.close()
