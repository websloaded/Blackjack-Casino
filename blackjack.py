import random

# Función para calcular la suma de las cartas
def calcular_mano(mano):
    total = sum(mano)
    # Ajustar ases (1 u 11)
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
def turno_jugador(mano, ronda_ganar=False):
    while True:
        mostrar_manos(mano, [0,0], ocultar=True)
        total = calcular_mano(mano)
        if total >= 21:
            break

        accion = input("¿Querés pedir carta (p) o plantarte (s)? ").lower()
        if accion == "p":
            if ronda_ganar:
                # Dar solo cartas que no superen 21
                posibles = [c for c in range(1,12) if total + c <= 21]
                carta = random.choice(posibles)
            else:
                carta = sacar_carta()
            print(f"Te salió un {carta}")
            mano.append(carta)
        else:
            break
    return mano

# Turno del crupier (con patrón amañado)
def turno_crupier(crupier, jugador_total, ronda_ganar=False):
    while True:
        crupier_total = calcular_mano(crupier)

        if ronda_ganar:
            # Jugador <=16 → crupier se pasa
            if jugador_total <= 16:
                posibles = [c for c in range(1,12) if crupier_total + c > 21]
                if posibles:
                    carta = random.choice(posibles)
                else:
                    # fallback: forzar bust
                    carta = 12
                crupier.append(carta)
                break

            # Jugador = 17 → crupier se pasa
            elif jugador_total == 17:
                posibles = [c for c in range(1,12) if crupier_total + c > 21]
                if posibles:
                    carta = random.choice(posibles)
                else:
                    carta = 12  # forzar bust
                crupier.append(carta)
                break

            # Jugador 18–21 → crupier planta 17–jugador_total sin superar
            elif 18 <= jugador_total <= 21:
                if crupier_total < 17:
                    # elegir un número entre 17 y jugador_total
                    diferencia = random.randint(17, jugador_total) - crupier_total
                    if 1 <= diferencia <= 11:
                        crupier.append(diferencia)
                    else:
                        # fallback seguro: forzar a 17
                        crupier.append(17 - crupier_total)
                elif crupier_total >= jugador_total:
                    # si ya superó o igualó → forzar 17
                    crupier = [17]
                break
        else:
            # Comportamiento normal
            if crupier_total < 17:
                crupier.append(sacar_carta())
            else:
                break

    return crupier


# Patrón de rondas amañadas
patron_rondas = [True, True, False, True, False, False, None, False, False, False]

def jugar():
    for i in range(10):
        print(f"\n===== RONDA {i+1} =====")

        # Ronda 4: Blackjack fijo
        if i+1 == 4:
            jugador = [10, 11]
            crupier = [sacar_carta(), sacar_carta()]
            mostrar_manos(jugador, crupier)
            print("Blackjack! Ganaste automáticamente ✅")
            continue

        ronda_ganar = patron_rondas[i] == True
        ronda_empate = patron_rondas[i] == None

        jugador = [sacar_carta(), sacar_carta()]
        crupier = [sacar_carta(), sacar_carta()]

        # Verificar blackjack inicial
        if sorted(jugador) == [1, 10]:
            mostrar_manos(jugador, crupier)
            print("Blackjack! Ganaste automáticamente ✅")
            continue

        # Turno jugador
        jugador = turno_jugador(jugador, ronda_ganar)
        jugador_total = calcular_mano(jugador)

        if jugador_total > 21:
            mostrar_manos(jugador, crupier)
            print("Te pasaste de 21. Perdiste ❌")
            continue

        # Turno crupier
        print("Turno del crupier:")
        crupier = turno_crupier(crupier, jugador_total, ronda_ganar)
        crupier_total = calcular_mano(crupier)
        mostrar_manos(jugador, crupier)

        # Determinar ganador
        if ronda_ganar:
            print("Ganaste la ronda ✅")
        else:
            if jugador_total > 21:
                print("Te pasaste de 21. Perdiste ❌")
            elif crupier_total > 21:
                print("El crupier se pasó. Ganaste ✅")
            elif jugador_total > crupier_total:
                print("Ganaste la ronda ✅")
            elif jugador_total < crupier_total:
                print("El crupier gana ❌")
            else:
                if ronda_empate:
                    print("Empate ⚖️")
                else:
                    print("Empate ⚖️")

if __name__ == "__main__":
    jugar()


