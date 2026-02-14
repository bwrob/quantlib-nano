import sys
import os

# Add the build directory to path to find the .so
sys.path.append(os.path.join(os.getcwd(), 'build'))

try:
    import quantlib_nano_cpp as ql_nano
    print("Module imported successfully!")
    
    # Check main attributes
    print("Main attributes:", [a for a in dir(ql_nano) if not a.startswith('__')])
    
    # Check quant_lib submodule
    if hasattr(ql_nano, 'quant_lib'):
        ql = ql_nano.quant_lib
        print("Submodule attributes:", [a for a in dir(ql) if not a.startswith('__')])
        
        if hasattr(ql, 'Date'):
            # In nanobind, if we didn't bind dayOfMonth as a property, we call it
            try:
                d = ql.Date(14, 2, 2026)
                print("Instantiated Date successfully.")
                # We might need to check the actual methods available
            except Exception as e:
                print(f"Could not instantiate Date: {e}")
        else:
            print("Date class not found in submodule.")
    else:
        print("quant_lib submodule not found.")
        
except ImportError as e:
    print(f"Failed to import module: {e}")
except Exception as e:
    print(f"Error during verification: {e}")
