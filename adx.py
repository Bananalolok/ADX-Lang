import re
import time

class ADXInterpreter:
    def __init__(self):
        self.variables = {}

    def run(self, filename):
        with open(filename, 'r') as file:
            code = file.read()
            self.parse_code(code, filename)

    def parse_code(self, code, filename):
        lines = code.split('\n')
        in_loop = False

        for line_number, line in enumerate(lines, start=1):
            if line.strip():  # Skip empty lines
                if in_loop:
                    if line.strip() == "endloop":
                        in_loop = False
                    else:
                        self.execute_line(line, indent=True, line_number=line_number, filename=filename)
                else:
                    self.execute_line(line, line_number=line_number, filename=filename)

    def execute_line(self, line, indent=False, line_number=None, filename=None):
        if indent:
            line = line.strip()
        try:
            if line.startswith("var"):
                self.define_variable(line)
            elif line.startswith("print"):
                self.print_statement(line)
            elif line.startswith("loop"):
                self.loop_statement(line)
            elif line.startswith("if") or line.startswith("elif") or line.startswith("else"):
                self.condition_statement(line)
            elif line.startswith("input"):
                self.input_statement(line)
            elif line.startswith("wait"):
                self.wait_command(line)
            elif "=" in line:
                self.assign_variable(line)
            else:
                print(f"Error in {filename}, line {line_number}: Unknown statement - {line}")
        except Exception as e:
            print(f"Error in {filename}, line {line_number}: {e}")

    def define_variable(self, line):
        pattern = r"var\s+(\w+)\s*=\s*(.+)"
        match = re.match(pattern, line)
        if match:
            name, value = match.groups()
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                self.variables[name] = value[1:-1]  # Extract string value
            else:
                self.variables[name] = str(self.evaluate_expression(value))
        else:
            raise ValueError(f"Invalid variable declaration - {line}")


    def assign_variable(self, line):
        parts = line.split("=")
        variable_name = parts[0].strip()
        expression = parts[1].strip()

        if variable_name not in self.variables:
            raise ValueError(f"Variable '{variable_name}' not defined")
        else:
            self.variables[variable_name] = str(self.evaluate_expression(expression))

    def print_statement(self, line):
        pattern = r'print\s+(.+)'
        match = re.match(pattern, line)
        if match:
            expression = match.group(1).strip()
            if expression.startswith('"') and expression.endswith('"'):
                print(expression[1:-1])
            else:
                result = self.evaluate_expression(expression)
                if result is not None:
                    print(result)
        else:
            raise ValueError(f"Invalid print statement - {line}")

    def loop_statement(self, line):
        # Extract loop condition
        pattern = r'loop\s*:\s*(.+)'
        match = re.match(pattern, line)
        if match:
            loop_condition = match.group(1).strip()
            while self.evaluate_expression(loop_condition):
                pass  # Placeholder for loop block to be implemented
        else:
            raise ValueError(f"Invalid loop statement - {line}")

    def condition_statement(self, line):
        # Extract condition
        pattern = r'(if|elif|else)\s*:\s*(.+)'
        match = re.match(pattern, line)
        if match:
            keyword, condition = match.groups()
            if keyword == "else" or self.evaluate_expression(condition):
                pass  # Placeholder for if, elif, and else block to be implemented
            else:
                while line.strip() != "else:":
                    pass
        else:
            raise ValueError(f"Invalid condition statement - {line}")

    def input_statement(self, line):
        pattern = r'var\s+(\w+)\s*=\s*input\s+"(.+)"'
        match = re.match(pattern, line)
        if match:
            variable_name, question = match.groups()
            user_input = input(f"{question}: ")
            self.variables[variable_name] = user_input
        else:
            raise ValueError(f"Invalid input statement - {line}")

    def wait_command(self, line):
        pattern = r'wait\s+(\d+)'
        match = re.match(pattern, line)
        if match:
            seconds = int(match.group(1))
            time.sleep(seconds)
        else:
            raise ValueError(f"Invalid wait command - {line}")

    def evaluate_expression(self, expression):
        for var_name in self.variables:
            expression = expression.replace(var_name, str(self.variables[var_name]))
        try:
            result = eval(expression)
            return result
        except Exception as e:
            raise ValueError(e)

# Example usage
if __name__ == "__main__":
    interpreter = ADXInterpreter()
    interpreter.run("test.adx")
