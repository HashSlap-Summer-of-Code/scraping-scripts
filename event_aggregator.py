def main():
    print("Welcome to the Event Aggregator!")
    input_file = input("Enter the path to the event data file: ")
    output_file = input("Enter the desired output file name: ")
    event_type = input("Enter the event type to aggregate (or 'all' for all types): ")

    # Example: Read and process the file dynamically
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            events = f.readlines()
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        return

    # Example aggregation logic
    aggregated = []
    for event in events:
        if event_type.lower() == 'all' or event_type in event:
            aggregated.append(event.strip())

    # Write results
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in aggregated:
            f.write(line + '\n')

    print(f"Aggregation complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()