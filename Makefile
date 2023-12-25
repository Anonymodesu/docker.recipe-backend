DOCKER_IMAGE := docker.recipe-backend
TIMESTAMP_FILE := .timestamp
DOCKER_IMAGE_FULL ?= $(DOCKER_IMAGE):$(shell cat $(TIMESTAMP_FILE))

$(TIMESTAMP_FILE):
	date '+%F-%H%M%S' > $(TIMESTAMP_FILE)

build: $(TIMESTAMP_FILE)
build:
	docker build -t $(DOCKER_IMAGE_FULL) .

run:
	DOCKER_IMAGE=$(DOCKER_IMAGE_FULL) \
	docker compose up \
		--remove-orphans \
		--force-recreate \
		--renew-anon-volumes \

test:
	DOCKER_IMAGE=$(DOCKER_IMAGE_FULL) \
	docker compose -f docker-compose.test.yml up \
		--remove-orphans \
		--force-recreate \
		--renew-anon-volumes \
		--exit-code-from test

lint: FIX := --fix
lint: check-lint

check-lint:
	echo 'TODO'

.PHONY: build check-lint clean lint run test

clean:
	-docker rmi $(DOCKER_IMAGE_FULL)
	-rm $(TIMESTAMP_FILE)
