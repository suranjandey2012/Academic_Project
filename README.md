# Fake News Detection Using BERT Model

## Project Description
In this project, we tackle the problem of fake news detection using a variation of the pre-trained BERT model, bert-base-uncased. The model has been fine-tuned on a labeled dataset to perform a specific downstream classification task: predicting whether a news article is real or fake based on its title.

During fine-tuning, we froze the initial layers of the BERT model to retain the learned contextual embeddings from pre-training. On top of these frozen layers, we added custom fully connected layers designed for our classification task. These layers were trained on our dataset to adapt the model to the domain-specific task of fake news detection.

Our pipeline involves preprocessing the input data, tokenizing using the BERT tokenizer, fine-tuning the model, and evaluating its performance using relevant metrics. This approach leverages transfer learning to achieve robust classification performance


## About The Dataset
- ISOT Fake News Dataset contains labeled fake and real news articles. This dataset was collected from realworld sources; the truthful articles were obtained by crawling articles from Reuters.com (News website). As for the fake news articles, they were collected from different sources. The fake news articles were collected from unreliable websites that were flagged by Politifact (a fact-checking organization in the USA) and Wikipedia.
- The dataset consists of two CSV files. The first file named “True.csv” contains more than 12,600 articles from reuter.com. The second file named “Fake.csv” contains more than 12,600 articles from different fake news outlet resources. Each article contains the following information: article title, text, type and the date the article was published on.
- Url: https://www.kaggle.com/datasets/emineyetm/fake-news-detection-datasets/data
- ### Dataset Class Distribution:
  ![image](https://github.com/user-attachments/assets/89471f8f-50e6-47ae-bd9a-fdfd29562b55)

### About BERT base model (uncased)
- BERT is a Pretrained model on English language using a masked language modeling (MLM) objective. It is a transformers model pretrained on a large corpus of English data in a self-supervised fashion. This means it was pretrained on the raw texts only, with no humans labeling them in any way (which is why it can use lots of publicly available data) with an automatic process to generate inputs and labels from those texts. It was trained with two objectives Masked Language Modelling (MLM) and Next Sentence Prediction (NSP).
- Please refer https://arxiv.org/abs/1810.04805 for more information about BERT.
- BERT has originally been released in base and large variations, for cased and uncased input text. The uncased models also strips out an accent markers.
- Hugging Face URL: https://huggingface.co/google-bert/bert-base-uncased

  |         **Model**            | #Params  | **Language** |
  |------------------------------|----------|--------------|
  |   bert-base-uncased          |  110M    | English      |
 

 ### About Transfer Learning & Fine Tuning
 - Transfer Learning is a technique where the deep leaning models that has been already trained on large datasets are used to perform similar task on some other dataset while Fine Tuning involves training a Pre-trained model with huge number of parameters in the order of (millions or even billions) on a relatively smaller dataset for downstream tasks.
 - Training the model from scratch on a relatively small dataset can lead to overfitting. In order to avaoid that we have freezed the initial layers of the model and fine tuned our own layers during the training process.
  ![image](https://github.com/user-attachments/assets/7179443d-1f9d-417e-bc56-c10b8d0786ae)
### Model Architecture

![image](https://github.com/user-attachments/assets/805254ca-a214-4190-a0a8-99a6f988c5ab)

- We have used AdamW optimizer which is a standard optimizer for transfer learning tasks
- Negative Log Likelihood Loss has been used since we have used log softmax in our model for numerical stability.

### Python Libraries Used
- Pytorch
- transformers (Hugging Face)
- numpy
- pandas
- matplotlib
- sklearn
