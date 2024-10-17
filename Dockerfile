FROM python:3.12.4-slim

RUN pip install --upgrade pip
RUN apt-get update

# the .dockerignore file excludes all files except ones needed by commands below
# to ensure this COPY only reruns when those files change
COPY / /src

# Install Debian packages listed in any **/packages.txt file
RUN find ./ -name packages.txt -type f -print0 | xargs -0 -I {} sh -c 'cat {} | sed "/^#/d" | tr "\n" " " | xargs apt-get install -y'

# Install Python packages listed in any **/requirements.txt file
RUN find ./ -name requirements.txt -type f -print0 | xargs -0 -I {} sh -c 'pip install -r {}'

RUN mv /src/entrypoint.sh /usr/local/bin
RUN chmod u+x /usr/local/bin/entrypoint.sh

RUN rm -Rf /src

WORKDIR /src
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 8501
