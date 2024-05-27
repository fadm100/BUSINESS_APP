def DeliveryStops(edgesList, dVE):
    names = []
    routes = []
    routesDic = {}
    for i in range(len(edgesList)-1):
        names.append("Ruta_VAN_" + str(i) + "DE_" + str(dVE))
        routes.append([edgesList[i], edgesList[i+1]])
    routesDic['names'] = names
    routesDic['routes'] = routes
    return routesDic