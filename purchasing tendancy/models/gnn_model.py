import torch
import torch.nn.functional as F
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv, GATConv
from torch_geometric.data import HeteroData

class PurchasingGNN(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels, num_user_features, num_product_features, num_location_features):
        super().__init__()
        
        # Linear layers to project features to same dimension
        self.user_lin = torch.nn.Linear(num_user_features, hidden_channels)
        self.product_lin = torch.nn.Linear(num_product_features, hidden_channels)
        self.loc_lin = torch.nn.Linear(num_location_features, hidden_channels)
        
        # Heterogeneous Convolution layers
        self.conv1 = HeteroConv({
            ('user', 'purchases', 'product'): SAGEConv((-1, -1), hidden_channels),
            ('product', 'bought_by', 'user'): SAGEConv((-1, -1), hidden_channels),
            ('user', 'resides_in', 'location'): SAGEConv((-1, -1), hidden_channels),
            ('location', 'host_to', 'user'): SAGEConv((-1, -1), hidden_channels),
        }, aggr='sum')
        
        self.conv2 = HeteroConv({
            ('user', 'purchases', 'product'): GATConv((-1, -1), hidden_channels, add_self_loops=False),
            ('product', 'bought_by', 'user'): GATConv((-1, -1), hidden_channels, add_self_loops=False),
            ('user', 'resides_in', 'location'): GATConv((-1, -1), hidden_channels, add_self_loops=False),
            ('location', 'host_to', 'user'): GATConv((-1, -1), hidden_channels, add_self_loops=False),
        }, aggr='sum')
        
        self.post_lin = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x_dict, edge_index_dict):
        # Project features
        x_dict['user'] = self.user_lin(x_dict['user']).relu()
        x_dict['product'] = self.product_lin(x_dict['product']).relu()
        x_dict['location'] = self.loc_lin(x_dict['location']).relu()
        
        # Layer 1
        x_dict = self.conv1(x_dict, edge_index_dict)
        x_dict = {key: x.relu() for key, x in x_dict.items()}
        
        # Layer 2
        x_dict = self.conv2(x_dict, edge_index_dict)
        x_dict = {key: self.post_lin(x) for key, x in x_dict.items()}
        
        return x_dict

# Model for Community Classification (using the embeddings)
class CommunityClassifier(torch.nn.Module):
    def __init__(self, embedding_dim, num_communities):
        super().__init__()
        self.lin1 = torch.nn.Linear(embedding_dim, 64)
        self.lin2 = torch.nn.Linear(64, num_communities)
        
    def forward(self, x):
        x = F.relu(self.lin1(x))
        return F.log_softmax(self.lin2(x), dim=-1)
