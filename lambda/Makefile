.PHONY: all venv clean zip

all: clean venv zip

venv: requirements.txt
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

clean:
	rm -f tfltree-lambda.zip
	rm -rf venv

zip: tfltree-lambda.zip zip-ffmpeg

zip-ffmpeg:
	cd ./ffmpeg; \
	if [ ! -f ./ffmpeg ]; \
	then \
		tar -xJf ffmpeg.xz; \
	fi; \
	zip -9 ../tfltree-lambda.zip ./ffmpeg ; \
	cd ..

tfltree-lambda.zip: venv
	zip -r9 tfltree-lambda.zip src/ -x *.pyc
	cd venv/lib/python3.7/site-packages; zip -r9 ../../../../tfltree-lambda.zip .
