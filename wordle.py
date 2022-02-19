# wordle solver

import sys

def decorate_result_char(status, character):
    if status == 'bad':
        return character
    color = {
        'positional': '\x1b[42m',
        'contains': '\x1b[43m',
    }[status]
    reset = '\x1b[0m'
    return f'{color}{character}{reset}'

class Hint:
    def __init__(self, character, position, status):
        self.character = character
        self.position = position
        self.status = status

    def match(self, name):
        if self.status == 'contains':
            if self.character not in name:
                return False
            if name[self.position] == self.character:
                return False
            return True
        elif self.status == 'bad':
            return self.character not in name
        else:
            return name[self.position] == self.character

    def __eq__(self, other):
        if other.character != self.character:
            return False
        if other.position != self.position:
            return False
        return True

    def __repr__(self):
        return f"'{str(self)}'"

    def __str__(self):
        return decorate_result_char(self.status, self.character)

def choose_try_answer(hints, try_log, dictionary):
    candidates = set()

    for name in set(dictionary) - set(try_log):
        if False not in [h.match(name) for h in hints]:
            candidates.add(name)

    if len(candidates) == 1:
        return list(candidates)[0], 1

    hint_chars = set([h.character for h in hints])
    chars = set(''.join(candidates))
    char_score = dict([(c, len([n for n in candidates if c in n])) for c in chars])

    name_score = []
    for name in candidates:
        score = sum([char_score[c] for c in name])
        name_score.append((name, score))

    trial, score = sorted(name_score, reverse=True, key=lambda i: i[1])[0]
    return trial, len(candidates)

def check_answer(answer, trial):
    result = []
    for i, c in enumerate(trial):
        if answer[i] == trial[i]:
            result.append(Hint(c, i, 'positional'))
        elif c in answer:
            result.append(Hint(c, i, 'contains'))
        else:
            result.append(Hint(c, i, 'bad'))
    return result

def solve(answer, dictionary):
    hints = []
    try_log = []

    for i in range(12):
        try_ans, total = choose_try_answer(hints, try_log, dictionary)
        try_log.append(try_ans)

        result = check_answer(answer, try_ans)

        result_decorated = ''
        result_plain = ''
        for r in result:
            result_decorated += str(r)
            result_plain += r.character
            hints.append(r)

        if sys.stdout.isatty():
            result_line = result_decorated
        else:
            result_line = result_plain
        print(f'try{i+1}: {result_line} ({total} candidates)')
        if try_ans == answer:
            return True

    return False

def main():
    with open('dictionary.txt') as f:
        dictionary = [w.strip() for w in f if len(w.strip()) == 5]

    for answer in dictionary:
        print(f'answer: {answer}')
        won = solve(answer, dictionary)
        if not won:
            break
        print()

if __name__ == '__main__':
    main()
