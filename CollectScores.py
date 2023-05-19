import subprocess

NUM_RUNS = 100
def collect_score(score,scores):
    scores.append(score)
    
if __name__ == '__main__':
    NUM_RUNS = 100
    scores = []
    for _ in range(NUM_RUNS):
        output_score = subprocess.check_output(['python', 'MainGame.py'])
        score = int(output_score.decode().strip())
        scores.append(score)
    average_score = sum(scores) / len(scores)
    print("average score:",average_score)   
    print("scores[NUM_RUNS]:")
    print(scores)