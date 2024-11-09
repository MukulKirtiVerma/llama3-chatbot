# register_model.py

import os
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from azure.identity import DefaultAzureCredential
from huggingface_hub import snapshot_download

# Replace these with your Azure subscription details
subscription_id = "<YOUR_SUBSCRIPTION_ID>"
resource_group = "<YOUR_RESOURCE_GROUP>"
workspace_name = "<YOUR_WORKSPACE_NAME>"

# Authenticate to Azure ML using DefaultAzureCredential
# This credential will use the environment's default authentication methods
credential = DefaultAzureCredential()

# Create an MLClient instance
ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

# Download the GPT-Neo 1.3B model from Hugging Face
print("Downloading GPT-Neo 1.3B model... This may take a while.")
model_name = "EleutherAI/gpt-neo-1.3B"
local_model_path = "./models/gpt-neo-1.3B"

# Download the model to the specified directory
snapshot_download(repo_id=model_name, local_dir=local_model_path, local_dir_use_symlinks=False)

print("Model download complete.")

# Register the model with Azure ML
print("Registering model in Azure ML...")
model = Model(
    path=local_model_path,
    name="gpt-neo-1.3b",
    description="GPT-Neo 1.3B model from EleutherAI",
    type="custom_model",
)

ml_client.models.create_or_update(model)
print("Model registration complete.")
