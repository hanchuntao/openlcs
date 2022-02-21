# https://catalog.redhat.com/software/containers/ubi8/python-38/5dde9cacbed8bd164a0af24a?container-tabs=overview
# FROM registry.access.redhat.com/ubi8/python-38:1-75
# This image is copied from the first image, to prevent upstream image changed
FROM quay.io/pelc/python-38:latest

MAINTAINER prodsec-dev-pelc <prodsec-dev-pelc@redhat.com>
LABEL name="pelc2" \
      maintainer="prodsec-dev-pelc@redhat.com" \
      summary="PELC2" \
      description="PELC2 service in a container"

USER 0

RUN dnf config-manager --add-repo http://tito.eng.nay.redhat.com/yum/redhat/pelc/qe/rhel8/noarch \
    --add-repo http://download.eng.bos.redhat.com/brewroot/repos/brew-rhel-8/latest/x86_64/ && \
    dnf install --nogpgcheck --nodoc -y  \
    cpio && \
    dnf clean all

RUN cd /etc/pki/ca-trust/source/anchors/ && \
    curl -skO https://password.corp.redhat.com/RH-IT-Root-CA.crt && \
    curl -skO https://engineering.redhat.com/Eng-CA.crt && \
    update-ca-trust

# Install the dependencies
RUN pip install --upgrade 'pip'

# To make docker could cache pip package, copy requirement firstly
COPY ./requirements /tmp
RUN pip install -r /tmp/base.txt

# To avoid docker cache invaild , put these code in the last part
ARG quay_expiration
LABEL quay.expires-after=$quay_expiration
ENV REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt
ENV HOME=/opt/app-root/src
ENV PYTHONUNBUFFERED 1

COPY . /opt/app-root/src
RUN mkdir -p /var/pelc/static /var/log/pelc/ /var/cache/ && \
    chmod a+rwX -R /var/log/pelc/ /var/cache/ /var/pelc/static  ${HOME}  /etc/passwd

RUN chmod a+x -R ${HOME}/containers/docker-pelc/bin/*

# Ordinary users
USER 1001


# Set the default command for the resulting image
CMD exec gunicorn "pelc.wsgi"