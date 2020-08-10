from utils.hitokoto import gen_sentence
from utils.gtrans import gtrans
import os
import re
from pathlib import Path
import random


action = Path('.') / '.github/workflows/main.yml'


def reset_schedule():
    with open(action) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        pattern = "(\s+-\scron:\s')(\d+)\s(\d+)(.*)"
        if re.match(pattern, line):
            print('match', line)
            L, m, h, R = re.findall(pattern, line)[0]
            h = int(h)
            m = int(m)
            current_min = h*60+m
            interval = random.randint(4*60, 12*60)
            next_h, next_m = divmod(current_min+interval, 60)
            next_h %= 24
            print(f'{h}:{m} + {interval} ==> {next_h}:{next_m}')
            p = "\s+-\scron:\s'(\d+\s\d+).*"
            new_line = re.sub(p, f'{L}{next_m} {next_h}{R}', line)
            print(repr(line), '\t==>\n', repr(new_line), sep='')
            lines[i] = new_line
            break
    with open(action, 'w') as f:
        f.writelines(lines)

    next_time = f'{next_h}:{next_m}'
    return next_time


def main():
    sentence, author, uuid = gen_sentence()

    with open('poem.h', 'a') as f:
        print(f'"{gtrans(sentence)}\\n"', file=f)

    # nt = reset_schedule()
    # schedule_comment = f'Next schedule time at {nt}'
    os.system(f'git add poem.h')
    commit_text = f'''Add sentence from {author}, detail: https://hitokoto.cn/?uuid={uuid}'''
    print(commit_text)
    os.system(f'git commit -m "{commit_text}"')


if __name__ == '__main__':
    main()
