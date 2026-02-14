import os
import pytest
from utils.generate_bindings import load_config

def test_config_logic():
    # Verify our logic for handling the scope file
    mock_config_content = """
[project]
name = "quantlib_nano"
namespace = "ql"

[[classes]]
name = "Date"
header = "ql/time/date.hpp"
"""
    with open('temp_scope.toml', 'w') as f:
        f.write(mock_config_content)
        
    try:
        config = load_config('temp_scope.toml')
        assert config['project']['name'] == "quantlib_nano"
        assert config['classes'][0]['name'] == "Date"
    finally:
        if os.path.exists('temp_scope.toml'):
            os.remove('temp_scope.toml')

# We'll skip actual litgen execution if Java is missing
@pytest.mark.skip(reason="litgen requires Java for execution")
def test_litgen_call():
    pass
