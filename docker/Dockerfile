# Use a base image with gcc
FROM gcc:11

# Set the working directory
WORKDIR /usr/src/app

# Copy the test file and script into the container
COPY tests.json ./
COPY run_tests.sh ./
COPY cpp-files/ ./cpp-files/

# Set environment variable for the C++ file to compile
ARG CPP_FILE

# Compile the C++ program
RUN g++ -o myprogram cpp-files/${CPP_FILE}

# Run the compiled program by default
CMD ["./myprogram"]
