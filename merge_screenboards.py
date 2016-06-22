from datadog import initialize, api
import sys
import json

class Custom_Dash_builder(object):

	dash = []
	dash_list = []
	margin = 5
	dict_tem_var = []
	#[{'default': '*', 'prefix': 'scope', 'name': 'scope'},
	# {'default': '*', 'prefix': 'region', 'name': 'region'}] # if you want to set your own template variables
	title = "Merged Screenboard"

	@classmethod
	def initialize(cls):
		# Init method for keys

		options = {
			'api_key': '****',
			'app_key': '****'
		}
		initialize(**options)

	@classmethod
	def dash_fetch(cls, dash_ref):
		# Method to fetch Screenboards data.

		cls.dash_list = dash_ref
		for i in range(len(dash_ref)):
			cls.dash_list[i] =  api.Screenboard.get(dash_ref[i])

		return cls.dash_list
	
	@classmethod
	def get_template_var(cls, dash):
		# Method to get the template variables and gather them without duplicate

		for i in range (len(dash['template_variables'])):

			if dash['template_variables'][i]['prefix'] not in [cls.dict_tem_var[x]['prefix'] for x in range(len(cls.dict_tem_var))]:
				cls.dict_tem_var.append(dash['template_variables'][i])

			if dash['template_variables'][i]['name'] not in [cls.dict_tem_var[x]['name'] for x in range(len(cls.dict_tem_var))]:
				if  dash['template_variables'][i]['prefix'] not in [cls.dict_tem_var[x]['prefix'] for x in range(len(cls.dict_tem_var))]: # Avoid copying twice for the first round
					cls.dict_tem_var.append(dash['template_variables'][i])
				else:
					for x in range(len(cls.dict_tem_var)): # if the name is not in the list and if the prefix is. Add the name and prefix - Get the name associated with the prefx
						if dash['template_variables'][i]['prefix'] == cls.dict_tem_var[x]['prefix']:
							cls.dict_tem_var.append(dash['template_variables'][i])
			#else:
			#	print "you have two template_variables with the same name, only getting one"			


	@classmethod
	def builder(cls, dash_ref, config):
		# Main method to build the fianl dash. 
		# Iterates through the dashboards and aligns them according to _config_ vertically or horizontally
		#config is a parameter that organizes the dashes [0:vertical (default), 1:horizontal, 2:square (if possible)]

		cls.dash_list = cls.dash_fetch(dash_ref) # array of references to the dashboards 
		cls.dash = cls.dash_list[0]
		cls.get_template_var(cls.dash)

		for j in range(1, len(cls.dash_list)):

			wmaxfinal = 0
			hmaxfinal = 0
			temp_dash = cls.dash_list[j]
			widgets = temp_dash['widgets']
			original_widgets = cls.dash['widgets']

			cls.get_template_var(temp_dash)
			## max width of dash ##
			wmax = 0
			for i in range(len(original_widgets)):
				if original_widgets[i]['x']+original_widgets[i]['width'] > wmax:
					wmax = original_widgets[i]['x']+original_widgets[i]['width']
			wmaxfinal = wmaxfinal + wmax
			## max height of dash ##
			hmax = 0
			for i in range(len(original_widgets)):
				if original_widgets[i]['y']+original_widgets[i]['height']>hmax:
					hmax = original_widgets[i]['y']+original_widgets[i]['height']
			hmaxfinal = hmaxfinal + hmax

			nmb_widgets_temp =len(widgets)
			for i in range(nmb_widgets_temp):

				cls.dash['widgets'].append(widgets[i])
				
				if config == 0:

					cls.dash['widgets'][len(original_widgets) - 1]['y'] = widgets[i]['y'] + hmaxfinal + cls.margin
					cls.dash['widgets'][len(original_widgets) - 1]['x'] = widgets[i]['x'] 
				
				if config == 1:

					cls.dash['widgets'][len(original_widgets) - 1]['y'] = widgets[i]['y'] 
					cls.dash['widgets'][len(original_widgets) - 1]['x'] = widgets[i]['x'] + wmaxfinal + cls.margin
	
		return cls.dash

	@classmethod
	def create(cls, dash_list, config):
		# Main method to init, build and perform the API call

		cls.initialize()
		cls.builder(dash_list, config)
		output = api.Screenboard.create(board_title=cls.title,
			     widgets=cls.dash['widgets'], template_variables=cls.dict_tem_var, width=cls.dash['width'])
		print "http://app.datadoghq.com/screen/" + str(output['id'])

Custom_Dash_builder().create(json.loads(sys.argv[1]), json.loads(sys.argv[2]))