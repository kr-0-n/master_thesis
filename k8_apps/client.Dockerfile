FROM alpine
RUN apk add --no-cache iperf3
RUN mkdir /logs
COPY ./iperf_client.sh /iperf_client.sh
RUN chmod +x /iperf_client.sh
CMD "/iperf_client.sh"
