import subprocess
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import matplotlib.pyplot as plt
from statistics import stdev

def collect_score(score, scores):
    scores.append(score)

def single_thread_with_gui(num_runs,num_cut):
    scores = []
    for count in range(num_runs):            
        output_score = subprocess.check_output(['python', 'MainGame.py', '10',str(num_cut)]) # set zero to disable gui
        print(f" {count+1}/{num_runs} jobs finished! score = ",output_score.decode().strip())
        score = float(output_score.decode().strip())
        scores.append(score)
        # print(f" {count+1}/{num_runs} jobs finished!", end="\r")
    average_score = sum(scores) / len(scores)
    print(f"num_cut = {num_cut}, average score = {average_score}, standard deviation: = {stdev(scores)}")
    print("scores:")
    print(scores)
    return scores

def run_game(num_cut):
    strd = str(num_cut)
    output_score = subprocess.check_output(['python', 'MainGame.py', '1',strd]) # set zero to disable gui
    score = float(output_score.decode().strip())
    # if count == num_runs - 1:
    #     print(f" {count+1}/{num_runs} jobs finished!")
    # else:
    #     print(f" {count+1}/{num_runs} jobs finished!", end="\r")
    # print(f"cut = {num_cut}, score = {score}")
    return score

def multi_thread_without_gui(num_runs, num_cut):
    scores = Parallel(n_jobs = 8)(delayed(run_game)(num_cut) for _ in range(num_runs))
    # print(scores)
    average_score = sum(scores) / len(scores)
    stv = stdev(scores)
    print(f"num_cut = {num_cut}, average score = {average_score}, standard deviation: = {stv}")
    return average_score, stv
def multi_plot():    
    average_scores = []
    score_stdevs = []
    nums = []
    # num_cuts = range(0, 31,5)
    # for num_cut in num_cuts:
    #     average_score, score_stdev = multi_thread_without_gui(100, num_cut)
    #     nums.append((num_cut))
    #     average_scores.append(average_score)
    #     score_stdevs.append(score_stdev)
        
    # num_cuts = range(31, 50,5)
    # for num_cut in num_cuts:
    #     average_score, score_stdev = multi_thread_without_gui(100, num_cut)
    #     nums.append((num_cut))
    #     average_scores.append(average_score)
    #     score_stdevs.append(score_stdev)
        
    num_cuts = range(0, 100,10)
    for num_cut in num_cuts:
        average_score, score_stdev = multi_thread_without_gui(100, num_cut)
        nums.append((num_cut))
        average_scores.append(average_score)
        score_stdevs.append(score_stdev)
    # Plotting the curves
    plt.plot(nums, average_scores, label='Average Score')
    plt.plot(nums, score_stdevs, label='Standard Deviation')
    plt.xlabel('num_cut')
    plt.ylabel('Value')
    plt.title('Average Score and Standard Deviation on num_cut')
    plt.legend()
    plt.show()

    
if __name__ == '__main__':
    single_thread_with_gui(20,20)
    multi_plot()

# num_cut = 1, average score = 21.91, standard deviation: = 67.42089940639829
# num_cut = 6, average score = 18.51, standard deviation: = 69.06613650785175
# num_cut = 11, average score = 18.92, standard deviation: = 67.5410357867831
# num_cut = 16, average score = 18.71, standard deviation: = 69.2585982701313
# num_cut = 21, average score = 14.8, standard deviation: = 70.46397460526703
# num_cut = 26, average score = 30.91, standard deviation: = 57.732244198558746
# num_cut = 31, average score = 25.06, standard deviation: = 63.050536088205476
# num_cut = 36, average score = 34.35, standard deviation: = 52.54173425367532
# num_cut = 41, average score = 25.64, standard deviation: = 59.40539036182158
# num_cut = 46, average score = 22.38, standard deviation: = 60.04960575653392
# num_cut = 51, average score = 5.63, standard deviation: = 68.2786410840376
# num_cut = 56, average score = 8.72, standard deviation: = 63.68817342602498
# num_cut = 61, average score = 16.13, standard deviation: = 57.4903865481399
# num_cut = 66, average score = -3.11, standard deviation: = 66.18338388923841
# num_cut = 71, average score = 8.95, standard deviation: = 58.05855195012578
# num_cut = 76, average score = -8.45, standard deviation: = 63.23219596108146
# num_cut = 81, average score = -22.01, standard deviation: = 70.60453171709234
# num_cut = 86, average score = -11.48, standard deviation: = 64.84550092256971
# num_cut = 91, average score = -15.5, standard deviation: = 69.59079528126394
# num_cut = 96, average score = -23.08, standard deviation: = 70.74447974323802


# num_cut = 0, average score = -91.67, standard deviation: = 84.23836490110739
# num_cut = 5, average score = -102.12, standard deviation: = 74.87609698021058
# num_cut = 10, average score = -87.37, standard deviation: = 84.01607049255577
# num_cut = 15, average score = -91.2, standard deviation: = 84.56591476117278
# num_cut = 20, average score = -96.41, standard deviation: = 81.59150468255648
# num_cut = 25, average score = -94.66, standard deviation: = 91.72204608148326
# num_cut = 30, average score = -107.83, standard deviation: = 89.43843376503993
# num_cut = 31, average score = -99.53, standard deviation: = 92.95230176838228
# num_cut = 32, average score = -107.89, standard deviation: = 91.42727915527932
# num_cut = 33, average score = -65.08, standard deviation: = 106.23298960684521
# num_cut = 34, average score = -91.29, standard deviation: = 100.39239125661976
# num_cut = 35, average score = -76.23, standard deviation: = 107.73507114935023
# num_cut = 36, average score = -77.99, standard deviation: = 108.81060322292755
# num_cut = 37, average score = -86.86, standard deviation: = 111.61803735340567
# num_cut = 38, average score = -79.19, standard deviation: = 107.39502226863593
# num_cut = 39, average score = -87.11, standard deviation: = 102.65032288248678
# num_cut = 40, average score = -69.18, standard deviation: = 109.86542548578109
# num_cut = 41, average score = -68.14, standard deviation: = 111.69339526334825
# num_cut = 42, average score = -78.7, standard deviation: = 107.66591612460043
# num_cut = 43, average score = -81.71, standard deviation: = 107.7712031213451
# num_cut = 44, average score = -67.34, standard deviation: = 112.58238016329342
# num_cut = 45, average score = -73.98, standard deviation: = 110.43650582204155
# num_cut = 46, average score = -80.16, standard deviation: = 109.42371725997019
# num_cut = 47, average score = -51.27, standard deviation: = 112.07463737810774
# num_cut = 48, average score = -61.59, standard deviation: = 111.17554550885693
# num_cut = 49, average score = -72.77, standard deviation: = 109.86252704396003
# num_cut = 50, average score = -49.47, standard deviation: = 110.69445206139157
# num_cut = 60, average score = -41.0, standard deviation: = 109.86198872065154
# num_cut = 70, average score = -40.98, standard deviation: = 106.21266830793259
# num_cut = 80, average score = -16.99, standard deviation: = 86.34327718561252
# num_cut = 90, average score = -5.78, standard deviation: = 77.33105796025635