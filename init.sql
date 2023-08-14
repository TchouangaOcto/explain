CREATE TABLE IF NOT EXISTS metadata_donnée_v2  (
    date VARCHAR(255),
    fichier  VARCHAR(255),
    contenu text
);

CREATE TABLE IF NOT EXISTS metadata_modèle  (
    date VARCHAR(255),
    fichier  VARCHAR(255),
    model VARCHAR(255),
    hyperparametre text,
    contenu text
);
