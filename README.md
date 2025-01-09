# Semi-Supervised Node Classification Using Graph Convolutional Network

## Project Description
- In this project we have implemented a 2 layer Graph Convolution Network to perform Node classification on Cora dataset (citation network). 
- The Citation Networks are undirected,unweighted graphs where the nodes denote academic publications and the edges represent the citations between 2 papers.
- Semi Supervised Learning involves few labeled nodes for training the model, remaining nodes labels needs to be determined using the graph structure and the node features.

## About Graph Convolution Network
A Graph Convolution Network (GCN) is a type of neural network designed to perform convolutional operations on graph-structured data. Unlike standard convolutional networks that operate on grid-like data such as images, GCNs can learn node embeddings by aggregating and propagating information from neighboring nodes in a graph. This makes them particularly effective for tasks like semi-supervised node classification, link prediction, and graph-level predictions. GCNs use spectral graph theory and a message-passing mechanism to perform graph convolutions, allowing the model to leverage both node features and the graph's connectivity structure.

![image](https://github.com/user-attachments/assets/fb7c8a06-d0f2-4150-91b0-e2a45083d3f3)


## About The Dataset
Cora dataset is a citation network that can be sourced from the Planetoid library.It is a standard benchmark for node classification tasks. In this graph nodes represent documents and edges represent citation links. Training, validation and test splits are given by binary masks. The entire dataset can be loaded from torch_geometric.datasets module.
### Cora Dataset Overview

| **Name** | **# Nodes** | **# Edges** | **# Features** | **# Classes** |
|----------|-------------|-------------|----------------|---------------|
| **Cora** | 2,708       | 10,556      | 1,433          | 7             |

## About GCN Methodology

Message propagtion in a 2 layer GCN can be illustrated using the following expression

$Z=\text{Softmax}(\hat{A}(ReLU(\hat{A} X W^{(0)})) W^{(1)})$

where $W^{(0)}, W^{(1)}$ are two trainable weight matrices,

$Z \in \mathbb{R}^{n \times c}$ where $c$ is the number of classes

$X \in \mathbb{R}^{n \times d}$ is the feature matrix.

$\hat{A} = \tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}}$

where $\tilde{A} = A + I$, $\tilde{D}= D + I$

$\hat{A}$ is a symetrically normalized adjacency matrix

A is the $n \times n$ adjacency matrix and D is the $n \times n$ node degree matrix

## Paper
The paper titled "Semi-supervised Classification with Graph Convolutional Networks" by Thomas Kipf and Max Welling is accessible [here](https://arxiv.org/abs/1609.02907).

## Python Libraries Used
- Pytorch
- torch_geometric
- Matplotlib
- Sklearn

## Results
- t-SNE plot of the embedding before training the model on dataset
![image](https://github.com/user-attachments/assets/554e3a7b-565f-45f1-804c-31346dd24753)


- t-SNE Visualization of Node Embeddings Using Model Predicted Labels Post-Training
  ![image](https://github.com/user-attachments/assets/0be9ba96-f947-4bcc-94f8-ffe3b5f515a5)


