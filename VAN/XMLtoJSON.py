
# import  jpype     
# import  asposecells     
# jpype.startJVM() 
# from asposecells.api import Workbook
# workbook = Workbook("Battery.out.xml")
# workbook.save("BatteryOut.json")
# jpype.shutdownJVM()

# Program to convert an xml
# file to json file

##########################################

# # import json module and xmltodict
# # module provided by python
# import json
# import xmltodict


# # open the input xml file and read
# # data in form of python dictionary 
# # using xmltodict module
# with open("Battery.out.xml") as xml_file:
	
# 	data_dict = xmltodict.parse(xml_file.read())
# 	# xml_file.close()
	
# 	# generate the object using json.dumps() 
# 	# corresponding to json data
	
# 	json_data = json.dumps(data_dict)
	
# 	# Write the json data to output 
# 	# json file
# 	with open("BatteryOut.json", "w") as json_file:
# 		json_file.write(json_data)
# 		# json_file.close()

###################################

import json
import xml.etree.ElementTree as E
tree = E.parse('Battery.out.xml')
root = tree.getroot()
d={}
for child in root:
	if child.tag not in d:
		d[child.tag]=[]
	dic={}
	for child2 in child:
		if child2.tag not in dic:
			dic[child2.tag]=child2.text
	d[child.tag].append(dic)

with open("BatteryOut.json", "w") as json_file:
	json.dump(d, json_file)

