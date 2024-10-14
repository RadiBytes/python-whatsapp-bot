# Deployment checklist

delete src/python_whatsapp_bot.egg-info/
delete dist/
change version of pyproject.toml
*optional run >> python3 -m pip install --upgrade build
run >> python3 -m build
*optional run >> python3 -m pip install --upgrade twine
run >> python3 -m twine upload dist/*
use __token__ as username
enter password with the pypi prefix
