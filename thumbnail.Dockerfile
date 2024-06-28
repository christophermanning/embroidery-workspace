FROM alpine:3.19

# for compressing example images
RUN apk --no-cache add imagemagick

WORKDIR /src
