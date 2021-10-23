FROM public.ecr.aws/lambda/python:3.8

# Set the container timezone
ENV TZ=America/Toronto
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN yum -y install gcc python3-devel mysql-devel libevent-devel
RUN python3 -m pip install boto3 requests

COPY ./app/*.py  ./

CMD ["app.handler"]
