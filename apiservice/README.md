# Make best use of poetry
poetry manages dependencies and virtual environments for Python projects. It is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

## Installation
```bash
pip3 install poetry
```

## Develop apiservices
```bash
# Create a new virtual environment in the same folder and install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run apiservices
python3 apiservices.py
```

## Build apiservices
To deliver api services as a wheel package, you need to build it first. The wheel package is a built distribution format that can be installed using pip. It is the preferred format for distributing Python libraries.
```bash
# Build apiservices
poetry build

# Install apiservices
pip3 install dist/apiservices-0.1.0-py3-none-any.whl
```

## Add new dependencies
Dependencies that are common in dev and production can be installed using the following command.
Look at the pyproject.toml file to see the dependencies and better understanding.
```bash
# Add new dependencies
poetry add <package_name>

# Add new dependencies for development
poetry add <package_name> --group dev
```

## Api Writing Guidelines
- Endpoint decorator should be defined in the format '@api.route('/<resource_name>/<id>/<sub_resource>/<id>.../?query_params')'
- APIs should return same type of object for every success response, the response codes can be different though
- Endpoint decorator should contain response_model if the response is a json object

Example of a good endpoint decorator:
```python
@router.get(
    path="/data-federations",
    description="Get list of all the data federations",
    response_description="List of data federations",
    response_model=GetMultipleDataFederation_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_all_data_federations",
)
async def get_all_data_federations(
    data_submitter_id: Optional[PyObjectId] = Query(default=None, description="UUID of Data Submitter in the data federation"),
    researcher_id: Optional[PyObjectId] = Query(default=None, description="UUID of Researcher in the data federation"),
    dataset_id: Optional[PyObjectId] = Query(default=None, description="UUID of Dataset in the data federation"),
    current_user: TokenData = Depends(get_current_user),
) -> GetMultipleDataFederation_Out:
```
