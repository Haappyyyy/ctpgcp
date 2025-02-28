## Questions Ouvertes 


# 1. Création d'un Service Account 

Dans un premier temps il est nécessaire de se rendre sur IAM & Admin > Service Accounts puis on crée un compte de service en cliquant sur "Create Service Account".
On va nommer le compte, lui attribuer une description, puis cliquer sur "Create". Ensuite on va lui assigner les rôles nécessaires pour définir les permissions du service account.

Et enfin on peut configurer les clés d’authentification si besoin (JSON ou P12), puis finaliser la création.



# 2. Création d'un bucket 

Pour commencer on accéde à Google Cloud Storage via la console GC puis on clique sur "Create bucket" et on choisit un nom.
On vient ensutie définir l’emplacement selon les besoins de disponibilité et de latence.

Ensuite on doit choisir une classe de stockage en fonction des besoins d’accès.

On configure les contrôles d'accès et enfin on peut éventuellement activer la politique de conservation.

# Gestion des droits (IAM)

IAM est un outil permettant de gérer l'autorisation précise pour Google Cloud. En d'autres termes, il permet de contrôler qui peut faire quoi sur quelles ressources.

Exemple concret : 

Par exemple, dans le cas de figure où des administrateurs et des développeurs travaillent sur les mêmes ressources, il serait intéressant de séparer les permissions. 

Ainsi on pourrait avoir cette configuration pour les admins : 

gcloud projects add-iam-policy-binding my-project \
  --member="group:admin@example.com" \
  --role="roles/storage.admin"

Et pour les dev : 

gcloud projects add-iam-policy-binding my-project \
  --member="group:devs@example.com" \
  --role="roles/storage.objectViewer"

# Configuration de la facturation 

Pour configurer la facturation, on doit suivre ces étapes : GCP -> Facturation -> On crée un compte de facturation et on le lie avec un moyen de paiement -> On lie compte de facturation au projet GCP 

Mes recommandations pour éviter des coûts imprévus  : 

- Configurer un budget et des alertes
- Surveiller les coûts avec les outils intégrés 
- Désactiver les ressources inutilisées
- Mettre en place des quotas pour limiter la consommation

# Règles de vie 

Merci et au revoir. 


# TP 

On commence logiquement par créér le dépot github disponible à cette adresse : https://github.com/Haappyyyy/ctpgcp

# Création Service Account (SA)

gcloud iam service-accounts create my-service-account \
    --description="Service Account pour CI/CD" \
    --display-name="ci-cd-sa"

# Autorisations 

## Permissions

Le compte sebastien.wachter.ext@univ-lille.fr doit pouvoir consulter uniquement mon projet complet.
On va donc lui donner les droits Lecteur d'objets Storage (voir captures)

On doit également autoriser le SA cicd-swa@notes-on-cloud-swa.iam.gserviceaccount.com à pouvoir écrire sur le bucket 
On va donc lui donner les droits Créateur d'objets Storage (voir captures)



## Création d'un CI CD

On commence par ajouter un github workflows Actions 

On crée un fichier `.github/workflows/ci-cd.yml` dans votre le dépot avec le contenu suivant :

```yaml
name: CI CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Log in to Google Cloud
      uses: google-github-actions/auth@v0
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}

    - name: Configure docker for Google Artifact Registry
      run: gcloud auth configure-docker us-central1-docker.pkg.dev

    - name: Build Docker image
      run: docker build -t us-central1-docker.pkg.dev/$GCP_PROJECT_ID/$ARTIFACT_REPOSITORY/$IMAGE_NAME:$GITHUB_SHA .

    - name: Push Docker image
      run: docker push us-central1-docker.pkg.dev/$GCP_PROJECT_ID/$ARTIFACT_REPOSITORY/$IMAGE_NAME:$GITHUB_SHA

    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image us-central1-docker.pkg.dev/$GCP_PROJECT_ID/$ARTIFACT_REPOSITORY/$IMAGE_NAME:$GITHUB_SHA \
          --region us-central1 \
          --platform managed \
          --allow-unauthenticated
```

Je définis les secrets `GCP_SA_KEY`, `GCP_PROJECT_ID`, `ARTIFACT_REPOSITORY`, `IMAGE_NAME`, et `SERVICE_NAME` dans les paramètres de mon dépôt GitHub.


# Création d'alertes 

On veut créer une alerte si le budget dépasse 50$. 

On se rend dans le menu Facturation -> Budgets et Alertes -> Créer un budget 

Ensuite on choisit un nom puis le montant, c'est à dire 50$

# Stocker sur le bucket le fichier Dockerfile 

On utilise la commande : 

gsutil cp Dockerfile gs:/bucket-arthur-delobel-ctp

# Déploiement d'un cloud run 



