import random

def valor_mano(mano):
    total = 0
    ases = 0
    for carta in mano:
        if carta in ['J', 'Q', 'K']:
            total += 10
        elif carta == 'A':
            total += 11
            ases += 1
        else:
            total += int(carta)
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

def es_blackjack(mano):
    """Devuelve True si la mano inicial es un Blackjack (21 con dos cartas)."""
    return len(mano) == 2 and valor_mano(mano) == 21

def mostrar_manos(jugador, crupier, oculto=True):
    if oculto:
        print(f"Crupier: [{crupier[0]}, ?]")
    else:
        print(f"Crupier: {crupier} (Total: {valor_mano(crupier)})")
    print(f"Jugador: {jugador} (Total: {valor_mano(jugador)})")

def carta_aleatoria():
    return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])

def blackjack_ronda(ronda):
    mano_jugador = [carta_aleatoria(), carta_aleatoria()]
    mano_crupier = [carta_aleatoria(), carta_aleatoria()]

    # Patrón: 2 jugador, 2 crupier
    gana_jugador = ((ronda - 1) // 2) % 2 == 0

    # Revisar Blackjack inicial
    if es_blackjack(mano_jugador) or es_blackjack(mano_crupier):
        mostrar_manos(mano_jugador, mano_crupier, oculto=False)
        if es_blackjack(mano_jugador) and es_blackjack(mano_crupier):
            print("¡Ambos tienen Blackjack! Empate.")
        elif es_blackjack(mano_jugador):
            print("¡Jugador gana con Blackjack!")
        else:
            print("¡Crupier gana con Blackjack!")
        return

    # Turno del jugador
    while True:
        mostrar_manos(mano_jugador, mano_crupier)
        if valor_mano(mano_jugador) >= 21:
            break
        decision = input("¿Quieres pedir carta? (s/n): ").lower()
        if decision == 's':
            mano_jugador.append(carta_aleatoria())
        else:
            break

    jugador_total = valor_mano(mano_jugador)

    # Turno normal del crupier (pide hasta 17 o más)
    crupier_total = valor_mano(mano_crupier)
    while crupier_total < 17:
        mano_crupier.append(carta_aleatoria())
        crupier_total = valor_mano(mano_crupier)

    # Ajuste mínimo para respetar el patrón (solo si no hay Blackjack antes)
    if gana_jugador:
        if jugador_total <= crupier_total and jugador_total <= 21:
            # Forzar que el jugador tenga ventaja
            while jugador_total <= crupier_total and jugador_total < 21:
                mano_jugador.append(carta_aleatoria())
                jugador_total = valor_mano(mano_jugador)
    else:
        if crupier_total <= jugador_total and jugador_total < 21 and crupier_total < 21:
            while crupier_total <= jugador_total and crupier_total < 21:
                mano_crupier.append(carta_aleatoria())
                crupier_total = valor_mano(mano_crupier)

    # Mostrar manos finales
    mostrar_manos(mano_jugador, mano_crupier, oculto=False)

    # Determinar ganador
    if jugador_total > 21:
        print("¡Jugador se pasa! Crupier gana.")
    elif crupier_total > 21:
        print("¡Crupier se pasa! Jugador gana.")
    elif jugador_total > crupier_total:
        print("¡Jugador gana!")
    elif jugador_total < crupier_total:
        print("¡Crupier gana!")
    else:
        print("¡Empate!")

def jugar_blackjack():
    num_rondas = 8  # Cambiar número de rondas
    for ronda in range(1, num_rondas + 1):
        print(f"\n--- Ronda {ronda} ---")
        blackjack_ronda(ronda)

if __name__ == "__main__":
    jugar_blackjack()
