# Flight Finder

## Features

- Search for flights offers

## Local Usage

Clone the repo into your workspace.

```sh
./debug.sh
```

Upon successful image build, you can do a POST call to:

```sh
http://localhost:9000/2015-03-31/functions/function/invocations
BODY:
{
    "payload": [
        {
            "id": 1
        }
    ]
}
```

## Deployment to AWS

For deploying changes from your local...

```sh
## You can add this line to the end of the deploy.sh script to update the code or replace the image_uri to the one generated from the deploy script
aws lambda update-function-code --function-name ${FUNCTION_NAME} --image-uri $IMAGE_URI --publish
```
