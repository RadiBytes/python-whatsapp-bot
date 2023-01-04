delete src/python_whatsapp_bot.egg-info/
delete dist/
change version of pyproject.toml
run python3 -m build
run python3 -m twine upload dist/*
use __token__ as username
enter password with the pypi prefix
