def get_request_parameters(request, query_parameters_info):
    
    parameters = []
    for parameter_info in query_parameters_info: # name, check, default, error_message
        
        default = parameter_info['default']
        value = request.GET.get(parameter_info['name'], default)
        if parameter_info['check'] and value == default:
            return [None, parameter_info['error_message']]
        
        parameters.append(value)
    
    return [parameters, '']