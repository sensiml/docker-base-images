FROM sensiml/base_image:latest
LABEL Author="Justin Moore <justin.moore@sensiml.com>"

ARG ARM_GCC_DOWNLOAD_LINK
ARG ARM_GCC_FOLDER_NAME
ARG ARM_GCC_VERSION

LABEL Description="Image for building arm-gcc project using ARM-gcc $ARM_GCC_VERSION"
RUN cd /usr/local && wget -qO- $ARM_GCC_DOWNLOAD_LINK | tar -xj

ENV PATH="/usr/local/$ARM_GCC_FOLDER_NAME/bin:${PATH}"
ENV TC_PATH="/usr/local/$ARM_GCC_FOLDER_NAME/bin"
ENV GNU_INSTALL_ROOT="/usr/local/$ARM_GCC_FOLDER_NAME"
