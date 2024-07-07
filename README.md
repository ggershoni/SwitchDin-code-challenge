# SwitchDin VPP Revenue Calculator

This project implements a simple Virtual Power Plant (VPP) revenue calculator as part of a programming exercise for SwitchDin. It calculates the distribution of revenues for fictional VPPs based on battery discharge data.

## Project Structure
```
SwitchDin-code-challenge/
│
├── scripts/
│   └── (scripts to simplify common operations)
│
├── src/
│   └── (where the code is)
│
├── test/
│   └── (tests for checking the code)
│
├── Dockerfile
└── README.md
```

## Features

- Create VPPs with custom revenue sharing percentages and daily fees
- Add sites to VPPs
- Add batteries to sites
- Import discharge events from CSV files
- Generate revenue-sharing reports for specified VPPs and months

## Quick Start

We've included several scripts to make it easy to get started:

Make sure to make the scripts executable:
```bash
chmod +x scripts/*.sh
```

1. To build the Docker image:
```bash
./scripts/build.sh
```
2. To run the tests:
```bash
./scripts/run-tests.sh
```
3. To start an interactive shell in the container:
```bash
./scripts/shell.sh
```

## Usage

The main functionality is implemented in `src/commands.py`. To use the calculator:

1. Create a VPP using `create_vpp()`
2. Add sites to the VPP using `create_site()`
3. Add batteries to sites using `create_battery()`
4. Import discharge events from a CSV file using `import_events()`
5. Generate a revenue report using `create_report()`

## Design Decisions and Assumptions

1. **Global Variables**: The implementation uses global dictionaries (`vpps`, `sites`, `batteries`, `events`) for simplicity and to focus on the core logic. In a production environment, these would likely be replaced with a proper database.

2. **No Object-Oriented Design**: The implementation uses simple functions and data structures instead of classes. This was done to keep the code straightforward and focus on the core logic of the revenue calculations.

3. **In-Memory Storage**: All data is stored in memory. This is suitable for small datasets but would need to be replaced with persistent storage for larger, real-world applications.

4. **Minimal Error Handling**: The current implementation assumes valid inputs and doesn't include extensive error checking. In a production environment, more robust error handling and input validation would be necessary.

5. **Fixed Month Length**: The code assumes every month has 28 days for simplicity in calculating daily fees.

6. **CSV Format**: The implementation assumes a specific format for the input CSV file (NMI, DATE, ENERGY, TARIFF) and that all dates are valid and in ISO 8601 format.

7. **Revenue Distribution**: The code implements a specific revenue sharing model (80% to the site with the event, 20% distributed based on capacity) as per the exercise requirements.  It is not configurable at this stage.

## Running Tests

Tests are located in `tests`. To run the tests:

1. Ensure you're in the project root directory
2. Run the following command:
```bash
python -m unittest
```

Tests can also be run using the provided script:
```bash
./scripts/run-tests.sh
```

## Development

To make changes to the code:

1. Modify the files in the `test/` and `src/` directories
2. Rebuild the Docker image using `./scripts/build.sh`
3. Run the tests using `./scripts/run-tests.sh` to ensure everything still works

## Future Improvements

- Implement proper database storage
- Add more comprehensive error handling and input validation
- Create a more robust CLI or API interface
- Implement logging for better debugging and monitoring
- Consider using an OO approach for better encapsulation and extensibility
- Optimize calculations for larger datasets

## Note

This implementation is part of a time-limited programming exercise and is not intended for production use without further development and testing.