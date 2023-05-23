import subprocess
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import matplotlib.pyplot as plt
def collect_score(score, scores):
    scores.append(score)

def single_thread_with_gui(num_runs):
    scores = []
    for count in range(num_runs):            
        output_score = subprocess.check_output(['python', 'MainGame.py', '0']) # set zero to disable gui
        print(f" {count+1}/{num_runs} jobs finished! output = ",output_score.decode().strip())
        score = int(output_score.decode().strip())
        scores.append(score)
        # print(f" {count+1}/{num_runs} jobs finished!", end="\r")
    average_score = sum(scores) / len(scores)
    print("average score:", average_score)
    print("scores:")
    print(scores)
    return scores

def run_game(num_cut):
    strd = str(num_cut)
    output_score = subprocess.check_output(['python', 'MainGame.py', '0',strd]) # set zero to disable gui
    score = int(output_score.decode().strip())
    # if count == num_runs - 1:
    #     print(f" {count+1}/{num_runs} jobs finished!")
    # else:
    #     print(f" {count+1}/{num_runs} jobs finished!", end="\r")
    return score

def multi_thread_without_gui(num_runs, num_cut):
    scores = Parallel(n_jobs = 4)(delayed(run_game)(num_cut) for _ in range(num_runs))
    # print(scores)
    average_score = sum(scores) / len(scores)
    print(f"num_cut = {num_cut}, average score = {average_score}.")
    return average_score

if __name__ == '__main__':
    num_cuts = range(1, 100,2)
    average_scores = Parallel(n_jobs=8)(delayed(multi_thread_without_gui)(200, num_cut) for num_cut in num_cuts)

    # Plotting the curve
    plt.plot(num_cuts, average_scores)
    plt.xlabel('num_cut')
    plt.ylabel('Average Score')
    plt.title('Average Score on each num_cut')
    plt.show()