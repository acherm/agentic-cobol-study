FROM debian:bookworm
RUN apt-get update -qq && apt-get install -y -qq gnucobol4 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
