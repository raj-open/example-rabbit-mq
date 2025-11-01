# ----------------------------------------------------------------
# BUILD STAGE - bedrock / pull image
# ----------------------------------------------------------------

FROM python:3.12-slim AS stage-bedrock

# ----------------------------------------------------------------
# BUILD STAGE - set up system
# ----------------------------------------------------------------

# --------------------------------
# SETUP
# --------------------------------

# prevent interactive prompts
USER root
ENV DEBIAN_FRONTEND=noninteractive

ARG USER="basicuser"

# update PATH
ENV PATH="/home/${USER}/.local/bin:/root/.cargo/bin:/usr/local/bin:/root/.local/bin:/usr/sbin:$PATH"

# --------------------------------
# INSTALL TOOLS
# --------------------------------

# install utils
RUN apt-get update
RUN apt-get install -y --no-install-recommends sudo
RUN apt-get install -y --no-install-recommends ca-certificates
RUN apt-get install -y --no-install-recommends curl
RUN apt-get install -y --no-install-recommends xz-utils
RUN apt-get install -y --no-install-recommends watch
RUN apt-get install -y --no-install-recommends cron
RUN apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y --no-install-recommends gnupg
# RUN apt-get install -y --no-install-recommends make
# RUN apt-get install -y --no-install-recommends vim
RUN apt-get install -y --no-install-recommends git
# RUN apt-get install -y --no-install-recommends pkg-config
# RUN apt-get install -y --no-install-recommends clang
# RUN apt-get install -y --no-install-recommends libssl-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# install Justfile tool directly
ARG JUST_VERSION="1.40.0"
RUN curl --proto '=https' --tlsv1.2 -sSL \
    https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-x86_64-unknown-linux-musl.tar.gz \
    -o /tmp/just.tar.gz
RUN mkdir -p /tmp/casey \
    && tar -xzf /tmp/just.tar.gz -C /tmp/casey
RUN chmod +x /tmp/casey/just \
    && mv /tmp/casey/just /usr/local/bin
RUN rm -f /tmp/just.tar.gz \
    && rm -rf /tmp/casey

RUN apt-get purge -y \
        gnupg \
        # pkg-config \
        # clang \
        # libssl-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ping tools
RUN which python3 && python3 --version
RUN which pip3 && pip3 --version
RUN which just && just --version

# --------------------------------
# SYSTEM SETTING
# --------------------------------

# ensures package installation (pip, cargo, etc.) can obtain packages via git
RUN git config --global http.sslVerify false

# set system timezone so that CRON jobs behave as expected
ARG TIMEZONE
RUN ln -snf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone

# --------------------------------
# MARK STAGE
# --------------------------------

FROM stage-bedrock AS stage-system

# ----------------------------------------------------------------
# BUILD STAGE - set up users
# ----------------------------------------------------------------

# --------------------------------
# USERS
# --------------------------------

ARG USER="basicuser"
ARG GROUP="basicgroup"
ARG WD="//home/${USER}/app"

# create group + user within this group
USER root
RUN groupadd -r "${GROUP}"
RUN useradd -r -g "${GROUP}" -m "${USER}"

# create the workspace + add permissions (this will need to be performed again later)
USER root
RUN mkdir -p "${WD}"
RUN chown -R "${USER}:${GROUP}" "${WD}"
RUN chmod -R g+rwX "${WD}"

# --------------------------------
# BASH PROFILE / ENV
# --------------------------------

USER "${USER}"
RUN touch "//home/${USER}/.bash_profile"
RUN echo "export PATH=\"/root/.local/bin:\$PATH\""         >> "//home/${USER}/.bash_profile"
RUN echo "export PATH=\"/usr/local/bin:\$PATH\""           >> "//home/${USER}/.bash_profile"
RUN echo "export PATH=\"/home/${USER}/.local/bin:\$PATH\"" >> "//home/${USER}/.bash_profile"
# set ensure secrets are loaded into bash sessions upon execution
RUN echo 'source /run/secrets/credentials' >> "//home/${USER}/.bash_profile"

# --------------------------------
# MARK STAGE
# --------------------------------

FROM stage-system AS stage-userprofile

# ----------------------------------------------------------------
# BUILD STAGE - base = set up repo
# ----------------------------------------------------------------

# --------------------------------
# COPY FILES
# --------------------------------

# now set up workspace
USER root
WORKDIR "${WD}"
COPY . .

# --------------------------------
# MARK STAGE
# --------------------------------

FROM stage-userprofile AS stage-base

# ----------------------------------------------------------------
# BUILD STAGE - build
# ----------------------------------------------------------------

# --------------------------------
# STEPS
# --------------------------------

# NOTE: we *do not* have access to run-time env vars!
ARG PYTHON_PATH

USER root
RUN chown -R "${USER}:${GROUP}" "${WD}"
RUN chmod -R g+rwX "${WD}"

USER "${USER}"
RUN just build

# --------------------------------
# MARK STAGE
# --------------------------------

FROM stage-base AS stage-build

# ----------------------------------------------------------------
# DEFAULT COMMAND
# ----------------------------------------------------------------

CMD ["bash", "--login", "-i"]
