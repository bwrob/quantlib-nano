import os
import toml
import re
from litgen import LitgenOptions, generate_code_for_file

def load_config(path='benchmark_scope.toml'):
    with open(path, 'r') as f:
        return toml.load(f)

class BindingProcessor:
    def __init__(self, header, generator_output):
        self.header = header
        self.code = generator_output.pydef_code
        
    def clean(self):
        # 1. Base replacements
        self.code = self.code.replace('py::', 'nb::')
        self.code = self.code.replace('pyNsQuantLib', 'sub_m')
        
        # 2. Nanobind specific fixes
        self.code = self.code.replace('nb::arithmetic()', '')
        self.code = self.code.replace(', ,', ',')
        self.code = re.sub(r'auto pyNsstd_Classhash<.*?> =.*?;', '', self.code, flags=re.DOTALL)

        # 3. Handle abstract classes - minimal registration
        abstract_patterns = ["yieldtermstructure", "calendar.hpp", "observable.hpp", "termstructure.hpp", "lazyobject.hpp", "quote.hpp", "handle.hpp", "flatforward.hpp"]
        is_abstract = any(p in self.header for p in abstract_patterns)
        
        if is_abstract:
            # Special case for Handle templates
            if "handle.hpp" in self.header:
                self.code = """
    nb::class_<Handle<Quote>>(sub_m, "HandleQuote");
    nb::class_<RelinkableHandle<Quote>>(sub_m, "RelinkableHandleQuote");
"""
            else:
                # Match only the class declaration, NO methods
                match = re.search(r'(nb::class_<.*?>\s*\(.*?\))', self.code, flags=re.DOTALL)
                if match:
                    self.code = "    " + match.group(1) + ";"
                else:
                    lines = self.code.split('\n')
                    for line in lines:
                        if "nb::class_<" in line:
                            self.code = line + ";"
                            break

        return self.code

def generate_bindings():
    config_path = 'benchmark_scope.toml'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    config = load_config(config_path)
    project_name = config['project']['name']
    
    output_dir = os.path.join(os.getcwd(), 'src/generated')
    os.makedirs(output_dir, exist_ok=True)
    
    options = LitgenOptions()
    options.module_name = project_name
    options.namespace = config['project'].get('namespace', '')
    options.python_run_black_formatter = False
    options.nanobind_import_name = "nb"
    
    quantlib_include = os.path.join(os.getcwd(), 'external/quantlib')
    
    print(f"Generating bindings for project: {project_name}")
    
    headers_processed = []
    registration_functions = []
    
    skip_headers = [] 
    
    headers = [cls['header'] for cls in config.get('classes', [])]
    seen = set()
    headers = [x for x in headers if not (x in seen or seen.add(x))]
    
    for header in headers:
        if header in skip_headers:
            continue
            
        print(f"Generating bindings for header: {header}")
        header_full_path = os.path.join(quantlib_include, header)
        
        func_suffix = header.replace('/', '_').replace('.hpp', '')
        func_name = f"gen_{func_suffix}"
        registration_functions.append(func_name)
        
        output_basename = f"{func_suffix}.cpp"
        output_path = os.path.join(output_dir, output_basename)
        
        try:
            generator = generate_code_for_file(options, header_full_path)
            processor = BindingProcessor(header, generator)
            code = processor.clean()

            wrapped_code = f"""
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <{header}>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void {func_name}(nb::module_ &m) {{
    nb::module_ &sub_m = m; 
{code}
}}
"""
            # Fix: Inject YieldTermStructure base for FlatForward manually if needed
            if "flatforward" in header:
                wrapped_code = wrapped_code.replace('nb::class_<QuantLib::FlatForward>', 'nb::class_<QuantLib::FlatForward, YieldTermStructure>')

            with open(output_path, 'w') as f:
                f.write(wrapped_code)
            headers_processed.append(header)
        except Exception as e:
            print(f"Error generating {header}: {e}")
    
    with open(os.path.join(output_dir, "registration.h"), 'w') as f:
        f.write("#include <nanobind/nanobind.h>\n\n")
        for func in registration_functions:
            f.write(f"void {func}(nanobind::module_ &m);\n")
            
    print(f"Binding generation complete. Processed {len(headers_processed)} headers.")

if __name__ == "__main__":
    generate_bindings()
