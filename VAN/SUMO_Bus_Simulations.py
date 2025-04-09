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
MAXIMUM_CHARGE = 0.9  # 90% carga máxima
MAXIMUM_DOD = 0.8  # 80% descarga máxima (Depth of Discharge)
INITIAL_MASS = 4989.5161
EMISSION_CLASS = "MMPEVEM"  # Modelo de emisiones https://sumo.dlr.de/docs/Models/MMPEVEM.html

# Verificar entorno SUMO_HOME
if "SUMO_HOME" not in os.environ:
    sys.exit("Por favor, declara la variable de entorno 'SUMO_HOME'")

TOOLS_PATH = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(TOOLS_PATH)

# Configuración del comando de simulación
SUMO_CMD = ["sumo-gui", "-c", "Pasto_Ruta_E2.sumocfg"]

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

def handle_charging(vehicle_id):
    """Gestiona la lógica de carga de los vehículos."""
    current_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.actualBatteryCapacity"))
    max_capacity = float(traci.vehicle.getParameter(vehicle_id, "device.battery.maximumBatteryCapacity"))
    charge_stop = current_capacity < max_capacity * (1 - MAXIMUM_DOD)
    battery_full = current_capacity > max_capacity * MAXIMUM_CHARGE
    charging_station = traci.vehicle.getParameter(vehicle_id, "device.battery.chargingStationId")
    if charge_stop:
        print(vehicle_id, current_capacity)
        # traci.vehicle.setParameter(vehicle_id, "device.battery.actualBatteryCapacity", battery_full)
        traci.vehicle.setChargingStationStop(vehicle_id, "Bus_CS_200kW", duration=1000000)
        output = True
    elif battery_full:
        traci.vehicle.setParkingAreaStop(vehicle_id, "Bus_ParkArea", duration=10000)
        output = False
    elif charging_station == "Bus_CS_200kW":
        output = True
    else:
        output = False

    return output
    # if not battery_full:
    #     traci.vehicle.setChargingStationStop(vehicle_id, "cS_2to19_0a", duration=10)
    #     charge_flags[vehicle_index] = 1
    # elif battery_full:
    #     traci.vehicle.setParkingAreaStop(vehicle_id, "ParkAreaA", duration=MIDNIGHT)
    #     charge_flags[vehicle_index] = 0

def run_simulation(sumo_cmd, emission_class):
    """Ejecuta la simulación de vehículos eléctricos."""

    step = 0
    day = 1
    finish = {}

    traci.start(sumo_cmd)
    for i in range(15):  # Del 0 al 14
        vehicle = f"Bus_{i+1:02d}"
        traci.vehicle.setEmissionClass(vehicle, emission_class)
        finish[vehicle] = False

    while day <= SIMULATION_DAYS:
        traci.simulationStep()

        five_am = 18000
        nine_am = 32400
        eleven_am = 39600
        twelve_am = 43200
        ten_min = 600

        for i in range(5): 
            vehicle = f"Bus_{i+1:02d}"  # Nombres Bus_01, Bus_02, ..., Bus_06
            if i < 6 and step == five_am + i * ten_min:
                traci.vehicle.resume(vehicle)
            elif i < 8 and step == nine_am + (i-6) * ten_min:
                traci.vehicle.resume(vehicle)
            elif i < 12 and step == eleven_am + (i-8) * ten_min:
                traci.vehicle.resume(vehicle)
            elif i <= 14 and step == twelve_am + (i-12) * ten_min:
                traci.vehicle.resume(vehicle)
            
            current_edge = traci.vehicle.getRoadID(vehicle)
            if current_edge == "735027154":#"-48268326#1": 
                finish[vehicle] = True
                traci.vehicle.setParkingAreaStop(vehicle, "Bus_ParkArea", duration=10000)
            if finish[vehicle] and traci.vehicle.isStoppedParking(vehicle) and not handle_charging(vehicle):
                traci.vehicle.setRouteID(vehicle, "Ruta_E2")
                traci.vehicle.resume(vehicle)
                finish[vehicle] = False

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
