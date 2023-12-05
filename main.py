from src.input_reader import InputReader
from src.hsa import HSA
import time

if __name__ == "__main__":
    # Example usage
    start_time = time.time()

    file_path = "input/toy.ctt"
    inputReader = InputReader(file_path)
    timetable = inputReader.read_input_file()
    hsa = HSA(timetable)
    hsa.solve()

    

    print("--- %s seconds ---" % (time.time() - start_time))
