all: install fonts out

fonts:
	curl -L -o montserrat.tar.gz https://github.com/JulietaUla/Montserrat/archive/refs/tags/v7.222.tar.gz
	tar zxvf montserrat.tar.gz
	mv Montserrat-*/fonts/webfonts ./fonts
	rm -rf Montserrat-*
	rm montserrat.tar.gz

install:
	pip install -r requirements.txt

out:
	python generate.py