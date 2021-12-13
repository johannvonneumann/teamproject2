import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle

#배경바꾸기...
# QPixmap bg('./images/background.jpg!d');
#
#        QPalette p(palette());
#        p.setBrush(QPalette::Background, bg);
#
#        setAutoFillBackground(true);
#        setPalette(p);
#책 배경
# from PyQt5.QtGui import *
# qPixmapVar = QPixmap()
# qPixmapVar.load("./images/BG2.jpg")


#책배경


form_window = uic.loadUiType('./book_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_reviews = pd.read_csv('./crawling_data/yes24_cleaned_contents.csv')
        self.Tfidf_matrix = mmread('./models/Tfidf_book_review.mtx').tocsr()
        self.embedding_model = Word2Vec.load('./models/Word2VecModel_yes24.model')
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.cmb_titles.addItem(title)

        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)


        self.cmb_titles.currentIndexChanged.connect(self.cmb_titles_slot)
        self.btn_recommend.clicked.connect(self.btn_recommend_slot)

    def cmb_titles_slot(self):
        title = self.cmb_titles.currentText()
        book_idx = self.df_reviews[self.df_reviews['titles']==title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[book_idx],
                                   self.Tfidf_matrix)
        recommendation_title = self.getRecommendation(cosine_sim)
        recommendation_title = '\n'.join(list(recommendation_title))
        self.lbl_recommend.setText(recommendation_title)


    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[1:11]
        bookidx = [i[0] for i in simScore]
        recBookList = self.df_reviews.iloc[bookidx]
        return recBookList['titles']

    def btn_recommend_slot(self):
        key_word = self.le_keyword.text()
        if key_word:
            if key_word in self.titles:
                book_idx = self.df_reviews[self.df_reviews['titles'] == key_word].index[0]
                cosine_sim = linear_kernel(self.Tfidf_matrix[book_idx],
                                           self.Tfidf_matrix)
                recommendation_title = self.getRecommendation(cosine_sim)
                recommendation_title = '\n'.join(list(recommendation_title))
                self.lbl_recommend.setText(recommendation_title)
            else:
                key_word = key_word.split()
                if len(key_word) > 20:
                    key_word = key_word[:20]
                if len(key_word) > 10:
                    sentence = ' '.join(key_word)
                    print(sentence)
                    sentence_vec = self.Tfidf.transform([sentence])
                    cosine_sim = linear_kernel(sentence_vec,
                                                                          self.Tfidf_matrix)
                    recommendation_titles = self.getRecommendation(cosine_sim)
                    recommendation_titles = '\n'.join(list(recommendation_titles))
                    self.lbl_recommend.setText(recommendation_titles)
                else:
                    sentence = [key_word[0]] * 11
                    try:
                        sim_word = self.embedding_model.wv.most_similar(key_word[0], topn=10)
                    except:
                        self.lbl_recommend.setText('제가 모르는 단어에요 ㅠㅠ')
                        return
                    words = []
                    for word, _ in sim_word:
                        words.append(word)
                    for i, word in enumerate(words):
                        sentence += [word] * (10-i)
                    sentence = ' '.join(sentence)
                    sentence_vec = self.Tfidf.transform([sentence])
                    cosine_sim = linear_kernel(sentence_vec,
                                               self.Tfidf_matrix)
                    recommendation_title = self.getRecommendation(cosine_sim)
                    recommendation_title = '\n'.join(list(recommendation_title))
                    self.lbl_recommend.setText(recommendation_title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())



