import os
import sys
import random
import traci
import RouteGenerator as RG

# Definir constantes descriptivas
EIGHT_AM = 28800
MIDDAY = 43200
TWO_PM = 50400
SIX_PM = 64800
MIDNIGHT = 86400
SIMULATION_DAYS = 5
MAXIMUM_CHARGE = 0.8  # 80% carga máxima
MAXIMUM_DOD = 0.8  # 80% descarga máxima (Depth of Discharge)
INITIAL_MASS = 4989.5161
EMISSION_CLASS = "MMPEVEM"  # Modelo de emisiones https://sumo.dlr.de/docs/Models/MMPEVEM.html

# Verificar entorno SUMO_HOME
if "SUMO_HOME" not in os.environ:
    sys.exit("Por favor, declara la variable de entorno 'SUMO_HOME'")

TOOLS_PATH = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(TOOLS_PATH)

# Configuración del comando de simulación
SUMO_CMD = ["sumo", "-c", "TestVan.sumocfg"]

# Rutas de los archivos JSON
MORNING_ROUTES_JSON = [
    "MorningRoutesJSON/DE_520001_Route.json",
    "MorningRoutesJSON/DE_520002_Route.json",
    "MorningRoutesJSON/DE_520003_Route.json",
    "MorningRoutesJSON/DE_520004_Route.json",
    "MorningRoutesJSON/DE_520006_Route.json",
    "MorningRoutesJSON/DE_520010_Route.json",
]

AFTERNOON_ROUTES_JSON = [
    "AfternoonRoutesJSON/DE_520001_Route.json",
    "AfternoonRoutesJSON/DE_520002_Route.json",
    "AfternoonRoutesJSON/DE_520003_Route.json",
    "AfternoonRoutesJSON/DE_520004_Route.json",
    "AfternoonRoutesJSON/DE_520006_Route.json",
    "AfternoonRoutesJSON/DE_520010_Route.json",
]

def load_fleet_routes(session):
    """Carga las rutas de la flota según la sesión (AM o PM)."""
    if session == "AM":
        return RG.DeliveryRoutes(MORNING_ROUTES_JSON, session)
    elif session == "PM":
        return RG.DeliveryRoutes(AFTERNOON_ROUTES_JSON, session)
    else:
        raise ValueError("Sesión no válida. Usa 'AM' o 'PM'.")

def manage_vehicle(step, vehicle_index, charge_flags, vehicle_names, fleet_routes):
    """Gestiona el estado y operaciones de un vehículo durante la simulación."""
    vehicle_id = vehicle_names[vehicle_index]
    try:
        current_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.actualBatteryCapacity"))
        max_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.maximumBatteryCapacity"))
        charge_stop = current_capacity < max_capacity * (1 - MAXIMUM_DOD)
        battery_full = current_capacity > max_capacity * MAXIMUM_CHARGE

        if traci.vehicle.isStoppedParking(vehicle_id) and step in [EIGHT_AM, TWO_PM]:
            handle_delivery_start(vehicle_id, fleet_routes)
        
        elif traci.vehicle.getRoadID(vehicle_id) == fleet_routes[vehicle_id][1] and len(fleet_routes[vehicle_id]) > 1:
            handle_next_delivery(vehicle_id, fleet_routes)

        if charge_stop:
            handle_charging(vehicle_id, charge_flags, vehicle_index, battery_full)

    except Exception as e:
        print(f"Error gestionando el vehículo {vehicle_id}: {e}")

def handle_delivery_start(vehicle_id, fleet_routes):
    """Inicia la entrega desde el área de estacionamiento."""
    traci.vehicle.setParkingAreaStop(vehicle_id, "ParkAreaA", duration=10, until=EIGHT_AM)
    traci.vehicle.changeTarget(vehicle_id, fleet_routes[vehicle_id][1])

def handle_next_delivery(vehicle_id, fleet_routes):
    """Avanza al siguiente punto de entrega."""
    del fleet_routes[vehicle_id][1]
    new_target = fleet_routes[vehicle_id][1]
    traci.vehicle.changeTarget(vehicle_id, new_target)
    stop_time = random.randint(60, 600)
    traci.vehicle.setStop(vehicle_id, new_target, 0.1, stop_time=stop_time)

def handle_charging(vehicle_id, charge_flags, vehicle_index, battery_full):
    """Gestiona la lógica de carga de los vehículos."""
    if not battery_full:
        traci.vehicle.setChargingStationStop(vehicle_id, "cS_2to19_0a", duration=10)
        charge_flags[vehicle_index] = 1
    elif battery_full:
        traci.vehicle.setParkingAreaStop(vehicle_id, "ParkAreaA", duration=MIDNIGHT)
        charge_flags[vehicle_index] = 0

def run_simulation(sumo_cmd, emission_class):
    """Ejecuta la simulación de vehículos eléctricos."""
    charge_flags = [0] * len(MORNING_ROUTES_JSON)
    fleet_routes_am = load_fleet_routes("AM")
    fleet_routes_pm = load_fleet_routes("PM")
    vehicle_names = list(fleet_routes_am.keys())
    step = 0
    day = 1

    traci.start(sumo_cmd)

    for vehicle in vehicle_names:
        traci.vehicle.add(vehicle, "ParkingReturn", "VAN")
        traci.vehicle.setEmissionClass(vehicle, emission_class)
        traci.vehicle.setParkingAreaStop(vehicle, "ParkAreaA", duration=MIDNIGHT)

    while day <= SIMULATION_DAYS:
        traci.simulationStep()
        current_routes = fleet_routes_am if step < MIDDAY else fleet_routes_pm

        for i, _ in enumerate(vehicle_names):
            manage_vehicle(step, i, charge_flags, vehicle_names, current_routes)

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
    run_simulation(SUMO_CMD, EMISSION_CLASS)
