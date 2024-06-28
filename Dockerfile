FROM python:3.12-slim

RUN pip install --upgrade pip
RUN apt-get update

# a .dockerignore file excludes everything except requirements.txt and package.txt files
# so this reruns when those files change
COPY / /src

# Install Debian packages listed in any **/packages.txt file
RUN find ./ -name packages.txt -type f -print0 | xargs -0 -I {} sh -c 'cat {} | sed "/^#/d" | tr "\n" " " | xargs apt-get install -y'

# Install Python packages listed in any **/requirements.txt file
RUN find ./ -name requirements.txt -type f -print0 | xargs -0 -I {} sh -c 'pip install -r {}'

RUN rm -Rf /src

WORKDIR /src
