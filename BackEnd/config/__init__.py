import os

config_name = os.getenv('FLASK_CONFIG', 'local')

if config_name == 'local':
    from .local import Config
elif config_name == 'production':
    from .production import Config
else:
    raise ValueError(f"Invalid FLASK_CONFIG value: {config_name}")
