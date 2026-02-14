import sys
import os
import pytest

# Add build dir to path
sys.path.append(os.path.join(os.getcwd(), 'build'))

def test_quantlib_nano_import():
    try:
        import quantlib_nano_cpp as ql_nano
        assert hasattr(ql_nano, 'quant_lib')
        ql = ql_nano.quant_lib
        assert hasattr(ql, 'Date')
        # TARGET is in main module or submodule? Check attributes log
        # Submodule attributes: ['Actual365Fixed', 'Date', 'Month', 'SavedSettings', 'Settings', 'TARGET', 'TimeUnit', 'days_between', 'hash_value', 'io']
        assert hasattr(ql, 'TARGET')
        assert hasattr(ql, 'Actual365Fixed')
        # FlatForward is in MAIN module or submodule?
        # Main attributes: ['Calendar', 'FlatForward', 'HandleQuote', 'RelinkableHandleQuote', 'YieldTermStructure', 'quant_lib', 'std']
        assert hasattr(ql_nano, 'FlatForward')
    except ImportError:
        pytest.fail("quantlib_nano_cpp extension not found or could not be imported")

def test_date_instantiation():
    import quantlib_nano_cpp.quant_lib as ql
    d = ql.Date(14, 2, 2026)
    assert d is not None
