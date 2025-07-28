all: run plot
run:
    cargo run -r > data.csv
plot:
    python3 ./plot.py
