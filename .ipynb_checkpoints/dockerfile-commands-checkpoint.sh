# most dockerfile settings can be overrun by docker run (setting)
# in most (if not all) cases, spaces and backslashes need to be escaped when using in a value
# the less commands, the smaller the image

# base image (required)
FROM [--platform=<platform>] <image> [AS <name>]

# execute commands in a new layer on top of the new image
# as many times as you want, the rest builds on that
RUN (shell command)
# or
RUN ["executable", "param1", "param2"]  # exec format
# example with shell command in a different shell
RUN ["/bin/bash", "-c", "echo hello"]

# execute a command (ONLY ONCE) to provide defaults
# CMD is executed after build time 
# AT LEAST one CMD or ENTRYPOINT command is needed for a valid Dockerfile
CMD ["executable","param1","param2"]

# add a key-value label
LABEL version="1.0"

# listen to the specified port at runtime
EXPOSE (port) (possibly other ports or protocols)
# To actually publish the port when running the container,
# use the -p flag on docker run to publish and map one or more ports

# set environment variables
ENV (key)=(value)

# set environment variables that do not persist in the final image
ARG (key)=(value)
RUN (...)

# copy new files, directories or remote file URLs and add to image filesystem
# example valid use case: extract a local tar file into a specific directory in image
ADD (--chown=(user):(group)) (src) (dest)

# copy files or directories and add to container filesystem
# 99% of the time use COPY, not ADD!
COPY (--chown=(user):(group)) (src) (dest)

# use 1: basically CMD but more "strict", tougher to being overriden by user
# use 2: combination with CMD: 
# the CMD strings will be appended to ENTRYPOINT strings
# CMD strings can be easily overriden so they are basically default params to ENTRYPOINT command
ENTRYPOINT ["command", "param1", "param2"]

# create mount point and mark it as holding externally mounted volumes 
VOLUME ("/data")

# specify user id or user group 
USER (user(:group)) 
# or
USER (UID(:GID))

# set working directory for RUN, CMD, COPY etc. instructions
WORKDIR (/path/to/workdir) 
# can be used multiple times and relative paths will be appended
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
# outputs /a/b/c

# define variable that can be passed at build time with docker build
ARG (name)(=default_value)

# add a trigger instruction to be executed when the image is used to build another one
ONBUILD (instruction)(e.g. ADD ...)

# override default shell 
SHELL ["executable", "params"]