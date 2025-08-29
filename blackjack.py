import random

# Valores de las cartas
valores = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

cartas = list(valores.keys()) * 4

def valor_mano(mano):
    total = sum(valores[c] for c in mano)
    ases = mano.count('A')
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

def dar_carta():
    return random.choice(cartas)


def jugar_blackjack():
    for ronda in range(1, 11):
        print(f"\n--- Ronda {ronda} ---")
        jugador = [dar_carta(), dar_carta()]
        crupier = [dar_carta(), '?']

        while True:
            total_jugador = valor_mano(jugador)
            print(f"Crupier: [{crupier[0]}, ?]")
            print(f"Jugador: {jugador} (Total: {total_jugador})")

            if total_jugador >= 21:
                break

            decision = input("¿Quieres pedir carta o plantarte? (pedir/plantarse): ").strip().lower()
            if decision == 'pedir':
                nueva = dar_carta()
                jugador.append(nueva)
                print(f"Jugador pide carta y recibe: {nueva}")
            else:
                print("Jugador se planta.")
                break

        total_jugador = valor_mano(jugador)

        # Lógica según ronda
        if ronda in [1, 2]:
            # Jugador gana siempre
            total_crupier = random.randint(15, total_jugador - 1)
            crupier = [dar_carta(), dar_carta()]
            while valor_mano(crupier) != total_crupier:
                crupier[1] = dar_carta()
                total_crupier = valor_mano(crupier)
            print(f"Crupier: {crupier} (Total: {total_crupier})")
            print(f"Jugador: {jugador} (Total: {total_jugador})")
            print("¡Jugador gana!")

        elif ronda == 3:
            # Crupier gana sí o sí
            if total_jugador >= 20:
                total_crupier = 21
            else:
                total_crupier = total_jugador + 1
            crupier = [dar_carta(), dar_carta()]
            while valor_mano(crupier) != total_crupier:
                crupier[1] = dar_carta()
            print(f"Crupier: {crupier} (Total: {total_crupier})")
            print(f"Jugador: {jugador} (Total: {total_jugador})")
            print("¡Crupier gana!")

        elif ronda == 4:
            # Blackjack del jugador
            jugador = ['A', random.choice(['10', 'J', 'Q', 'K'])]
            total_jugador = 21
            total_crupier = random.randint(15, 20)
            crupier = [dar_carta(), dar_carta()]
            print(f"Crupier: {crupier} (Total: {total_crupier})")
            print(f"Jugador: {jugador} (Total: {total_jugador})")
            print("¡Jugador obtiene Blackjack!")
            print("¡Jugador gana!")

        elif ronda in [5, 6, 7, 9, 10]:
            # Crupier gana siempre, jugador no toca 21
            if total_jugador >= 20:
                total_jugador = 19
            if total_jugador < 21:
                total_crupier = total_jugador + 1
            else:
                total_crupier = random.randint(17, 21)
            crupier = [dar_carta(), dar_carta()]
            while valor_mano(crupier) != total_crupier:
                crupier[1] = dar_carta()
            print(f"Crupier: {crupier} (Total: {total_crupier})")
            print(f"Jugador: {jugador} (Total: {total_jugador})")
            print("¡Crupier gana!")

        elif ronda == 8:
            # Empate
            total_jugador = random.choice([18, 19, 20, 21])
            total_crupier = total_jugador
            crupier = [dar_carta(), dar_carta()]
            print(f"Crupier: {crupier} (Total: {total_crupier})")
            print(f"Jugador: {jugador} (Total: {total_jugador})")
            print("¡Empate!")


# Ejecutar
jugar_blackjack()


