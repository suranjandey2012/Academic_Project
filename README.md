**NEXT WORD PREDICTOR USING LSTM NETWORK (Long Short Term Memory)**

**Overview**
- This model predicts the next word in an incomplete sentence, providing the five most likely next words based on the given input.
- Built using an LSTM neural network, the model is trained on a diverse vocabulary involving TREC news articles and even Bible texts to generate contextually relevant predictions,
  enhancing applications like text completion and language assistance.

**Deep Learning and Python Libraries Used**
- Pytorch
- tensorflow
- keras
- re (Python Regular Expression)

**Project Structure**
- Corpus.txt -> File contains the training corpus from TREC news articles and Kaggle datasets.
- Next_Word_Predictor_Train_Torch.ipynb - Colab file used to build and train the LSTM model on the corpus and store the tokenizer word index along with the trained model in order to reuse them while testing.
- Next_Word_Predictor_Test_Pytorch.ipynb - Colab file used to test our model.
- next_word_predictor.pth - Pytorch file used to save the trained model parameters.
- vocabulary.json - JSON file to save the tokenizer word index.

**Usage**
1. Load the Corpus on your notebook
2. Run the 'Next_Word_Predictor_Train_Torch.ipynb' file.
3. Load the saved .pth file and .json file on test notebook
4. Run the Next_Word_Predictor_Test_Pytorch.ipynb and check the resuts

**Results**
![image](https://github.com/user-attachments/assets/8da58db5-beee-4744-8c16-20026df88127)

   
 
  
