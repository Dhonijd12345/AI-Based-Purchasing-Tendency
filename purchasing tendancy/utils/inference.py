import torch
import numpy as np
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from models.gnn_model import PurchasingGNN
from models.sasrec_model import SASRec
import os

class InferenceService:
    def __init__(self, model_dir="models/trained"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_dir = model_dir
        
        # Load encoders
        self.u_le = joblib.load(os.path.join(model_dir, "u_le.joblib"))
        self.p_le = joblib.load(os.path.join(model_dir, "p_le.joblib"))
        self.l_le = joblib.load(os.path.join(model_dir, "l_le.joblib"))
        
        # Load Embeddings
        self.embeddings = torch.load(os.path.join(model_dir, "embeddings.pth"), map_location=self.device)
        self.user_embeddings = self.embeddings['user'].detach().cpu().numpy()
        self.product_embeddings = self.embeddings['product'].detach().cpu().numpy()
        
        # Perform Community Detection on startup
        self.num_communities = 5
        self.kmeans = KMeans(n_clusters=self.num_communities, random_state=42)
        self.user_communities = self.kmeans.fit_predict(self.user_embeddings)
        
        # Load models
        num_products = len(self.p_le.classes_)
        self.sas_model = SASRec(item_num=num_products, hidden_units=64, num_blocks=2, num_heads=2, dropout_rate=0.1, device=self.device)
        self.sas_model.load_state_dict(torch.load(os.path.join(model_dir, "sasrec_model.pth"), map_location=self.device))
        self.sas_model.eval()

    def get_user_community(self, user_id):
        try:
            u_idx = self.u_le.transform([user_id])[0]
            return int(self.user_communities[u_idx])
        except:
            return -1 # Cold Start

    def get_recommendations(self, user_id, top_n=5):
        try:
            u_idx = self.u_le.transform([user_id])[0]
            user_emb = self.user_embeddings[u_idx]
            
            # Simple similarity-based recommendation using GNN embeddings
            scores = np.dot(self.product_embeddings, user_emb)
            top_indices = np.argsort(scores)[-top_n:][::-1]
            return self.p_le.inverse_transform(top_indices).tolist()
        except:
            # Random recommendations for cold start
            return np.random.choice(self.p_le.classes_, top_n).tolist()

    def get_regional_demand(self):
        # Calculate demand per location based on user embeddings and transactions
        # Returns a list of dicts for visualization
        location_demand = []
        for loc_name in self.l_le.classes_:
            loc_idx = self.l_le.transform([loc_name])[0]
            # Average embedding of users in this location
            # (In a real scenario, integrate more complex demand logic)
            demand_score = np.random.uniform(0.1, 1.0) # Placeholder
            level = 'high' if demand_score > 0.7 else 'medium' if demand_score > 0.4 else 'low'
            location_demand.append({
                'location': loc_name,
                'demand_score': round(demand_score, 2),
                'demand_level': level
            })
        return location_demand

if __name__ == "__main__":
    service = InferenceService()
    print("Inference service loaded.")
    print(f"User 1 recommendations: {service.get_recommendations(1)}")
    print(f"User 1 community: {service.get_user_community(1)}")
