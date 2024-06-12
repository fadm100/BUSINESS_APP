import json

def DeliveryStops(edgesList, session, nVE): 
    '''edgeList are the edges where the routes 
    end and nVE is the name of the vehicle 
    that will travel the route.'''
    routes = []
    for i in range(len(edgesList)-1):
        item = []
        item.append("Ruta_" + str(i) + "_" + session + "_" + nVE)
        item.append([edgesList[i], edgesList[i+1]])
        routes.append(item)
    return routes

def DeliveryRoutes(routesJSON, session):
    vehicleNames = []
    routesDic = {}
    for i in range(len(routesJSON)):
        vehicleNames.append("Delivery_" + str(i))
        with open(routesJSON[i]) as json_file:
            deliveryRoute = json.load(json_file)
        routesDic[vehicleNames[i]] = DeliveryStops(deliveryRoute, session, vehicleNames[i])
    
    if session == 'AM':
        with open('MorningRoutesJSON/TotalRoutes.json', 'w') as outfile:
            json.dump(routesDic, outfile)
    else:
        with open('AfternoonRoutesJSON/TotalRoutes.json', 'w') as outfile:
            json.dump(routesDic, outfile)
        
    return routesDic

# routesJSON = ['RoutesJSON/DE_520001_Route.json', 'RoutesJSON/DE_520002_Route.json', 'RoutesJSON/DE_520010_Route.json']
# fleetRoutes = DeliveryRoutes(routesJSON)
# print(len(fleetRoutes["Delivery_0"]))