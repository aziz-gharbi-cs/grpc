from concurrent import futures
import grpc

import prime_pb2
import prime_pb2_grpc
from prime_service import is_prime, factorize


class PrimeService(prime_pb2_grpc.PrimeServiceServicer):

    def IsPrime(self, request, context):
        n = request.n

        if is_prime(n):
            return prime_pb2.PrimeResponse(
                n=n,
                is_prime=True,
                message=f"{n} est premier"
            )

        factors = factorize(n) if n > 1 else []

        return prime_pb2.PrimeResponse(
            n=n,
            is_prime=False,
            factors=factors,
            message=f"{n} n'est pas premier"
        )

    def FirstPrime(self, request, context):
        count = request.count
        n = 2
        sent = 0

        while sent < count:
            if is_prime(n):
                yield prime_pb2.PrimeNumber(value=n)
                sent += 1
            n += 1


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    prime_pb2_grpc.add_PrimeServiceServicer_to_server(
        PrimeService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Serveur gRPC demarre sur le port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
