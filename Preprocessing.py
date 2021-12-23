#!/usr/bin/python
import pickle
def load_pairs():
     '''
     Function to load the pairs calculated using DBSCAN + TSNE/PCA + Cointegration test
     '''
     infile = open('pair_dict_pca','rb')
     pair_dict_pca = pickle.load(infile)
     infile.close()

     infile = open('pair_dict_tsne','rb')
     pair_dict_tsne = pickle.load(infile)
     infile.close()

     pairs_joined = {**pair_dict_pca,**pair_dict_tsne}
     return pairs_joined 

def get_industry(ticker):
     '''
     Return industry to which the ticker belonds to
     '''
     df = pd.read_csv('Stock_data.csv')
     industry = df[df['Security Id'] ==ticker]['Industry']
     return industry.values[0]

def get_tuple_pairs(sorted_pairs):
     '''
     Returns a tuple with both tickers and industry they belong to
     '''

     pair_tuples = []
     for i in range(len(sorted_pairs)):
          ticker_1 = sorted_pairs[i][0][0]
          ticker_2 = sorted_pairs[i][0][1]
          temp = {ticker_1:get_industry(ticker_1),ticker_2:get_industry(ticker_2)} 
          pair_tuples.append(temp)
     return pair_tuples  

def save_dump(filename,var):
     outfile = open(filename,'wb')
     pickle.dump(var,outfile)
     outfile.close