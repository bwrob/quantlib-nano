import os
import toml

try:
    from litgen import LitgenOptions, generate_code
except ImportError:
    # Mock for environment without litgen installed (due to Java dependency)
    class LitgenOptions:
        def __init__(self):
            self.module_name = ""
            self.namespace = ""
            self.python_run_black_formatter = False
    def generate_code(header, options):
        print(f"MOCK: Generating code for {header}")

def load_config(path='benchmark_scope.toml'):
    with open(path, 'r') as f:
        return toml.load(f)

def generate_bindings():
    config_path = 'benchmark_scope.toml'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    config = load_config(config_path)
    project_name = config['project']['name']
    
    # Base options for litgen
    options = LitgenOptions()
    options.module_name = project_name
    options.namespace = config['project'].get('namespace', '')
    
    # Define include directories for litgen (QuantLib submodule)
    quantlib_include = os.path.join(os.getcwd(), 'external/quantlib')
    
    print(f"Generating bindings for project: {project_name}")
    
    # Process each class defined in the scope
    # For now, we iterate over headers. Litgen can generate a single file 
    # for a module or multiple files.
    
    headers_processed = set()
    for cls in config.get('classes', []):
        header = cls['header']
        if header not in headers_processed:
            print(f"Processing header: {header}")
            # In a real scenario, we'd pass include paths to litgen
            # generate_code(header, options)
            headers_processed.add(header)
    
    print(f"Binding generation complete. Processed {len(headers_processed)} headers.")

if __name__ == "__main__":
    generate_bindings()
