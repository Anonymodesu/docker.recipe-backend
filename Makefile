DOCKER_IMAGE := docker.recipe-backend
TIMESTAMP_FILE := .timestamp
DOCKER_IMAGE_FULL ?= $(DOCKER_IMAGE):$(shell cat $(TIMESTAMP_FILE))
DOCKER_IMAGE_LATEST ?= $(DOCKER_IMAGE):latest

$(TIMESTAMP_FILE):
	date '+%F-%H%M%S' > $(TIMESTAMP_FILE)

build: $(TIMESTAMP_FILE)
build:
	docker build \
		--no-cache \
		-t $(DOCKER_IMAGE_FULL) \
		-t $(DOCKER_IMAGE_LATEST) \
		./src

run:
	DOCKER_IMAGE=$(DOCKER_IMAGE_FULL) \
	docker compose up \
		--remove-orphans \
		--force-recreate \
		--renew-anon-volumes

test:
	DOCKER_IMAGE=$(DOCKER_IMAGE_FULL) \
	docker compose -f docker-compose.yml -f docker-compose.test.yml up \
		--build \
		--remove-orphans \
		--force-recreate \
		--renew-anon-volumes \
		--exit-code-from test

lint:
	docker compose -f docker-compose.lint.yml run \
		--user $(USER) \
		--env CHECK_ONLY=$(CHECK_ONLY) \
		--rm \
		lint


check-lint: CHECK_ONLY ?= true
check-lint: lint

.PHONY: build check-lint clean lint run test

clean:
	-docker rmi -f $(DOCKER_IMAGE_FULL) $(DOCKER_IMAGE_LATEST)
	-rm $(TIMESTAMP_FILE)
