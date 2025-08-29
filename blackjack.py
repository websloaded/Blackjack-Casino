import random

# Función para calcular la suma de las cartas
def calcular_mano(mano):
    total = sum(mano)
    # Ajustar ases (1 o 11)
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

# Función para sacar una carta aleatoria (1-11)
def sacar_carta():
    return random.choice([1,2,3,4,5,6,7,8,9,10,10,10,10])

# Turno del jugador
def turno_jugador(mano, ronda_ganar=False):
    while True:
        mostrar_manos(mano, [0, 0], ocultar=True)
        total = calcular_mano(mano)
        
        if ronda_ganar and total == 21:
            print("Has llegado a 21! Ganas automáticamente ✅")
            return mano, True
        
        if total >= 21:
            return mano, False
        
        accion = input("¿Querés pedir carta (p) o plantarte (s)? ").lower()
        if accion == "p":
            if ronda_ganar:
                # Elegir solo cartas que no pasen de 21
                posibles = [c for c in range(1,12) if total + c <= 21]
                if not posibles:
                    print("No hay cartas seguras para pedir, te plantas automáticamente.")
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
def turno_crupier(crupier, jugador_total, jugador_mano, ronda_ganar=False):
    while True:
        crupier_total = calcular_mano(crupier)
        jugador_actual = jugador_total
        # Si el jugador tiene menos de 17
        if jugador_total < 17:
            # El crupier no puede tocar 17-21
            posibles = [c for c in range(1,12) if not (17 <= crupier_total+c <= 21)]
            if not posibles:
                print("No hay cartas seguras, el crupier se pasa automáticamente y pierde ✅")
                crupier_total = 22
                break
            carta = random.choice(posibles)
        else:
            # Jugador 18-21
            posibles = [c for c in range(1,12) if crupier_total+c <= jugador_total]
            if not posibles:
                crupier_total = 22
                break
            carta = random.choice(posibles)
        crupier.append(carta)
        crupier_total = calcular_mano(crupier)
        if crupier_total > 21:
            print(f"El crupier se pasa de 21 con {crupier} = {crupier_total}")
            break
        if crupier_total >= 17 and crupier_total <= 21:
            if ronda_ganar and crupier_total >= jugador_total:
                crupier_total = 22
            break
    return crupier

# Patrón de rondas: True si jugador debe ganar, False si pierde, None si empate posible
patron_rondas = [True, True, False, True, False, False, None, False, False, False]

def jugar():
    for i in range(10):
        print(f"\n===== RONDA {i+1} =====")
        jugador = [sacar_carta(), sacar_carta()]
        crupier = [sacar_carta(), sacar_carta()]
        ronda_ganar = patron_rondas[i] == True
        ronda_empate = patron_rondas[i] == None
        
        # Turno jugador
        jugador, auto_ganar = turno_jugador(jugador, ronda_ganar)
        jugador_total = calcular_mano(jugador)
        if auto_ganar:
            crupier_total = calcular_mano(crupier)
            print("Turno del crupier:")
            crupier = turno_crupier(crupier, jugador_total, jugador, ronda_ganar)
            mostrar_manos(jugador, crupier)
            print("Ganaste la ronda ✅")
            continue
        
        # Turno crupier
        print("Turno del crupier:")
        crupier = turno_crupier(crupier, jugador_total, jugador, ronda_ganar)
        crupier_total = calcular_mano(crupier)
        mostrar_manos(jugador, crupier)
        
        # Determinar ganador
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
                if ronda_ganar:
                    print("Ganaste la ronda ✅")
                else:
                    print("El crupier gana ❌")

if __name__ == "__main__":
    jugar()
