import subprocess
from joblib import Parallel, delayed
from multiprocessing import cpu_count

def collect_score(score, scores):
    scores.append(score)

def single_thread_with_gui(num_runs):
    scores = []
    for count in range(num_runs):            
        output_score = subprocess.check_output(['python', 'MainGame.py', '1']) # set zero to disable gui
        score = int(output_score.decode().strip())
        scores.append(score)
        # print(f" {count+1}/{num_runs} jobs finished!", end="\r")
        print(f" {count+1}/{num_runs} jobs finished! score = ",score)
    average_score = sum(scores) / len(scores)
    print("average score:", average_score)
    print("scores[%d]:" % count)
    print(scores)
    return scores

def run_game():
    output_score = subprocess.check_output(['python', 'MainGame.py', '0']) # set zero to disable gui
    score = int(output_score.decode().strip())
    # if count == num_runs - 1:
    #     print(f" {count+1}/{num_runs} jobs finished!")
    # else:
    #     print(f" {count+1}/{num_runs} jobs finished!", end="\r")
    return score

def multi_thread_without_gui(num_runs):
    scores = Parallel(n_jobs = 32)(delayed(run_game)() for _ in range(num_runs))
    print(scores)
    average_score = sum(scores) / len(scores)
    print("average score:", average_score)
    return scores

if __name__ == '__main__':
    # single_thread_with_gui(20)
    multi_thread_without_gui(200)
