.PHONY: install
install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	sudo mkdir -p /opt/wgm_wallpapers
	sudo cp requirements.txt /opt/wgm_wallpapers
	sudo cp wallpapers.py /opt/wgm_wallpapers
	sudo cp Makefile /opt/wgm_wallpapers
	sudo cp -r .venv /opt/wgm_wallpapers

.PHONY: run
run:
	. .venv/bin/activate && python wallpapers.py

.PHONY: uninstall
uninstall:
	sudo rm -rf /opt/wgm_wallpapers
