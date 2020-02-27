class VariableHolder:
    def __init__(self, **kwargs):
        self.add_variables(**kwargs)

    def add_variables(self, **kwargs):
        for name, value in kwargs.items():
            exec(f"self.{name} = {float(value)}")

    def set_value(self, variable_name: str, value: float):
        if variable_name in dir(self)[28:]:
            prev_value = exec(f"self.{variable_name}")
            exec(f"self.{variable_name} = {value}")
            success = True
        else:
            prev_value = None
            success = False
        return success, prev_value
