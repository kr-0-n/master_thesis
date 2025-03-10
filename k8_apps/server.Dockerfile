FROM alpine
RUN apk add --no-cache iperf3
RUN mkdir /logs
COPY ./iperf_server.sh /iperf_server.sh
RUN chmod +x /iperf_server.sh
CMD "/iperf_server.sh"