# syntax=docker/dockerfile:1.2

FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y openssh-client git

COPY app.py ${LAMBDA_TASK_ROOT}
COPY content_types.py ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN echo "$SSH_PRV_KEY" > /root/.ssh/id_rsa && \
    chmod 700 /root/.ssh/id_rsa

RUN --mount=type=ssh \
    pip install git+ssh://git@github.com/the-deep/deepl-pdf-extraction.git

CMD [ "app.process_docs" ]
