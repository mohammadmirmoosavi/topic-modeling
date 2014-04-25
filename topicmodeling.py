# -*- coding: UTF-8 -*-
import json
from gensim import corpora, models 
from nltk import stem

st=stem.ISRIStemmer()

def make_dict(page_list):
	document_list=[]
	for quran_file_name in page_list:
		word_list=[]
		quran_file=open(quran_file_name,'r') 	# open quran_file
		ayeh_list=[]				# ayeh_list is a list of ayeha	
		for line in quran_file:
			ayeh_list.append(st.stem(json.loads(line)["text"])) #processing only arabic text ayeh_list is a list include "ayeha"
		
		word_list=[[word for word in text.split()] for text in ayeh_list]
		word_list=sum(word_list,[])
		document_list.append(word_list)
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
	print lsi.print_topics(10)
make_dict(['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10'])
topicmodeling('corpus.mm','quran_dict.dict')
