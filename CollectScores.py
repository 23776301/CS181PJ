import subprocess
import multiprocessing

NUM_RUNS = 100

def collect_score(score, scores):
    scores.append(score)

def run_game(output_queue):
    output_score = subprocess.check_output(['python', 'MainGame.py'])
    score = int(output_score.decode().strip())
    output_queue.put(score)

if __name__ == '__main__':
    scores = []
    output_queue = multiprocessing.Queue()

    processes = []
    for i in range(NUM_RUNS):
        
        print(f"Running game {i+1}/{NUM_RUNS}",end='\r',flush=True)
        process = multiprocessing.Process(target=run_game, args=(output_queue,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not output_queue.empty():
        score = output_queue.get()
        collect_score(score, scores)

    average_score = sum(scores) / len(scores)
    print("\nAverage score:", average_score)
    print("\nScores:\n", scores)