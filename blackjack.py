import random

def valor_mano(mano):
    total = 0
    ases = 0
    for carta in mano:
        if carta in ['J','Q','K']:
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

def mostrar_manos(jugador, crupier, oculto=True):
    if oculto:
        print(f"Crupier: [{crupier[0]}, ?]")
    else:
        print(f"Crupier: {crupier} (Total: {valor_mano(crupier)})")
    print(f"Jugador: {jugador} (Total: {valor_mano(jugador)})")

def carta_aleatoria():
    return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])

def es_blackjack(mano):
    return len(mano) == 2 and valor_mano(mano) == 21

def blackjack_ronda(ronda, ultima_ronda=False):
    print(f"\n--- Ronda {ronda} ---")

    # Configuración inicial según la ronda
    if ronda == 4:
        mano_jugador = ['A','K']  # Blackjack garantizado
        mano_crupier = [carta_aleatoria(), carta_aleatoria()]
        ronda_segura = False
    else:
        mano_jugador = [carta_aleatoria(), carta_aleatoria()]
        mano_crupier = [carta_aleatoria(), carta_aleatoria()]
        ronda_segura = ronda in [1,2]

    # --- Turno del jugador ---
    while True:
        mostrar_manos(mano_jugador, mano_crupier)
        jugador_total = valor_mano(mano_jugador)
        if jugador_total >= 21:
            break

        while True:
            decision = input("¿Quieres pedir carta o plantarte? (pedir/plantarse): ").lower()
            if decision in ['pedir','plantarse']:
                break
            print("Respuesta inválida. Escribe 'pedir' o 'plantarse'.")

        if decision == 'pedir':
            nueva = carta_aleatoria()
            if ronda_segura:
                for _ in range(100):
                    nueva = carta_aleatoria()
                    if valor_mano(mano_jugador + [nueva]) <= 21:
                        mano_jugador.append(nueva)
                        print(f"Jugador pide carta y recibe: {nueva}")
                        break
            else:
                mano_jugador.append(nueva)
                print(f"Jugador pide carta y recibe: {nueva}")
        else:
            print("Jugador se planta.")
            break

    jugador_total = valor_mano(mano_jugador)

    if jugador_total > 21:
        mostrar_manos(mano_jugador, mano_crupier, oculto=False)
        print("¡Jugador se pasa! El crupier gana.")
        return

    # --- Turno del crupier ---
    crupier_total = valor_mano(mano_crupier)
    while crupier_total < 17:
        nueva = carta_aleatoria()
        mano_crupier.append(nueva)
        crupier_total = valor_mano(mano_crupier)
        print(f"Crupier pide carta y recibe: {nueva}")

    if crupier_total > 21:
        mostrar_manos(mano_jugador, mano_crupier, oculto=False)
        print("¡Crupier se pasa! Jugador gana.")
        return

    # --- Mostrar manos finales ---
    mostrar_manos(mano_jugador, mano_crupier, oculto=False)

    # --- Notificar Blackjack si hay ---
    if es_blackjack(mano_jugador):
        print("¡Jugador obtiene Blackjack!")
    if es_blackjack(mano_crupier):
        print("¡Crupier obtiene Blackjack!")

    # --- Determinar ganador según ronda ---
    if ronda_segura or ronda == 4:
        print("¡Jugador gana!")
    elif ronda == 3:
        # Forzar que crupier supere al jugador sin pasarse
        while valor_mano(mano_crupier) <= valor_mano(mano_jugador) and valor_mano(mano_crupier) < 21:
            nueva = carta_aleatoria()
            mano_crupier.append(nueva)
            crupier_total = valor_mano(mano_crupier)
            print(f"Crupier pide carta adicional para ganar y recibe: {nueva}")
        mostrar_manos(mano_jugador, mano_crupier, oculto=False)
        print("¡Crupier gana!")
    elif ronda >= 5 and not ultima_ronda:
        print("¡Crupier gana!")
    elif ultima_ronda:
        if jugador_total > crupier_total:
            print("¡Jugador gana!")
        elif jugador_total < crupier_total:
            print("¡Crupier gana!")
        else:
            print("¡Empate!")

def jugar_blackjack():
    num_rondas = 9
    for ronda in range(1, num_rondas+1):
        ultima = (ronda == num_rondas)
        blackjack_ronda(ronda, ultima_ronda=ultima)

if __name__ == "__main__":
    jugar_blackjack()

