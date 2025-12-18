FROM alpine:3.20
RUN apk add --no-cache iperf3
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update
RUN apk add hping3
RUN mkdir /logs
COPY ./iperf_client.sh /iperf_client.sh
RUN chmod +x /iperf_client.sh
CMD "/iperf_client.sh"
