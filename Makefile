# I made some changes to support multiple environments. Basically, each environment is defined by a Dockerfile.<environment> or what I called ROLE
# So when you to make, you say make ROLE=name drun, or make ROLE=name dbuild or whatever.
# If you don't define a ROLE, there is a default, so what you are used to, no ROLE, will still work.

PRODUCT = trader
ROLE_DEFAULT=
ROLE := $(ROLE_DEFAULT) # example .dev
IMAGE_NAME = $(PRODUCT)
CONTAINER_NAME = $(IMAGE_NAME)
DOCKERFILE = Dockerfile$(ROLE)
VOLUMES = -v $(CURDIR):/app
HOSTS = --add-host=localhost:127.0.0.1

.PHONY = help build rebuild dev run shell bash stop links clean

help:
	@echo "Please use 'make <target> ROLE=<ROLE> if you don't specify role, the default will be \"$(ROLE)\" and will use Dockerfile.$(ROLE)"
	@echo "where <target> is one of"
	@echo "Please use 'make <target> ROLE=<role>' where <target> is one of"
	@echo "  build           build the docker image containing a redis cluster"
	@echo "  rebuild         rebuilds the image from scratch without using any cached layers"
	@echo "  run             run the built docker image"
	@echo "  restart         restarts the docker image"
	@echo "  bash            starts bash inside a running container."
	@echo "  clean           removes the tmp cid file on disk"
	@echo -n "and <ROLE> is a suffix of a Dockerfile in this directory, one of these: "
	@ls Dockerfile.*
	@echo "Example: make ROLE=dev .drun"

version: version.txt
	$(shell verstamp.sh -i $(git ls-files --modified))

build:  
	@echo "Building docker image..."
	docker build --rm=true -f $(DOCKERFILE) -t $(IMAGE_NAME) .

rebuild:
	@echo "Rebuilding docker image using: " 
	docker build --rm=true -f $(DOCKERFILE) --no-cache=true -t $(IMAGE_NAME) .

dev:    # runs container with interactive shell for debugging etc
	docker run --rm $(VOLUMES) $(PORTS) $(HOSTS) -it --entrypoint=/bin/bash --name $(CONTAINER_NAME) $(IMAGE_NAME) 

run:    # uses default entrypoint in container
	docker run --rm $(VOLUMES) $(PORTS) $(HOSTS) -it --name $(CONTAINER_NAME) $(IMAGE_NAME) 

shell: 
	docker exec -it $(CONTAINER_NAME) /bin/bash

bash:
	docker exec -it $(CONTAINER_NAME) /bin/bash

stop:
	-docker stop $(CONTAINER_NAME) 2>/dev/null
	-make clean

links:
	find . -type l -delete
	find . -mindepth 2 -maxdepth 2 -iname '*.py' -exec ln -s {} . \;

clean:
	#git clean -f .
	find . -iname '*~' -delete  # delete backup files
	find . -type l -delete              # delete symbolic links
	find . -type d -iname __pycache__ -exec rm -rf {} \; # delete python compiled cache

