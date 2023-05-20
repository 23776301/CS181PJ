import sys

if __name__ == '__main__':
    # Check if there are command-line arguments
    if len(sys.argv) > 1:
        # Access the command-line arguments starting from index 1
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

        # Print the command-line arguments
        print("Argument 1:", arg1)
        print("Argument 2:", arg2)
    else:
        print("No command-line arguments provided.")
