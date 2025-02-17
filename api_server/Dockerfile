# Use the official Rust image as the base image
FROM rust:latest

# Install protobuf compiler
RUN apt-get update && apt-get install -y protobuf-compiler


# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Cargo.toml and Cargo.lock files
COPY Cargo.toml Cargo.lock ./

# Copy the source code
COPY . .

# Build the Rust project
RUN cargo build --release

# Expose the port that the application will run on
EXPOSE 50051

# Run the compiled binary
CMD ["./target/release/api_server"]

