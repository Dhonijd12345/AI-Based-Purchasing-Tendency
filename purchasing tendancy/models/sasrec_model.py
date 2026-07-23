import torch
import torch.nn as nn
import numpy as np

class SASRec(nn.Module):
    def __init__(self, item_num, hidden_units, num_blocks, num_heads, dropout_rate, device='cpu'):
        super(SASRec, self).__init__()
        self.item_num = item_num
        self.hidden_units = hidden_units
        self.device = device
        
        # Embeddings
        self.item_emb = nn.Embedding(self.item_num + 1, self.hidden_units, padding_idx=0)
        self.pos_emb = nn.Embedding(51, self.hidden_units) # Max sequence length 50, 1-indexed
        self.emb_dropout = nn.Dropout(p=dropout_rate)
        
        # Transformer blocks
        self.attention_layers = nn.ModuleList()
        self.forward_layers = nn.ModuleList()
        self.attention_layernorms = nn.ModuleList()
        self.forward_layernorms = nn.ModuleList()
        
        for _ in range(num_blocks):
            self.attention_layernorms.append(nn.LayerNorm(hidden_units, eps=1e-8))
            self.attention_layers.append(nn.MultiheadAttention(hidden_units, num_heads, dropout=dropout_rate))
            self.forward_layernorms.append(nn.LayerNorm(hidden_units, eps=1e-8))
            self.forward_layers.append(nn.Sequential(
                nn.Linear(hidden_units, hidden_units),
                nn.ReLU(),
                nn.Linear(hidden_units, hidden_units)
            ))
            
        self.last_layernorm = nn.LayerNorm(hidden_units, eps=1e-8)

    def forward(self, log_seqs):
        # log_seqs: [batch_size, seq_len]
        seqs = self.item_emb(torch.LongTensor(log_seqs).to(self.device))
        seqs *= self.item_emb.embedding_dim ** 0.5
        
        positions = np.tile(np.arange(1, log_seqs.shape[1] + 1), [log_seqs.shape[0], 1])
        seqs += self.pos_emb(torch.LongTensor(positions).to(self.device))
        seqs = self.emb_dropout(seqs)
        
        # Use causal mask to prevent looking ahead
        timeline_mask = (torch.LongTensor(log_seqs) == 0).to(self.device)
        seqs *= ~timeline_mask.unsqueeze(-1) # [batch_size, seq_len, hidden_units]
        
        # Multi-head attention requires [seq_len, batch_size, hidden_units]
        tl = seqs.shape[1]
        attention_mask = ~torch.tril(torch.ones((tl, tl), device=self.device)).bool()
        
        for i in range(len(self.attention_layers)):
            seqs = torch.transpose(seqs, 0, 1) # [seq_len, batch_size, hidden_units]
            Q = self.attention_layernorms[i](seqs)
            mha_outputs, _ = self.attention_layers[i](Q, seqs, seqs, attn_mask=attention_mask)
            seqs = Q + mha_outputs 
            seqs = torch.transpose(seqs, 0, 1) # [batch_size, seq_len, hidden_units]
            
            # Feed forward
            residual = seqs
            seqs = self.forward_layernorms[i](seqs)
            seqs = self.forward_layers[i](seqs)
            seqs = residual + seqs
            
        log_feats = self.last_layernorm(seqs) # [batch_size, seq_len, hidden_units]
        return log_feats
