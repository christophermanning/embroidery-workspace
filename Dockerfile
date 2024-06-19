FROM python:3.12-slim

RUN pip install --upgrade pip
RUN apt-get update

COPY patterns/ patterns

# Install Debian packages listed in any patterns/**/packages.txt file
RUN find ./ -name packages.txt -type f -print0 | xargs -0 -I {} sh -c 'cat {} | tr "\n" " " | xargs apt-get install -y'

# Install Python packages listed in any patterns/**/requirements.txt file
RUN find ./ -name requirements.txt -type f -print0 | xargs -0 -I {} sh -c 'pip install -r {}'

RUN rm -Rf patterns

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /src
