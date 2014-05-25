# -*- coding: UTF-8 -*-
import json
from gensim import corpora, models 
from nltk import stem

st=stem.ISRIStemmer()

def make_dict(quran_file_name):
	document_list=[]
	quran_file=open(quran_file_name,'r')	
	line=json.loads(quran_file.readline())["sura"]
	for line in quran_file:
		aya_list=[]
		aya=st.stem(json.loads(line)["raw"])
		aya_list.append(aya)
		document_list.append([word for word in aya.split(" ")])
			
	dictionary=corpora.Dictionary(document_list)
	dictionary.save('quran_dict.dict')

	corpus = [dictionary.doc2bow(text) for text in document_list]
	
	corpora.MmCorpus.serialize('corpus.mm',corpus)


def topicmodeling(corpus_file_name,dict_file_name):
	dictionary = corpora.Dictionary.load(dict_file_name)
	corpus = corpora.MmCorpus(corpus_file_name)
	tfidf = models.TfidfModel(corpus)	
	corpus_tfidf = tfidf[corpus]
	lsi=models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

	corpus_list = lsi[corpus_tfidf]
	print lsi.print_topics(10)[3]
make_dict('quran.txt')
topicmodeling('corpus.mm','quran_dict.dict')
