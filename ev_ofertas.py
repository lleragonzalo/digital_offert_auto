import requests

URL_OFERTAS = "http://127.0.0.1:8000/ofertas/"
URL_EVALUACION = "http://127.0.0.1:8000/evaluacion/"
URL_EVALUACIONES = "http://127.0.0.1:8000/evaluaciones/"

response_ofertas = requests.get(URL_OFERTAS)

if response_ofertas.status_code == 200:
    ofertas = response_ofertas.json()

    if not ofertas:
        print("⚠️ No hay ofertas registradas en la base de datos. Agrega ofertas antes de evaluar.")
    else:
        print(f"🔍 Se encontraron {len(ofertas)} ofertas registradas.")

        # **Paso 2: Evaluar cada oferta**
        for oferta in ofertas:
            id_oferta = oferta.get("id")
            if id_oferta:
                response_eval = requests.post(f"{URL_EVALUACION}{id_oferta}")

                if response_eval.status_code == 200:
                    print(f"✅ Oferta {id_oferta} evaluada correctamente.")
                else:
                    print(f"❌ Error evaluando la oferta {id_oferta}: {response_eval.json()}")

        print("\n✅ Todas las ofertas han sido evaluadas correctamente.\n")

        response_evaluaciones = requests.get(URL_EVALUACIONES)

        if response_evaluaciones.status_code == 200:
            evaluaciones = response_evaluaciones.json()
            print("🔍 Evaluaciones disponibles:", evaluaciones)
        else:
            print(f"⚠️ Error obteniendo evaluaciones: {response_evaluaciones.json()}")

else:
    print(f"❌ Error obteniendo las ofertas: {response_ofertas.json()}")
