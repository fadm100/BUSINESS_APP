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
NINE_PM = 75600
MIDNIGHT = 86400
TEN_MIN = 600
THIRTY_MIN = 1800
SIMULATION_DAYS = 5
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

        
def Run_Simulation(sumo_cmd, emission_class):
    """Ejecuta la simulación de vehículos eléctricos."""

    step = FIVE_AM
    day = 1
    finish = {}

    traci.start(sumo_cmd)
    for i in range(15):  # Del 0 al 14
        vehicle = f"Bus_{i+1:02d}"
        traci.vehicle.setEmissionClass(vehicle, emission_class)
        finish[vehicle] = False
    traci.simulationStep(FIVE_AM)
    while day <= SIMULATION_DAYS:
        traci.simulationStep()

        for i in range(15): 
            vehicle = f"Bus_{i+1:02d}"  # Nombres Bus_01, Bus_02, ..., Bus_06
            if i < 6 and step == FIVE_AM + i * TEN_MIN:
                traci.vehicle.resume(vehicle)
            elif i >= 6 and i < 8 and step == NINE_AM + (i-6) * TEN_MIN:
                traci.vehicle.resume(vehicle)
            elif i >= 8 and i < 12 and step == ELEVEN_AM + (i-8) * TEN_MIN:
                traci.vehicle.resume(vehicle)
            elif i >= 12 and i <= 14 and step == MIDDAY + (i-12) * TEN_MIN:
                traci.vehicle.resume(vehicle)
            
            current_edge = traci.vehicle.getRoadID(vehicle)
            charge, SoC = Handle_Charging(vehicle)
            bus_available = Bus_Schedulling(step=step, vehicle_id=vehicle)
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
