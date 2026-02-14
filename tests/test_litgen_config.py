import toml
import os

def test_load_benchmark_scope():
    # Create a mock benchmark_scope.toml
    config_path = 'benchmark_scope.toml'
    mock_config = {
        'project': {
            'name': 'quantlib_nano',
            'namespace': 'ql'
        },
        'classes': [
            {'name': 'Date', 'header': 'ql/time/date.hpp'},
            {'name': 'Calendar', 'header': 'ql/time/calendar.hpp'}
        ]
    }
    
    with open(config_path, 'w') as f:
        toml.dump(mock_config, f)
        
    try:
        # Load and verify
        with open(config_path, 'r') as f:
            config = toml.load(f)
            
        assert config['project']['name'] == 'quantlib_nano'
        assert len(config['classes']) == 2
        assert config['classes'][0]['name'] == 'Date'
    finally:
        if os.path.exists(config_path):
            os.remove(config_path)
