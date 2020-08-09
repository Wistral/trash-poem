from utils.hitokoto import gen_sentence
from utils.gtrans import gtrans
from subprocess import check_call
import re
from pathlib import Path
import random


action = Path('.') / '.github/workflows/main.yml'


def reset_schedule():
    with open(action) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        pattern = "\s+-\scron:\s'(\d+)\s(\d+)(.*)'"
        if re.match(pattern, line):
            print('match', line)
            m, h, _ = re.findall(pattern, line)[0]
            h = int(h)
            m = int(m)
            current_min = h*60+m
            interval = random.randint(4*60, 12*60)
            next_h, next_m = divmod(current_min+interval, 60)
            next_h %= 24
            if next_h == next_m:
                next_m += 1
                next_m %= 60
            print(f'{h}:{m} + {interval} ==> {next_h}:{next_m}')
            new_line = line.replace(str(h), str(
                next_h)).replace(str(m), str(next_m))
            print(repr(line), '==>', repr(new_line))
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

    nt = reset_schedule()
    check_call(f'git add poem.h {action}')
    commit_text = f'''Add sentence from {author}, detail: https://hitokoto.cn/?uuid={uuid}\nNext schedule time at {nt}'''
    print(commit_text)
    check_call(f'git commit -m "{commit_text}"')


if __name__ == '__main__':
    main()
