import zipfile
import os
import sys


def extract_whl(whl_path, extract_to="whl_extracted"):
    """Décompresse un fichier .whl et récupère les métadonnées depuis METADATA."""

    if not zipfile.is_zipfile(whl_path):
        sys.exit(f"Erreur : {whl_path} n'est pas un fichier ZIP valide.")

    # Extraction des fichiers
    with zipfile.ZipFile(whl_path, 'r') as whl_file:
        whl_file.extractall(extract_to)
    print(f"Fichiers extraits dans {extract_to}")

    # Rechercher les métadonnées dans METADATA
    metadata = {}
    for root, _, files in os.walk(extract_to):
        if "METADATA" in files:
            with open(os.path.join(root, "METADATA"), encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Version:"):
                        metadata['version'] = line.split("Version:")[1].strip()
                    elif line.startswith("Name:"):
                        metadata['name'] = line.split("Name:")[1].strip()
                    elif line.startswith("Author:"):
                        metadata['author'] = line.split("Author:")[1].strip()

    if not metadata.get('version'):
        sys.exit("Erreur : Impossible de trouver la version !")

    print(f"Version trouvée : {metadata['version']}")
    return metadata


def generate_setup_cfg(extract_to, metadata):
    """Génère un fichier setup.cfg avec les métadonnées extraites."""

    setup_cfg_content = f"""
[metadata]
name = {metadata['name']}
version = {metadata['version']}
author = {metadata.get('author', 'Auteur inconnu')}
description = Description du package
long_description_content_type = text/markdown

[options]
packages = find:
python_requires = >=3.10.0
    """

    setup_cfg_path = os.path.join(extract_to, "setup.cfg")

    with open(setup_cfg_path, "w", encoding="utf-8") as f:
        f.write(setup_cfg_content)
    print(f"Le fichier setup.cfg a été généré dans {extract_to}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Utilisation : python unzip_whl.py fichier.whl")

    metadata = extract_whl(sys.argv[1])
    generate_setup_cfg("whl_extracted", metadata)  # Générer le fichier setup.cfg après extraction
