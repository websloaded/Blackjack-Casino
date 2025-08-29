import random

# Función para calcular la suma de las cartas
def calcular_mano(mano):
    total = sum(mano)
    ases = mano.count(1)
    while ases > 0 and total + 10 <= 21:
        total += 10
        ases -= 1
    return total

# Función para mostrar las manos
def mostrar_manos(jugador, crupier, ocultar=False):
    if ocultar:
        print(f"Tus cartas: {jugador} = {calcular_mano(jugador)}")
        print(f"Cartas del crupier: [{crupier[0]}, ?]")
    else:
        print(f"Tus cartas: {jugador} = {calcular_mano(jugador)}")
        print(f"Cartas del crupier: {crupier} = {calcular_mano(crupier)}")

# Función para sacar una carta aleatoria
def sacar_carta():
    return random.choice([1,2,3,4,5,6,7,8,9,10,10,10,10])

# Turno del jugador
def turno_jugador(mano, auto_ganar=False):
    while True:
        mostrar_manos(mano, [0, 0], ocultar=True)
        total = calcular_mano(mano)

        if auto_ganar and total == 21:
            print("Has llegado a 21! Ganas automáticamente ✅")
            return mano, True

        if total >= 21:
            return mano, False

        accion = input("¿Querés pedir carta (p) o plantarte (s)? ").lower()
        if accion == "p":
            if auto_ganar:
                posibles = [c for c in range(1,12) if total + c <= 21]
                if not posibles:
                    print("No hay cartas seguras, te plantas automáticamente.")
                    break
                carta = random.choice(posibles)
            else:
                carta = sacar_carta()
            print(f"Te salió un {carta}")
            mano.append(carta)
        else:
            break
    return mano, False

# Turno del crupier
def turno_crupier(crupier, jugador_total, jugador_mano, crupier_gana_ronda=False):
    while True:
        crupier_total = calcular_mano(crupier)

        if crupier_total > 21:
            print(f"El crupier se pasó de 21 con {crupier} = {crupier_total}")
            break

        # Plantarse normalmente entre 17 y 21
        if 17 <= crupier_total <= 21:
            if crupier_gana_ronda and crupier_total <= jugador_total:
                posibles = [c for c in range(1,12) if crupier_total + c > jugador_total]
                if posibles:
                    carta = random.choice(posibles)
                    crupier.append(carta)
                    continue
            break

        # Pedir carta normalmente si <17
        carta = sacar_carta()
        crupier.append(carta)

    return crupier

# Patrón de rondas
patron_rondas = [True, True, False, True, False, False, None, False, False, False]

def jugar():
    for i in range(10):
        print(f"\n===== RONDA {i+1} =====")
        jugador = [sacar_carta(), sacar_carta()]
        crupier = [sacar_carta(), sacar_carta()]

        ronda_ganar_jugador = patron_rondas[i] == True
        ronda_empate = patron_rondas[i] is None

        # Turno jugador
        jugador, auto_ganar = turno_jugador(jugador, auto_ganar=ronda_ganar_jugador)
        jugador_total = calcular_mano(jugador)

        # Si el jugador se pasa de 21, crupier gana automáticamente
        if jugador_total > 21:
            mostrar_manos(jugador, crupier)
            print("Te pasaste de 21. El crupier gana automáticamente ❌")
            continue

        if auto_ganar:
            crupier_total = calcular_mano(crupier)
            mostrar_manos(jugador, crupier)
            print("Ganaste la ronda ✅")
            continue

        # Turno crupier
        print("Turno del crupier:")
        crupier = turno_crupier(crupier, jugador_total, jugador, crupier_gana_ronda=(not ronda_ganar_jugador))
        crupier_total = calcular_mano(crupier)
        mostrar_manos(jugador, crupier)

        # Determinar ganador
        if crupier_total > 21:
            print("El crupier se pasó. Ganaste ✅")
        elif jugador_total > crupier_total:
            print("Ganaste la ronda ✅")
        elif jugador_total < crupier_total:
            print("El crupier gana ❌")
        else:
            if ronda_empate:
                print("Empate ⚖️")
            else:
                if ronda_ganar_jugador:
                    print("Ganaste la ronda ✅")
                else:
                    print("El crupier gana ❌")

if __name__ == "__main__":
    jugar()
