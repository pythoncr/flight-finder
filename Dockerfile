FROM public.ecr.aws/lambda/python:3.8

RUN python3 -m pip install boto3 requests

COPY ./app/*.py  ./

CMD ["app.handler"]
