import os
import sys
import random
import traci
import RouteGenerator as RG

# Definir constantes descriptivas
FIVE_AM = 18000
EIGHT_AM = 28800
NINE_AM = 32400
ELEVEN_AM = 39600
MIDDAY = 43200
ONE_PM = 46800
TWO_PM = 50400
FIVE_PM = 61200
SIX_PM = 64800
SEVEN_PM = 68400
EIGHT_PM = 72000
NINE_PM = 75600
MIDNIGHT = 86400
TEN_MIN = 600
THIRTY_MIN = 1800
SIMULATION_DAYS = 1
MAXIMUM_CHARGE = 0.9  # 90% carga máxima
MAXIMUM_DOD = 0.7  # 80% descarga máxima (Depth of Discharge)
INITIAL_MASS = 4989.5161
EMISSION_CLASS = "MMPEVEM"  # Modelo de emisiones https://sumo.dlr.de/docs/Models/MMPEVEM.html

# Verificar entorno SUMO_HOME
if "SUMO_HOME" not in os.environ:
    sys.exit("Por favor, declara la variable de entorno 'SUMO_HOME'")

TOOLS_PATH = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(TOOLS_PATH)

# Configuración del comando de simulación
SUMO_CMD = ["sumo", "-c", "Pasto_Ruta_E2.sumocfg"]

def Handle_Charging(vehicle_id):
    """
    Gestiona la lógica de carga de los vehículos.

    Args:
        vehicle_id (str): ID del vehículo a evaluar.

    Returns:
        tuple: (estado de carga, capacidad actual de batería)
            - 'ChargingNeeded' si la batería está por debajo del umbral.
            - 'ChargingFull' si está completamente cargada.
            - 'Charged' si está en un estado intermedio.
    """
    current_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.actualBatteryCapacity"))
    max_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.maximumBatteryCapacity"))

    dod_threshold = max_capacity * (1 - MAXIMUM_DOD)
    full_threshold = max_capacity * MAXIMUM_CHARGE

    if current_capacity < dod_threshold:
        return 'ChargingNeeded', current_capacity / max_capacity
    elif current_capacity > full_threshold:
        return 'ChargingFull', current_capacity / max_capacity
    else:
        return 'Charged', current_capacity / max_capacity

def Bus_Needed(step):
    """
    Determina la cantidad de buses necesarios en función del tiempo actual (step).
    
    El tiempo se compara contra intervalos predefinidos que representan distintas franjas horarias del día.
    Cada franja tiene una demanda específica de buses. Si el paso de tiempo no se encuentra en ninguna franja,
    se asume que no se requiere ningún bus (retorna 0).

    Parámetros:
        step: valor que representa el tiempo actual (puede ser un entero o timestamp dependiendo de la implementación).

    Retorna:
        int: número de buses necesarios en la franja correspondiente.
    """
    schedule = [
        (FIVE_AM + THIRTY_MIN, NINE_AM, 7),
        (NINE_AM, ELEVEN_AM, 9),
        (ELEVEN_AM, TWO_PM, 13),
        (TWO_PM, FIVE_PM, 8),
        (FIVE_PM, EIGHT_PM, 10),
        (EIGHT_PM, NINE_PM + THIRTY_MIN, 8),
    ]

    for start, end, buses in schedule:
        if start <= step < end:
            return buses

    return 0


def Bus_Schedulling(step, vehicle_id):
    """
    Determina si un autobús específico debe estar activo (en operación) en un instante dado de la simulación.
    
    Cada autobús tiene asignados uno o más intervalos de tiempo durante los cuales está programado para operar.
    La función consulta una tabla de horarios predefinida y verifica si el tiempo actual (`step`) cae dentro de 
    alguno de esos intervalos. Si el autobús no está en la tabla, se asume que siempre está activo.
    
    Parámetros:
        step (int): Tiempo actual de la simulación en segundos.
        vehicle_id (str): Identificador del vehículo (e.g., 'Bus_01').

    Retorna:
        bool: True si el bus debe estar activo, False en caso contrario.
    """

    schedule = {
        'Bus_01': [(FIVE_AM + THIRTY_MIN, MIDDAY), (FIVE_PM, NINE_PM)],
        'Bus_02': [(FIVE_AM + THIRTY_MIN, MIDDAY), (FIVE_PM, NINE_PM)],
        'Bus_03': [(FIVE_AM + THIRTY_MIN, MIDDAY), (SEVEN_PM, NINE_PM)],
        'Bus_04': [(FIVE_AM + THIRTY_MIN, ONE_PM + THIRTY_MIN), (SEVEN_PM, NINE_PM)],
        'Bus_05': [(FIVE_AM + THIRTY_MIN, ONE_PM + THIRTY_MIN), (SEVEN_PM, NINE_PM)],
        'Bus_06': [(FIVE_AM + THIRTY_MIN, ONE_PM + THIRTY_MIN), (SEVEN_PM, NINE_PM)],
        'Bus_07': [(NINE_AM, ONE_PM + THIRTY_MIN), (SEVEN_PM, NINE_PM)],
        'Bus_08': [(NINE_AM, ONE_PM + THIRTY_MIN)],
        'Bus_09': [(ELEVEN_AM, SIX_PM + THIRTY_MIN)],
        'Bus_10': [(ELEVEN_AM, SIX_PM + THIRTY_MIN)],
        'Bus_11': [(ELEVEN_AM, SIX_PM + THIRTY_MIN)],
        'Bus_12': [(ELEVEN_AM, SIX_PM + THIRTY_MIN)],
        'Bus_13': [(MIDDAY, SIX_PM + THIRTY_MIN)],
        'Bus_14': [(MIDDAY, SEVEN_PM + THIRTY_MIN)],
        'Bus_15': [(MIDDAY, SEVEN_PM + THIRTY_MIN)],
    }

    intervals = schedule.get(vehicle_id)
    
    if intervals is None:
        return True  # Valor por defecto si el bus no tiene programación definida
    
    return any(start <= step < end for start, end in intervals)

def Get_Vehicle_Stops():
    """
    Obtiene el estado de parada y la carretera actual para una flota de 15 buses simulados en SUMO (vía TraCI).

    Retorna:
        dict: Diccionario con los estados de parada de cada bus, indexado por el nombre del vehículo.
              Ejemplo: {'Bus_01': stopState, 'Bus_02': stopState, ...}
    """
    stops = {}
    # edges = {}  # Descomenta si también quieres devolver el ID de carretera para cada bus

    for i in range(15):
        vehicle_id = f"Bus_{i+1:02d}"  # Bus_01, Bus_02, ..., Bus_15
        try:
            stops[vehicle_id] = traci.vehicle.getStopState(vehicle_id)
            # edges[vehicle_id] = traci.vehicle.getRoadID(vehicle_id)
        except traci.exceptions.TraCIException:
            # El vehículo puede no estar presente en el paso actual
            stops[vehicle_id] = None
            # edges[vehicle_id] = None

    return stops  # o return stops, edges si quieres devolver ambos

def Count_Buses_in_Route(stops_state, finish):
    """
    Cuenta cuántos buses están actualmente en ruta, es decir,
    no están detenidos y aún no han terminado su operación.

    Parámetros:
        stops_state (dict): Diccionario con el estado de parada de cada bus (0 significa en ruta).
        finish (dict): Diccionario booleano que indica si cada bus ha terminado su operación.

    Retorna:
        int: Número de buses actualmente en ruta.
    """
    bus_inRoute_counter = 0

    for i in range(15):
        vehicle_id = f"Bus_{i+1:02d}"
        if stops_state.get(vehicle_id) == 0 and not finish.get(vehicle_id, True):
            bus_inRoute_counter += 1

    return bus_inRoute_counter


def Run_Simulation(sumo_cmd, emission_class):
    """Ejecuta la simulación de vehículos eléctricos."""

    step = FIVE_AM
    day = 1
    finish = {}
    current_edges = {}
    stops_state = {}
    in_route = {}

    traci.start(sumo_cmd)

    for i in range(15):  # Del 0 al 14
        vehicle = f"Bus_{i+1:02d}"
        traci.vehicle.setEmissionClass(vehicle, emission_class)
        finish[vehicle] = True
    traci.simulationStep(FIVE_AM)

    while day <= SIMULATION_DAYS:
        traci.simulationStep()

        


        for i in range(15): 

            vehicle = f"Bus_{i+1:02d}"  # Nombres Bus_01, Bus_02, ..., Bus_06     

            stops_state = Get_Vehicle_Stops()
            in_route_buses = Count_Buses_in_Route(stops_state, finish)
            buses = Bus_Needed(step)

            # Verifica si es momento de asignar buses y si hay menos buses en ruta que los necesarios
            bus_available = (step % TEN_MIN == 0) and (in_route_buses < buses)

            current_edge = traci.vehicle.getRoadID(vehicle)
            charge, SoC = Handle_Charging(vehicle)
            if current_edge == "735027154":
                if charge == 'Charged' and not finish[vehicle]: 
                    traci.vehicle.setParkingAreaStop(vehicle, "Bus_ParkArea", duration=10, flags=1)
                finish[vehicle] = True
            if charge == 'ChargingNeeded':
                if traci.vehicle.getStopState(vehicle) != 67 and current_edge != '-48268326#1' and current_edge != '-48268326#0':
                    traci.vehicle.setChargingStationStop(vehicle, "Bus_CS_150kW", duration=10000, flags=1)
            elif charge == 'ChargingFull': 
                if traci.vehicle.getStopState(vehicle) == 67:
                    traci.vehicle.changeTarget(vehicle, '-48268326#0')
                    traci.vehicle.resume(vehicle)
                    traci.vehicle.setParkingAreaStop(vehicle, "Bus_ParkArea", duration=1000, flags=1)
            if finish[vehicle] and traci.vehicle.getStopState(vehicle) == 131 and charge != 'ChargingNeeded' and bus_available:
                traci.vehicle.setRouteID(vehicle, "Ruta_E2")
                traci.vehicle.resume(vehicle)  
                finish[vehicle] = False   
            elif finish[vehicle] and traci.vehicle.getStopState(vehicle) == 131 and charge == 'ChargingNeeded':
                traci.vehicle.changeTarget(vehicle, '-735027154')
                traci.vehicle.resume(vehicle)  
            elif finish[vehicle] and traci.vehicle.getStopState(vehicle) == 131 and charge != 'ChargingNeeded' and not bus_available:      
                if SoC >= 0.8: 
                    traci.vehicle.setParkingAreaStop(vehicle, "Bus_ParkArea", duration=3600, flags=1)
                else:
                    traci.vehicle.changeTarget(vehicle, '-735027154')
                    traci.vehicle.resume(vehicle)
                    traci.vehicle.setChargingStationStop(vehicle, "Bus_CS_150kW", duration=10000, flags=1)

        step += 1
        if step >= MIDNIGHT:
            step = 0
            day += 1

    traci.close()

    clean_up_files()

def clean_up_files():
    """Elimina archivos temporales generados durante la simulación."""
    try:
        os.remove("MorningRoutesJSON/TotalRoutes.json")
        os.remove("AfternoonRoutesJSON/TotalRoutes.json")
    except FileNotFoundError as e:
        print(f"Error eliminando archivo: {e}")

# Ejecución principal
if __name__ == "__main__":
    Run_Simulation(SUMO_CMD, EMISSION_CLASS)
