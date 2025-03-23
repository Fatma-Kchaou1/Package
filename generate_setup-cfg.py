setup_cfg_content = """[metadata]
name = PackageTag
version = 0.0.0
author = Fatma
author_email = fatma.kchaou29@gmail.com
description = But de créer un package avec v0.0.0
long_description_content_type = text/markdown

[options]
packages = find:
install_requires =
    requests
    numpy
python_requires = >=3.10.0
"""

# Écriture dans le fichier setup.cfg
with open("setup.cfg", "w", encoding="utf-8") as file:
    file.write(setup_cfg_content)

print("setup.cfg a été créé avec succès !")
