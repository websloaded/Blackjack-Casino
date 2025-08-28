import random

# Funciones de apoyo
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

def es_blackjack(mano):
    return len(mano) == 2 and valor_mano(mano) == 21

def mostrar_manos(jugador, crupier, oculto=True):
    if oculto:
        print(f"Crupier: [{crupier[0]}, ?]")
    else:
        print(f"Crupier: {crupier} (Total: {valor_mano(crupier)})")
    print(f"Jugador: {jugador} (Total: {valor_mano(jugador)})")

def carta_aleatoria():
    return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])

# Lógica de cada ronda
def blackjack_ronda(ronda):
    print(f"\n--- Ronda {ronda} ---")

    # Configuración de manos
    if ronda == 4:
        mano_jugador = ['A','K']  # Blackjack garantizado
        mano_crupier = [carta_aleatoria(), carta_aleatoria()]
        ronda_segura = False
    else:
        mano_jugador = [carta_aleatoria(), carta_aleatoria()]
        mano_crupier = [carta_aleatoria(), carta_aleatoria()]
        ronda_segura = ronda in [1,2]

    # Turno jugador
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
            for _ in range(100):
                nueva = carta_aleatoria()
                total_temporal = valor_mano(mano_jugador + [nueva])
                if ronda_segura and total_temporal <= 21:
                    mano_jugador.append(nueva)
                    print(f"Jugador pide carta y recibe: {nueva}")
                    break
                elif ronda in [3,5,6,7,9,10] and total_temporal < 21:
                    mano_jugador.append(nueva)
                    print(f"Jugador pide carta y recibe: {nueva}")
                    break
                elif ronda == 8:
                    mano_jugador.append(nueva)
                    print(f"Jugador pide carta y recibe: {nueva}")
                    break
        else:
            print("Jugador se planta.")
            break

    jugador_total = valor_mano(mano_jugador)

    # Turno crupier
    crupier_total = valor_mano(mano_crupier)
    if ronda in [3,5,6,7,9,10]:
        while crupier_total <= jugador_total:
            for _ in range(100):
                nueva = carta_aleatoria()
                if valor_mano(mano_crupier + [nueva]) <= 21:
                    mano_crupier.append(nueva)
                    crupier_total = valor_mano(mano_crupier)
                    print(f"Crupier pide carta y recibe: {nueva}")
                    break
    else:
        while crupier_total < 17:
            nueva = carta_aleatoria()
            mano_crupier.append(nueva)
            crupier_total = valor_mano(mano_crupier)
            print(f"Crupier pide carta y recibe: {nueva}")

    mostrar_manos(mano_jugador, mano_crupier, oculto=False)

    # Notificación de blackjack
    if es_blackjack(mano_jugador):
        print("¡Jugador obtiene Blackjack!")
    if es_blackjack(mano_crupier):
        print("¡Crupier obtiene Blackjack!")

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

# Juego completo
def jugar_blackjack():
    for ronda in range(1,11):
        blackjack_ronda(ronda)

if __name__ == "__main__":
    jugar_blackjack()
