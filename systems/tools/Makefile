
all: errant m2scorer jfleg

errant:
	git clone https://github.com/chrisjbryant/errant
m2scorer:
	git clone https://github.com/nusnlp/m2scorer
jfleg:
	git clone https://github.com/keisks/jfleg

marian-dev:
	git clone https://github.com/marian-nmt/marian-dev
	mkdir -p marian-dev/build
	cd marian-dev/build && cmake .. -DUSE_SENTENCEPIECE=on && make -j8

pip:
	pip3 install --upgrade nltk spacy==1.9.0
	python3 -m spacy download en

.PHONY: all
