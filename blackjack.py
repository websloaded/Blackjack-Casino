import random  # Importa la librería random para generar cartas al azar.

def valor_mano(mano):  # Define función que calcula el valor de una mano.
    total = 0  # Inicializa el total de puntos en 0.
    ases = 0   # Contador de Ases para manejarlos como 1 o 11.
    for carta in mano:  # Recorre cada carta en la mano.
        if carta in ['J', 'Q', 'K']:  # Si la carta es J, Q o K.
            total += 10  # Suma 10 puntos.
        elif carta == 'A':  # Si la carta es un As.
            total += 11  # Cuenta el As como 11 inicialmente.
            ases += 1  # Aumenta el contador de Ases.
        else:  # Si es una carta numérica.
            total += int(carta)  # Convierte la carta en número y la suma.
    while total > 21 and ases:  # Si la suma pasa de 21 y hay Ases.
        total -= 10  # Convierte un As de 11 a 1 restando 10.
        ases -= 1  # Reduce el número de Ases restantes.
    return total  # Devuelve el valor final de la mano.

def es_blackjack(mano):  # Función que comprueba si hay Blackjack.
    return len(mano) == 2 and valor_mano(mano) == 21  # Devuelve True si hay 21 con 2 cartas.

def mostrar_manos(jugador, crupier, oculto=True):  # Función que muestra cartas.
    if oculto:  # Si el crupier debe ocultar una carta.
        print(f"Crupier: [{crupier[0]}, ?]")  # Muestra solo la primera carta del crupier.
    else:  # Si debe mostrar todas las cartas.
        print(f"Crupier: {crupier} (Total: {valor_mano(crupier)})")  # Muestra toda la mano y su valor.
    print(f"Jugador: {jugador} (Total: {valor_mano(jugador)})")  # Siempre muestra la mano del jugador.

def carta_aleatoria():  # Función que genera una carta aleatoria.
    return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])  # Elige carta al azar.

def blackjack_ronda(ronda):  # Función que maneja una ronda del juego.
    mano_jugador = [carta_aleatoria(), carta_aleatoria()]  # Reparte 2 cartas al jugador.
    mano_crupier = [carta_aleatoria(), carta_aleatoria()]  # Reparte 2 cartas al crupier.

    gana_jugador = ((ronda - 1) // 2) % 2 == 0  # Determina si debe ganar jugador según el patrón.

    if es_blackjack(mano_jugador) or es_blackjack(mano_crupier):  # Comprueba Blackjack inicial.
        mostrar_manos(mano_jugador, mano_crupier, oculto=False)  # Muestra todas las cartas.
        if es_blackjack(mano_jugador) and es_blackjack(mano_crupier):  # Si ambos tienen Blackjack.
            print("¡Ambos tienen Blackjack! Empate.")  # Mensaje de empate.
        elif es_blackjack(mano_jugador):  # Si solo el jugador tiene Blackjack.
            print("¡Jugador gana con Blackjack!")  # Jugador gana.
        else:  # Si solo el crupier tiene Blackjack.
            print("¡Crupier gana con Blackjack!")  # Crupier gana.
        return  # Termina la ronda.

    while True:  # Bucle para el turno del jugador.
        mostrar_manos(mano_jugador, mano_crupier)  # Muestra cartas del jugador y crupier (oculto).
        if valor_mano(mano_jugador) >= 21:  # Si el jugador llega a 21 o más.
            break  # Termina su turno.
        decision = input("¿Quieres pedir carta? (s/n): ").lower()  # Pregunta si pide carta.
        if decision == 's':  # Si responde que sí.
            mano_jugador.append(carta_aleatoria())  # Añade nueva carta al jugador.
        else:  # Si responde que no.
            break  # Se planta.

    jugador_total = valor_mano(mano_jugador)  # Calcula el total del jugador.

    crupier_total = valor_mano(mano_crupier)  # Calcula el total inicial del crupier.
    while crupier_total < 17:  # Mientras el crupier tenga menos de 17.
        mano_crupier.append(carta_aleatoria())  # Pide una nueva carta.
        crupier_total = valor_mano(mano_crupier)  # Recalcula su total.

    if gana_jugador:  # Si esta ronda debe ganar el jugador.
        if jugador_total <= crupier_total and jugador_total <= 21:  # Si jugador no va ganando.
            while jugador_total <= crupier_total and jugador_total < 21:  # Fuerza ventaja.
                mano_jugador.append(carta_aleatoria())  # Añade carta al jugador.
                jugador_total = valor_mano(mano_jugador)  # Recalcula puntos.
    else:  # Si esta ronda debe ganar el crupier.
        if crupier_total <= jugador_total and jugador_total < 21 and crupier_total < 21:  # Si no va ganando.
            while crupier_total <= jugador_total and crupier_total < 21:  # Fuerza ventaja.
                mano_crupier.append(carta_aleatoria())  # Añade carta al crupier.
                crupier_total = valor_mano(mano_crupier)  # Recalcula puntos.

    mostrar_manos(mano_jugador, mano_crupier, oculto=False)  # Muestra todas las cartas al final.

    if jugador_total > 21:  # Si jugador se pasa de 21.
        print("¡Jugador se pasa! Crupier gana.")  # Crupier gana.
    elif crupier_total > 21:  # Si crupier se pasa de 21.
        print("¡Crupier se pasa! Jugador gana.")  # Jugador gana.
    elif jugador_total > crupier_total:  # Si jugador tiene más puntos.
        print("¡Jugador gana!")  # Jugador gana.
    elif jugador_total < crupier_total:  # Si crupier tiene más puntos.
        print("¡Crupier gana!")  # Crupier gana.
    else:  # Si empatan en puntos.
        print("¡Empate!")  # Empate.

def jugar_blackjack():  # Función principal del juego.
    num_rondas = 8  # Número de rondas a jugar.
    for ronda in range(1, num_rondas + 1):  # Recorre todas las rondas.
        print(f"\n--- Ronda {ronda} ---")  # Muestra el número de la ronda.
        blackjack_ronda(ronda)  # Ejecuta una ronda.

if __name__ == "__main__":  # Comprueba si el archivo es el principal.
    jugar_blackjack()  # Ejecuta el juego completo.

