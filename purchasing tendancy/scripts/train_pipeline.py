import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
import numpy as np
from sklearn.preprocessing import LabelEncoder
from models.gnn_model import PurchasingGNN
from models.sasrec_model import SASRec
import os
import joblib

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def preprocess_for_gnn(users_path, products_path, transactions_path):
    users_df = pd.read_csv(users_path)
    products_df = pd.read_csv(products_path)
    transactions_df = pd.read_csv(transactions_path)
    
    # Label Encoders
    u_le = LabelEncoder()
    p_le = LabelEncoder()
    l_le = LabelEncoder()
    
    # Fit
    users_df['u_idx'] = u_le.fit_transform(users_df['user_id'])
    products_df['p_idx'] = p_le.fit_transform(products_df['product_id'])
    
    # Location mapping
    unique_locations = users_df['location'].unique()
    l_le.fit(unique_locations)
    users_df['l_idx'] = l_le.transform(users_df['location'])
    
    # Features
    user_features = torch.eye(len(users_df)) # Simple one-hot for now
    product_features = torch.eye(len(products_df))
    location_features = torch.eye(len(unique_locations))
    
    data = HeteroData()
    data['user'].x = user_features
    data['product'].x = product_features
    data['location'].x = location_features
    
    # Edges
    # user -> purchases -> product
    purchases = transactions_df.merge(users_df[['user_id', 'u_idx']], on='user_id')
    purchases = purchases.merge(products_df[['product_id', 'p_idx']], on='product_id')
    
    edge_index_user_product = torch.tensor([purchases['u_idx'].values, purchases['p_idx'].values], dtype=torch.long)
    data['user', 'purchases', 'product'].edge_index = edge_index_user_product
    data['product', 'bought_by', 'user'].edge_index = edge_index_user_product.flip(0)
    
    # user -> resides_in -> location
    edge_index_user_location = torch.tensor([users_df['u_idx'].values, users_df['l_idx'].values], dtype=torch.long)
    data['user', 'resides_in', 'location'].edge_index = edge_index_user_location
    data['location', 'host_to', 'user'].edge_index = edge_index_user_location.flip(0)
    
    return data, u_le, p_le, l_le

def train_gnn(data, hidden_channels, out_channels):
    model = PurchasingGNN(
        hidden_channels=hidden_channels,
        out_channels=out_channels,
        num_user_features=data['user'].x.size(1),
        num_product_features=data['product'].x.size(1),
        num_location_features=data['location'].x.size(1)
    ).to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    data = data.to(device)
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        out_dict = model(data.x_dict, data.edge_index_dict)
        
        # Link prediction loss (simplified)
        pos_edges = data['user', 'purchases', 'product'].edge_index
        user_emb = out_dict['user'][pos_edges[0]]
        prod_emb = out_dict['product'][pos_edges[1]]
        
        loss = F_link_loss(user_emb, prod_emb)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"GNN Epoch {epoch}, Loss: {loss.item()}")
            
    return model, out_dict

def F_link_loss(user_emb, prod_emb):
    # Binary cross entropy for positive samples (should include negative samples in real scenarios)
    scores = torch.sigmoid((user_emb * prod_emb).sum(dim=-1))
    return -torch.log(scores + 1e-15).mean()

def train_sasrec(transactions_path, item_num):
    df = pd.read_csv(transactions_path)
    # Group by user and sort by timestamp
    df = df.sort_values(['user_id', 'timestamp'])
    user_seqs = df.groupby('user_id')['product_id'].apply(list).tolist()
    
    # Pad sequences to length 50
    seq_len = 50
    padded_seqs = []
    for s in user_seqs:
        if len(s) > seq_len:
            padded_seqs.append(s[-seq_len:])
        else:
            padded_seqs.append([0] * (seq_len - len(s)) + s)
    
    padded_seqs = np.array(padded_seqs)
    
    model = SASRec(item_num=item_num, hidden_units=64, num_blocks=2, num_heads=2, dropout_rate=0.1, device=device).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss() # Simplified for demonstration
    
    print("Training SASRec...")
    for epoch in range(10):
        optimizer.zero_grad()
        # In real SASRec, we predict the next item. Here we just show forward pass.
        feats = model(padded_seqs)
        loss = feats.mean() # Placeholder loss
        loss.backward()
        optimizer.step()
        print(f"SASRec Epoch {epoch}, Loss: {loss.item()}")
        
    return model

if __name__ == "__main__":
    # Use relative paths from project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    model_dir = os.path.join(base_dir, "models", "trained")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    print("Preprocessing data for GNN...")
    gnn_data, u_le, p_le, l_le = preprocess_for_gnn(
        f"{data_dir}/users.csv",
        f"{data_dir}/products.csv",
        f"{data_dir}/transactions.csv"
    )
    
    print("Training GNN...")
    gnn_model, embeddings = train_gnn(gnn_data, hidden_channels=64, out_channels=32)
    torch.save(gnn_model.state_dict(), f"{model_dir}/gnn_model.pth")
    torch.save(embeddings, f"{model_dir}/embeddings.pth")
    
    print("Training SASRec...")
    num_products = len(p_le.classes_)
    sas_model = train_sasrec(f"{data_dir}/transactions.csv", num_products)
    torch.save(sas_model.state_dict(), f"{model_dir}/sasrec_model.pth")
    
    # Save LabelEncoders for inference
    import joblib
    joblib.dump(u_le, f"{model_dir}/u_le.joblib")
    joblib.dump(p_le, f"{model_dir}/p_le.joblib")
    joblib.dump(l_le, f"{model_dir}/l_le.joblib")
    
    print("All models trained and saved.")
