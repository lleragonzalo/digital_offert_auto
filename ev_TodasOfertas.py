import requests

URL_OFERTAS = "http://127.0.0.1:8000/ofertas/"
URL_EVALUACION = "http://127.0.0.1:8000/evaluacion/"
URL_EVALUACIONES = "http://127.0.0.1:8000/evaluaciones/"

metodos = ["aditivo", "multiplicativo", "leontieff"]

response_ofertas = requests.get(URL_OFERTAS)

if response_ofertas.status_code == 200:
    ofertas = response_ofertas.json()
    print(f"🔍 Se encontraron {len(ofertas)} ofertas registradas.")

    for oferta in ofertas:
        id_oferta = oferta["id"]
        for metodo in metodos:
            response_eval = requests.post(f"{URL_EVALUACION}{id_oferta}?metodo={metodo}")

            if response_eval.status_code == 200:
                print(f"✅ Oferta {id_oferta} evaluada con {metodo}.")
            else:
                print(f"❌ Error evaluando la oferta {id_oferta} con {metodo}: {response_eval.json()}")

    print("\n✅ Todas las ofertas han sido evaluadas correctamente.\n")

    response_evaluaciones = requests.get(URL_EVALUACIONES)

    if response_evaluaciones.status_code == 200:
        evaluaciones = response_evaluaciones.json()
        print("🔍 Evaluaciones disponibles:", evaluaciones)
    else:
        print(f"⚠️ Error obteniendo evaluaciones: {response_evaluaciones.json()}")

else:
    print(f"❌ Error obteniendo las ofertas: {response_ofertas.json()}")
