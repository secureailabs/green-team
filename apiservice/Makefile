CONTAINER_NAME="apiservice"

# Run the api service in the background
run: build_container
	@docker run -dit --rm --name $(CONTAINER_NAME) -p 8000:8000 $(CONTAINER_NAME)

# Run the api service in the foreground and print the logs to the terminal
debug_run: build_container
	@docker run -it --rm --name $(CONTAINER_NAME) -p 8000:8000 -v apiservice:/apiservice $(CONTAINER_NAME)

# Build the container
build_container:
	@docker build -t $(CONTAINER_NAME) .

# Generate the docs for the api service
docs: run
# Create the generated folder if it doesn't exist
	@mkdir -p generated
	@cd generated && rm -f docs/openapi.json
# Download the API spec
	@wget http://127.0.0.1:8000/openapi.json -P generated/docs/ --no-check-certificate
# Rename all "_id" in openapi.json to "id"
# This is done because the openapi spec generates the keys of the models with "_id" instead of "id"
# It is not a bug, it happens because the openapi spec uses alias of the keys used in the models
# For example, if a model has a field called "id", it will be renamed to "_id", because that's what mongodb uses
# But _is is considered a private member so "id" is used instead
	@sed -i 's/\"_id\"/\"id\"/g' generated/docs/openapi.json
# Kill the api service
	@docker kill $(CONTAINER_NAME)

# Generate the python client for the api service
client: docs
	@rm -rf generated/py-client/
	@openapi-python-client generate --path generated/docs/openapi.json


# Stop the api service
stop:
	@docker kill $(CONTAINER_NAME)
