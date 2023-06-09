
class EquivalencePartition(object):

    def __init__(self, parameters : dict):
        """
        Constructor de la clase EquivalencePartition.

        Args:
        ------
        parameters : dict
            Un diccionario de parámetros con la siguiente estructura: 
            { 'nombre_de_parametro_1': {{'equivalencia_1': {'valido': bool, 'representante': valor},
                                        'equivalencia_2': {'valido': bool, 'representante': valor}, ... },
                                        ...
                                        'equivalencia_n': {'valido': bool, 'representante': valor}},
            'nombre_de_parametro_2': {{'equivalencia_1': {'valido': bool, 'representante': valor},
                                        'equivalencia_2': {'valido': bool, 'representante': valor}, ... },
                                        ...
                                        'equivalencia_n': {'valido': bool, 'representante': valor}},
            ...
            'nombre_de_parametro_n': {{'equivalencia_1': {'valido': bool, 'representante': valor},
                                        'equivalencia_2': {'valido': bool, 'representante': valor},
                                        ...
                                        'equivalencia_n': {'valido': bool, 'representante': valor}, ... }

        Raises:
        -------
        Exception : Si se encuentra un error en los parámetros proporcionados.

        """

        self.__parameters = parameters
        self.__attribute_names = list(self.__parameters.keys())
        self.__n = len(parameters)

        self.__valid_parameters()
        
    
    def build_test_cases(self):
        
        """
        Genera una lista de casos de prueba válidos e inválidos para la combinación de parámetros
        especificados en la instancia actual de la clase.

        Args:
        ------
        self : obj
            La instancia actual de la clase.

        Returns:
        --------
        tests : dict 

            El formato de salida es un diccionario que contiene dos claves: 'valids' e 'invalids'.
            Cada clave contiene una lista de diccionarios que representan casos de prueba válidos e inválidos,
            respectivamente, para la combinación de parámetros especificados en la instancia actual de la clase.

            El formato de cada diccionario de caso de prueba es el siguiente:
            {
                'nombre_del_parametro_1': {
                    'equiv_class': 'nombre_clase_equivalencia_1',
                    'representante': valor_clase_de_equivalencia_1
                },
                'nombre_del_parametro_2': {
                    'equiv_class': 'nombre_clase_equivalencia_2',
                    'representante': valor_clase_de_equivalencia_2
                },
                ...,
                'nombre_del_parametro_n': {
                    'equiv_class': 'nombre_clase_equivalencia_n',
                    'representante': valor_clase_de_equivalencia_2
                }
            }

            Donde:
            - 'nombre_del_parametro_i': es el nombre del parámetro i-ésimo de la instancia de la clase.
            - 'equiv_class': es el nombre de la clase de equivalencia 
            - 'representante': es el valor del caso de prueba para el parámetro i-ésimo de la instancia de la clase.

        """


        valid_test_cases = self.__generate_valid_test_cases()
        invalid_test_cases = self.__generate_invalid_test_cases()
        tests = {'casos_validos' : valid_test_cases, 'casos_invalidos' : invalid_test_cases}

        return tests


    def __valid_parameters(self):

        """
        Valida los parámetros almacenados en la instancia actual de la clase.
        Args:
        ------
        self : obj
            La instancia actual de la clase.
        Raises:
        -------
        AssertionError : Si hay un error durante la validación de los parametros
        """
        for var in self.__parameters:
            try:
                assert len(self.__parameters[var].keys()) > 0, 'No hay clases de equivalencia.'
                for equiv_class_name in self.__parameters[var]:
                    equiv_class = self.__parameters[var][equiv_class_name]
                    assert equiv_class.get('valido') != None, f'`El valor "es valido" de {equiv_class_name}` es None.'
                    assert type(equiv_class['valido']) == bool, f'El tipo "es valido: de `{equiv_class_name}` no es un boolean.'
                    assert equiv_class.get('representante') != None, f'El valor de `{equiv_class_name}` es None.'
                    assert equiv_class['representante'] != "", f'El valor de `{equiv_class_name}` es vacio.'
            except AssertionError as e:
                raise AssertionError(F'Error en `{var}`: {e}')

    def __generate_valid_test_cases(self): 
        
        """
        Esta función genera una lista de casos de prueba válidos para la combinación de parámetros
        especificados en el diccionario de parámetros de la instancia actual. Los casos de prueba
        válidos son aquellos que tienen valores válidos para cada parámetro de entrada según lo
        especificado en el diccionario de parámetros.
        
        Args:
        ------
        self : obj
            La instancia actual de la clase.

        Returns:
        --------
        test_cases : list
            Una lista de diccionarios que representan casos de prueba válidos para la combinación de
            parámetros especificados en el diccionario de parámetros de la instancia actual.
        """
            
        test_cases = []
        def generate_combinations(remaining_attributes, current_combination):
            if not remaining_attributes:
                if current_combination not in test_cases:
                    test_cases.append(current_combination)
            else:
                current_attribute = remaining_attributes[0]
                items = list(filter(lambda x: x[1]['valido'] == True, self.__parameters[current_attribute].items()))
                for class_equivalent, class_value in items: 
                    new_combination = current_combination.copy()
                    new_combination[current_attribute] = {'clase_equivalencia' : class_equivalent, 'representante' : class_value['representante']}
                    generate_combinations(remaining_attributes[1:], new_combination)
                     
        generate_combinations(self.__attribute_names, {})
        return test_cases

    def __generate_invalid_test_cases(self):
        """
        Esta función genera una lista de casos de prueba inválidos para la combinación de parámetros
        especificados en el diccionario de parámetros de la instancia actual. Los casos de prueba
        inválidos son aquellos que tienen valores inválidos para al menos uno de los parámetros de
        entrada según lo especificado en el diccionario de parámetros.
        
        Return:
        --------
        test_cases : list
            Una lista de diccionarios que representan casos de prueba inválidos para la combinación de
            parámetros especificados en el diccionario de parámetros de la instancia actual. Para casa invalido
            se combina con otros paramatros valiudos
        """
        test_cases = []

        def generate_combinations(remaining_attributes, current_combination, valid):
            if not remaining_attributes: 
                if current_combination not in test_cases:
                    test_cases.append(current_combination)
            else:

                current_attribute = remaining_attributes[0]

                items = list(filter(lambda x: x[1]['valido'] == valid, self.__parameters[current_attribute].items()))
                items = items if not valid else [items[0]] 

                for class_equiv, class_value in items:
                    new_combination = current_combination.copy()
                    new_combination[current_attribute] = { 'clase_equivalencia' : class_equiv, 'representante' : class_value['representante'] }
                    generate_combinations(remaining_attributes[1:], new_combination, valid=True)

        for _ in range(self.__n):
            generate_combinations(self.__attribute_names, {}, valid=False)
            self.__attribute_names = self.__attribute_names[1:] + [self.__attribute_names[0]]

        return test_cases
