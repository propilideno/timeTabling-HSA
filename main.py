from src.input_reader import InputReader

if __name__ == "__main__":
    # Example usage
    file_path = "input/toy.ctt"
    inputReader = InputReader(file_path)
    timetable = inputReader.read_input_file()
