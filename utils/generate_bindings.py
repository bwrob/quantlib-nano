import os
import toml
from litgen import LitgenOptions, generate_code

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
    options.python_run_black_formatter = False
    
    # Define include directories for litgen (QuantLib submodule)
    quantlib_include = os.path.join(os.getcwd(), 'external/quantlib')
    
    print(f"Generating bindings for project: {project_name}")
    
    # Process each class defined in the scope
    headers_processed = set()
    for cls in config.get('classes', []):
        header = cls['header']
        if header not in headers_processed:
            print(f"Processing header: {header}")
            # Header path should be relative to QuantLib include or absolute
            header_full_path = os.path.join(quantlib_include, header)
            if os.path.exists(header_full_path):
                # In Phase 3, we will enable the actual call
                # generate_code(header_full_path, options)
                headers_processed.add(header)
            else:
                print(f"Warning: Header not found: {header_full_path}")
    
    print(f"Binding generation structure verified. Processed {len(headers_processed)} headers.")

if __name__ == "__main__":
    generate_bindings()
