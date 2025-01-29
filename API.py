from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
import torch

# Définir l'application FastAPI
app = FastAPI()

# Chemins et configuration
model_name = "google/flan-t5-base"  # Modèle de base sur Hugging Face
lora_path = "/home/abdellah/Documents/LLM/lora-flan-t5-"  # Chemin local des poids LoRA
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Charger le modèle de base depuis Hugging Face
print("Chargement du modèle de base...")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
print("Modèle de base chargé.")

# Charger les poids LoRA locaux
print("Chargement des poids LoRA...")
model = PeftModel.from_pretrained(model, lora_path)
model.to(device)
print("Poids LoRA appliqués.")

# Charger le tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Définir le format de la requête
class Query(BaseModel):
    question: str


# Endpoint pour générer une réponse
@app.post("/predict/")
def predict(query: Query):
    input_text = f"Question: {query.question}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"question": query.question, "response": response}


# Instructions pour démarrer le serveur
# Lancez cette commande : uvicorn filename:app --reload
