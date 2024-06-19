NAME=embroidery-workspace

build:
	@if [ -z "$(shell docker images -q ${NAME})" ]; then make clean; fi
	@make -s Dockerfile.build

# track the build timestamp in Dockerfile.build so the Dockerfile is rebuilt when dependencies change
Dockerfile.build: Dockerfile */**/packages.txt */**/requirements.txt
	docker build -t ${NAME} .
	touch $@

clean:
	rm Dockerfile.build || true

RUN_ARGS=--rm -it  --volume ./:/src ${NAME}

lint: build
	@docker run $(RUN_ARGS) black .

shell: build
	@docker run $(RUN_ARGS) /bin/bash

up: build
	@docker run -p "8501:8501" $(RUN_ARGS) streamlit run app.py

dev:
	-tmux kill-session -t "${NAME}"
	tmux new-session -s "${NAME}" -d -n vi
	tmux send-keys -t "${NAME}:vi" "vi" Enter
	tmux new-window -t "${NAME}" -n shell "/bin/zsh"
	tmux new-window -t "${NAME}" -n build
	tmux send-keys -t "${NAME}:build" "make up" Enter
	tmux select-window -t "${NAME}:vi"
	tmux attach-session -t "${NAME}"
