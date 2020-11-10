FROM ubuntu:18.04

ENV NAME_MB_SRCS_DIR connector_image/
ENV MB_DIR /opt/mb/

COPY .netrc /root/
RUN mkdir -p $MB_DIR/$NAME_MB_SRCS_DIR
WORKDIR $MB_DIR/$NAME_MB_SRCS_DIR

RUN apt-get -y update && \
    apt-get install -y curl pkg-config python-dev docker.io && \
    curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list && \
    curl https://bazel.build/bazel-release.pub.gpg | apt-key add - && \
    apt-get -y update && apt-get install -y bazel

CMD [ "./run" ]