from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 8080))
