"""
Juego de Blackjack simulado en Python con un crupier amañado.

Descripción:
Este código simula 10 rondas de Blackjack, donde el jugador puede pedir cartas o plantarse.
El crupier sigue un patrón amañado:
- Si el jugador tiene ≤16 o 17, el crupier se pasa (>21) sin tocar 17-21.
- Si el jugador tiene 18-21, el crupier puede plantarse entre 17 y su total,
  pero nunca superar el valor del jugador y puede pasarse.
El juego también maneja blackjack inicial (1+10) y una ronda fija de blackjack (ronda 4).
"""


import random  # Importa la librería random para generar cartas aleatorias

# Función que calcula el total de una mano de cartas
def calcular_mano(mano):
    total = sum(mano)  # Suma todos los valores de la mano
    ases = mano.count(1)  # Cuenta cuántos ases (1) hay en la mano
    while ases > 0 and total + 10 <= 21:  # Ajusta los ases a 11 si no se pasa de 21
        total += 10  # Suma 10 al total para que el as valga 11
        ases -= 1  # Reduce el contador de ases restantes por ajustar
    return total  # Devuelve el total calculado de la mano

# Función para mostrar las cartas del jugador y el crupier
def mostrar_manos(jugador, crupier, ocultar=False):
    if ocultar:  # Si ocultar es True, mostramos solo la primera carta del crupier
        print(f"Tus cartas: {jugador} = {calcular_mano(jugador)}")  # Muestra cartas del jugador
        print(f"Cartas del crupier: [{crupier[0]}, ?]")  # Muestra primera carta del crupier y oculta la segunda
    else:  # Si ocultar es False, mostramos todas las cartas
        print(f"Tus cartas: {jugador} = {calcular_mano(jugador)}")  # Muestra cartas del jugador
        print(f"Cartas del crupier: {crupier} = {calcular_mano(crupier)}")  # Muestra cartas del crupier

# Función para sacar una carta aleatoria
def sacar_carta():
    return random.choice([1,2,3,4,5,6,7,8,9,10,10,10,10])  # Devuelve un valor aleatorio (1-10, figuras valen 10)

# Función que maneja el turno del jugador
def turno_jugador(mano, ronda_ganar=False):
    while True:  # Bucle que se repite mientras el jugador siga pidiendo cartas
        mostrar_manos(mano, [0,0], ocultar=True)  # Muestra cartas con crupier oculto
        total = calcular_mano(mano)  # Calcula el total actual del jugador
        if total >= 21:  # Si llega a 21 o más, termina el turno
            break
        accion = input("¿Querés pedir carta (p) o plantarte (s)? ").lower()  # Pregunta acción al jugador
        if accion == "p":  # Si el jugador pide carta
            if ronda_ganar:  # Si es ronda amañada
                posibles = [c for c in range(1,12) if total + c <= 21]  # Lista cartas seguras para no pasarse
                carta = random.choice(posibles)  # Escoge una carta segura
            else:  # Ronda normal
                carta = sacar_carta()  # Carta aleatoria normal
            print(f"Te salió un {carta}")  # Muestra la carta obtenida
            mano.append(carta)  # Agrega la carta a la mano del jugador
        else:  # Si se planta
            break  # Termina el turno
    return mano  # Devuelve la mano final del jugador

# Función que maneja el turno del crupier siguiendo patrón amañado
def turno_crupier(crupier, jugador_total, ronda_ganar=False):
    while True:  # Bucle que se repite mientras el crupier deba actuar
        crupier_total = calcular_mano(crupier)  # Calcula el total del crupier
        if ronda_ganar:  # Comportamiento amañado si el jugador debe ganar
            if jugador_total <= 16:  # Si jugador ≤ 16
                posibles = [c for c in range(1,12) if crupier_total + c > 21]  # Cartas que hacen que crupier se pase
                carta = random.choice(posibles) if posibles else 12  # Escoge carta o forzar bust
                crupier.append(carta)  # Agrega carta a crupier
                break  # Termina turno crupier
            elif jugador_total == 17:  # Si jugador = 17
                posibles = [c for c in range(1,12) if crupier_total + c > 21]  # Cartas que hagan bust
                carta = random.choice(posibles) if posibles else 12  # Fallback si lista vacía
                crupier.append(carta)  # Agrega carta
                break  # Termina turno
            elif 18 <= jugador_total <= 21:  # Si jugador 18–21
                if crupier_total < 17:  # Si crupier < 17
                    diferencia = random.randint(17, jugador_total) - crupier_total  # Escoge carta que lo acerque a 17–jugador
                    if 1 <= diferencia <= 11:  # Si diferencia válida
                        crupier.append(diferencia)  # Añade carta
                    else:  # Si diferencia no válida
                        crupier.append(17 - crupier_total)  # Ajusta a 17
                elif crupier_total >= jugador_total:  # Si crupier ya iguala o supera jugador
                    crupier = [17]  # Forzar crupier a 17
                break  # Termina turno
        else:  # Comportamiento normal del crupier
            if crupier_total < 17:  # Si crupier < 17
                crupier.append(sacar_carta())  # Pide carta
            else:  # Si crupier ≥ 17
                break  # Se planta
    return crupier  # Devuelve la mano final del crupier

# Patrón de rondas amañadas
patron_rondas = [True, True, False, True, False, False, None, False, False, False]  # True=ganar, False=perder, None=empate posible

# Función principal que ejecuta todas las rondas
def jugar():
    for i in range(10):  # Itera 10 rondas
        print(f"\n===== RONDA {i+1} =====")  # Muestra número de ronda
        if i+1 == 4:  # Ronda 4 siempre Blackjack
            jugador = [10, 11]  # Blackjack fijo
            crupier = [sacar_carta(), sacar_carta()]  # Cartas crupier
            mostrar_manos(jugador, crupier)  # Mostrar manos
            print("Blackjack! Ganaste automáticamente ✅")  # Mensaje
            continue  # Pasar a la siguiente ronda

        ronda_ganar = patron_rondas[i] == True  # Define si la ronda está amañada para ganar
        ronda_empate = patron_rondas[i] == None  # Define si es posible empate

        jugador = [sacar_carta(), sacar_carta()]  # Reparte cartas al jugador
        crupier = [sacar_carta(), sacar_carta()]  # Reparte cartas al crupier

        if sorted(jugador) == [1, 10]:  # Blackjack inicial del jugador
            mostrar_manos(jugador, crupier)  # Muestra manos
            print("Blackjack! Ganaste automáticamente ✅")  # Mensaje
            continue  # Pasar a siguiente ronda

        jugador = turno_jugador(jugador, ronda_ganar)  # Ejecuta turno del jugador
        jugador_total = calcular_mano(jugador)  # Calcula total final del jugador

        if jugador_total > 21:  # Si se pasa de 21
            mostrar_manos(jugador, crupier)  # Muestra manos
            print("Te pasaste de 21. Perdiste ❌")  # Mensaje de pérdida
            continue  # Siguiente ronda

        print("Turno del crupier:")  # Mensaje
        crupier = turno_crupier(crupier, jugador_total, ronda_ganar)  # Turno crupier
        crupier_total = calcular_mano(crupier)  # Total crupier
        mostrar_manos(jugador, crupier)  # Muestra manos finales

        if ronda_ganar:  # Si la ronda está amañada
            print("Ganaste la ronda ✅")  # Mensaje de victoria
        else:  # Si es ronda normal
            if jugador_total > 21:  # Jugador se pasó
                print("Te pasaste de 21. Perdiste ❌")
            elif crupier_total > 21:  # Crupier se pasó
                print("El crupier se pasó. Ganaste ✅")
            elif jugador_total > crupier_total:  # Jugador gana
                print("Ganaste la ronda ✅")
            elif jugador_total < crupier_total:  # Crupier gana
                print("El crupier gana ❌")
            else:  # Empate
                if ronda_empate:  # Empate permitido
                    print("Empate ⚖️")
                else:
                    print("Empate ⚖️")

# Ejecuta el juego si el script se ejecuta directamente
if __name__ == "__main__":
    jugar()  # Llama a la función principal


