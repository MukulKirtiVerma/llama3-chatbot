# llama3-chatbot

```
az group create --name myResourceGroup --location eastus
az acr create --resource-group myResourceGroup --name myContainerRegistry --sku Basic --location eastus
az ml workspace create --name my-aml-workspace --resource-group myResourceGroup --location eastus
pip install huggingface_hub
python download_model.py
pip install azure-ai-ml azure-identity
python register_model.py
az ml online-endpoint create -f endpoint.yml
az ml online-deployment create -f deployment.yml --all-traffic
az acr login --name myContainerRegistry
docker build -t mycontainerregistry.azurecr.io/streamlit-app:latest .
docker push mycontainerregistry.azurecr.io/streamlit-app:latest
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myStreamlitApp --deployment-container-image-name mycontainerregistry.azurecr.io/streamlit-app:latest
az ml online-endpoint show --name gpt-neo-endpoint --query scoring_uri -o tsv
az ml online-endpoint get-credentials --name gpt-neo-endpoint --query primaryKey -o tsv
az webapp config appsettings set --resource-group myResourceGroup --name myStreamlitApp --settings ENDPOINT_URI=<YOUR_ENDPOINT_URI> ENDPOINT_KEY=<YOUR_KEY>
az ad sp create-for-rbac --name "github-actions-sp" --sdk-auth --role contributor --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID>/resourceGroups/myResourceGroup

```

