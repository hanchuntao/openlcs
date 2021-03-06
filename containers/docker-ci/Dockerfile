#FROM registry.access.redhat.com/ubi8/python-38:1-75
# This image is copied from the first image, to prevent upstream image changed
FROM quay.io/pelc/python-38:3.8.8

LABEL name="openlcs-ci" \
      maintainer="prodsec-dev-pelc@redhat.com" \
      summary="OpenLCS CI/CD" \
      description="OpenLCS ci-cd service in a container, will be auto deleted after 1 day"

USER 0

COPY ./requirements /tmp

# Return error when each pipe failed
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSk https://password.corp.redhat.com/RH-IT-Root-CA.crt \
        -o /etc/pki/ca-trust/source/anchors/Red_Hat_IT_Root_CA.crt && \
    curl -sSk https://engineering.redhat.com/Eng-CA.crt \
        -o /etc/pki/ca-trust/source/anchors/Eng-CA.crt && \
    update-ca-trust && \
    dnf config-manager --add-repo http://tito.eng.nay.redhat.com/yum/redhat/pelc/qe/rhel8/noarch \
        --add-repo http://download.eng.bos.redhat.com/brewroot/repos/brew-rhel-8/latest/x86_64/ && \
    dnf install --nogpgcheck --nodoc -y cpio-2.12 atool-0.39.0 && \
    dnf clean all && \
    # To make docker cache pip package, install dependencies
    pip install --upgrade pip && pip install -r /tmp/devel.txt && \
    # This download url is from currently ocp cluster console
    curl -k  https://downloads-openshift-console.apps.ocp-c1.prod.psi.redhat.com/amd64/linux/oc.tar | tar xf - -C /usr/local/bin/ && \
    pip install --upgrade pip && pip install -r /tmp/devel.txt && \
    # Link the site-packages to correct location, so that tox can find it when use current-env plugin
    # CI image site packages path is /usr/local/lib/python3.8/site-packages.
    # But tox will use one of ['/usr/local/lib64/python3.8/site-packages',
    # '/usr/local/lib/python3.8/site-packages', '/usr/lib64/python3.8/site-packages',
    # '/usr/lib/python3.8/site-packages'] as site packages path
    mkdir -p /usr/local/lib64/python3.8/ && \
    ln -s /opt/app-root/lib64/python3.8/site-packages /usr/local/lib64/python3.8/

# Apply patch for typecode, extractcode, packagedcode
COPY ./containers/patches/* /opt/app-root/lib64/python3.8/site-packages/
WORKDIR /opt/app-root/lib64/python3.8/site-packages/
RUN patch -p0 < magic2.patch && \
    patch -p0 < extract.patch && \
    patch -p0 < rpm.patch

WORKDIR /opt/app-root/src
USER 1001

# To avoid docker cache invaild , put this in the last
ARG quay_expiration
LABEL quay.expires-after=$quay_expiration
ENV REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt
