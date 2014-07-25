def pand(s1, s2):
	if s1 == 2:
		if s2 == 0:
			return 0
		else:
			return 2
	elif s2 == 2:
		if s1 == 0:
			return 0
		else:
			return 2
	return int(s1 and s2)

def pnand(s1, s2):
	if s1 == 2:
		if s2 == 1:
			return 0
		else:
			return 2
	elif s2 == 2:
		if s1 == 1:
			return 0
		else:
			return 2
	return int(not(s1 and s2))

def por(s1, s2):
	if s1 == 2:
		if s2 == 1:
			return 1
		else:
			return 2
	elif s2 == 2:
		if s1 == 1:
			return 1
		else:
			return 2
	return int(s1 or s2)

def pnor(s1, s2):
	if s1 == 2:
		if s2 == 0:
			return 1
		else:
			return 2
	elif s2 == 2:
		if s1 == 0:
			return 1
		else:
			return 2
	return int(not(s1 or s2))

def pxor(s1, s2):
	if s1 == 2 or s2 == 2:
		return 2
	return s1 == s2

def pxnor(s1, s2):
	if s1 == 2 or s2 == 2:
		return 2
	return s1 != s2

def pnot(s1):
	if s1 == 2:
		return 2
	return int(not s1)

def init(extracted_data, wave_in_data):
	global inputs
	global outputs
	global port_data
	global wave_in

	outputs = extracted_data['outputs']
	inputs = extracted_data['inputs']
	port_data = extracted_data['ports']
	wave_in = wave_in_data
	wave_in_length = len(wave_in[0][1])
	final_signal = {}

	for output in outputs:
		output_port = search_port_by_output(output)
		total_delay = get_total_delay(output_port['id'])
		timeline_length = wave_in_length + total_delay

		if not output in final_signal:
			final_signal[output] = [0]*timeline_length

		for t in range(timeline_length):
			final_signal[output][t] = process_signal(t, output_port['id'])
		
	return final_signal

def search_port_by_id(port_id):
	for port in port_data:
		if port['id'] == port_id:			
			return port

	return False

def get_wave_signal_by_port_signal_id(t, input_id):
	for wavein_el in wave_in:
		if wavein_el[0] == input_id:
			if t < 0:
				return 2
			else:
				if (len(wavein_el[1]) - 1) < t:
					return 2
				return wavein_el[1][t]

def choose_port(type, signal_1, signal_2):
	return globals()['p' + type](signal_1, signal_2)

def search_port_by_output(output):
	for port in port_data:
		if port['output'] == output:
			return port
	return False


def process_signal(t, port_id):
	current_port_data = search_port_by_id(port_id)
	t = t - current_port_data['delay']

	input_1 = current_port_data['inputs'][0]

	if input_1 in inputs:
		signal_1 = get_wave_signal_by_port_signal_id(t, input_1)
	else:
		searched_port_1 = search_port_by_output(input_1)
		signal_1 = process_signal(t, searched_port_1['id'])
	
	input_2 = current_port_data['inputs'][1]

	if input_2 in inputs:
		signal_2 = get_wave_signal_by_port_signal_id(t, input_2)
	else:	
		searched_port_2 = search_port_by_output(input_2)
		signal_2 = process_signal(t, searched_port_2['id'])

	return choose_port(current_port_data['type'], signal_1, signal_2)

def get_total_delay(port_id):
	current_port_data = search_port_by_id(port_id)
	current_delay = current_port_data['delay']

	input_1 = current_port_data['inputs'][0]

	if input_1 in inputs:
		delay_1 = 0
	else:
		searched_port_1 = search_port_by_output(input_1)
		delay_1 = get_total_delay(searched_port_1['id'])
	
	input_2 = current_port_data['inputs'][1]

	if input_2 in inputs:
		delay_2 = 0
	else:	
		searched_port_2 = search_port_by_output(input_2)
		delay_2 = get_total_delay(searched_port_2['id'])

	if delay_1 > delay_2:
		delay = delay_1
	else:
		delay = delay_2

	delay += current_delay

	return delay
