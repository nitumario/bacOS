FROM gcc:11

WORKDIR /usr/src/app

COPY tests.json ./
COPY run_tests.sh ./
COPY cpp-files/ ./cpp-files/

ARG CPP_FILE

RUN g++ -o myprogram cpp-files/${CPP_FILE}

CMD ["./myprogram"]
