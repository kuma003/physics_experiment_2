import pandas as pd
import os


def read_datafile(file_path):
    """
    Reads a data file and returns a DataFrame.
    Args:
        file_path (str): The path to the data file (space separated).
    Returns:
        pd.DataFrame: The data as a DataFrame.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # remove comments with #
    with open(file_path, "r") as file:
        lines = file.readlines()
    with open(file_path, "w") as file:
        for line in lines:
            if not line.startswith("#"):
                file.write(line)

    try:
        data = pd.read_csv(file_path, sep="  ", header=None, engine="python")
    except Exception as e:
        raise ValueError(f"Error reading the file: {e}")

    return data


if __name__ == "__main__":
    # read command line arguments
    import sys

    if len(sys.argv) != 2:
        print("Usage: python read_datafile.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]

    try:
        df = read_datafile(file_path)
        print(df.head())
        # calc average for each column
        avg = df.mean()
        print("Average for each column:")
        print(avg)

    except Exception as e:
        print(e)
