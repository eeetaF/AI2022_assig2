import math
import random

from mido import MidiFile, MidiTrack, Message
from music21 import *


class Note:
    def __init__(self, int_note, velocity, time):
        self.int_note = int_note
        self.velocity = velocity
        self.time = time


class Chord:
    def __init__(self, note1, note2, note3, score, velocity):
        self.notes_list = [note1, note2, note3]
        self.score = score
        self.velocity = velocity


def define_tonic(melody_key_name):
    # defines the tonic note
    tonic_note = 12
    if melody_key_name == 'C':
        tonic_note = 0
    elif melody_key_name == 'C#':
        tonic_note = 1
    elif melody_key_name == 'D':
        tonic_note = 2
    elif melody_key_name == 'D#':
        tonic_note = 3
    elif melody_key_name == 'E':
        tonic_note = 4
    elif melody_key_name == 'F':
        tonic_note = 5
    elif melody_key_name == 'F#':
        tonic_note = 6
    elif melody_key_name == 'G':
        tonic_note = 7
    elif melody_key_name == 'G#':
        tonic_note = 8
    elif melody_key_name == 'A':
        tonic_note = 9
    elif melody_key_name == 'A#':
        tonic_note = 10
    elif melody_key_name == 'B':
        tonic_note = 11
    return tonic_note


def parse_notes(mid1):
    # parses notes from midi file
    notes = []
    for i, track in enumerate(mid1.tracks):
        for msg in track:
            if msg.type == 'note_on':
                if msg.time == 0:
                    notes.append(Note(msg.note, msg.velocity, 0))
                else:
                    notes.append(Note(None, msg.velocity, msg.time))
                    notes.append(Note(msg.note, msg.velocity, 0))
            if msg.type == 'note_off':
                notes[len(notes) - 1].time = msg.time
    return notes


def fit_test(current_chord, tonic_note, notes_set, notes_during_chord, last_chord, mode):
    # evaluates the score of the chord

    # if a tonic note found, +20
    # if a note from the whole melody found, +12
    # if a note from currently played melody, +25
    chord_notes = current_chord.notes_list
    for current_note in chord_notes:
        if current_note == tonic_note:
            current_chord.score += 20
        elif notes_set[current_note]:
            current_chord.score += 12

        if current_note in notes_during_chord:
            current_chord.score += 25

    chord_notes.sort()
    interval1 = chord_notes[1] - chord_notes[0]
    interval2 = chord_notes[2] - chord_notes[1]
    interval3 = chord_notes[2] - chord_notes[0]

    # we want to end with a tonic accord
    if last_chord:
        if mode == 'major':
            if interval1 == 4 and interval2 == 3 and chord_notes[0] % 12 == tonic_note:
                current_chord.score += 100
            elif interval1 == 3 and interval2 == 4 and chord_notes[0] % 12 == tonic_note:
                current_chord.score += 20
        else:
            if interval1 == 3 and interval2 == 4 and chord_notes[0] % 12 == tonic_note:
                current_chord.score += 100
            elif interval1 == 4 and interval2 == 3 and chord_notes[0] % 12 == tonic_note:
                current_chord.score += 20

    # intervals evaluation
    if interval1 == 1:
        current_chord.score -= 100
    elif interval1 == 2:
        current_chord.score -= 30
    elif interval1 == 3:
        current_chord.score += 4
    elif interval1 == 4:
        current_chord.score += 4
    elif interval1 == 6 or interval1 == 7:
        current_chord.score -= 1
    elif interval1 == 8:
        current_chord.score -= 2
    elif interval1 == 10:
        current_chord.score -= 30
    elif interval1 == 11:
        current_chord.score -= 100

    if interval2 == 1:
        current_chord.score -= 100
    elif interval2 == 2:
        current_chord.score -= 30
    elif interval2 == 3:
        current_chord.score += 4
    elif interval2 == 4:
        current_chord.score += 4
    elif interval2 == 6 or interval2 == 7:
        current_chord.score -= 1
    elif interval2 == 8:
        current_chord.score -= 2
    elif interval2 == 10:
        current_chord.score -= 30
    elif interval2 == 11:
        current_chord.score -= 100

    if interval3 == 1:
        current_chord.score -= 100
    elif interval3 == 2:
        current_chord.score -= 30
    elif interval3 == 3:
        current_chord.score -= 10
    elif interval3 == 4:
        current_chord.score -= 5
    elif interval3 == 5:
        current_chord.score -= 1
    elif interval3 == 7:
        current_chord.score += 4
    elif interval3 == 8:
        current_chord.score += 2
    elif interval3 == 9:
        current_chord.score += 1
    elif interval3 == 10:
        current_chord.score -= 30
    elif interval3 == 11:
        current_chord.score -= 100


def select(chords):
    # tournament selection algorithm
    selected = []
    for _ in range(300):
        # 4 random parents
        a = random.randint(0, 299)
        b = random.randint(0, 299)
        c = random.randint(0, 299)
        d = random.randint(0, 299)
        while (a == b) or (a == c) or (b == c) or (a == d) or (b == d) or (c == d):
            b = random.randint(0, 299)
            c = random.randint(0, 299)
            d = random.randint(0, 299)
        temp = [chords[a], chords[b], chords[c], chords[d]]
        # best is chosen
        temp = sorted(temp, key=lambda x: x.score, reverse=True)
        # add a child to the next generation
        selected.append(temp[0])
    return selected


def check_intersection(chord1, chord2):
    # True if intersection found
    if (chord1.notes_list[0] == chord1.notes_list[1] or
            chord1.notes_list[1] == chord1.notes_list[2] or
            chord1.notes_list[0] == chord1.notes_list[2] or
            chord2.notes_list[0] == chord2.notes_list[1] or
            chord2.notes_list[1] == chord2.notes_list[2] or
            chord2.notes_list[0] == chord2.notes_list[2]):
        return True
    return False


def crossover(selected):
    # for every pair of chords
    for i in range(149):
        # skip 1/8 of iterations
        if random.randint(0, 7) == 0:
            continue
        chord1 = selected[i]
        chord2 = selected[i + 149]
        # switch one random note in chord1 with one random note in chord2
        random_position1 = random.randint(0, 2)
        random_position2 = random.randint(0, 2)
        note_from_chord1 = chord1.notes_list[random_position1]
        note_from_chord2 = chord2.notes_list[random_position2]
        chord1.notes_list[random_position1] = note_from_chord2
        chord2.notes_list[random_position2] = note_from_chord1
        # if there is intersection, switch back
        if check_intersection(chord1, chord2):
            chord1.notes_list[random_position1] = note_from_chord1
            chord2.notes_list[random_position2] = note_from_chord2

    return selected


def mutation(selected):
    # for every chord in selected
    for i in range(299):
        # skip 1/4 of chords
        if random.randint(0, 3) == 0:
            continue
        current_chord = selected[i]
        # replace a random note in the chord with a random note
        random_position = random.randint(0, 2)
        random_note = random.randint(0, 11)
        previous_note = current_chord.notes_list[random_position]
        current_chord.notes_list[random_position] = random_note
        # if the chord is not valid, revert the change
        if (current_chord.notes_list[0] == current_chord.notes_list[1] or
                current_chord.notes_list[1] == current_chord.notes_list[2] or
                current_chord.notes_list[0] == current_chord.notes_list[2]):
            current_chord.notes_list[random_position] = previous_note

    return selected


def save_mid(mid, chords, ticks_per_beat, name):
    mid.tracks.append(MidiTrack())
    mid.tracks.append(MidiTrack())
    mid.tracks.append(MidiTrack())

    for i in range(len(chords)):
        mid.tracks[2].append(Message("note_on", note=chords[i].notes_list[0], velocity=chords[i].velocity, time=0))
        mid.tracks[2].append(
            Message("note_off", note=chords[i].notes_list[0], velocity=chords[i].velocity, time=ticks_per_beat))

        mid.tracks[3].append(Message("note_on", note=chords[i].notes_list[1], velocity=chords[i].velocity, time=0))
        mid.tracks[3].append(
            Message("note_off", note=chords[i].notes_list[1], velocity=chords[i].velocity, time=ticks_per_beat))

        mid.tracks[4].append(Message("note_on", note=chords[i].notes_list[2], velocity=chords[i].velocity, time=0))
        mid.tracks[4].append(
            Message("note_off", note=chords[i].notes_list[2], velocity=chords[i].velocity, time=ticks_per_beat))

    mid.save(name)


def main():
    # work with mido and music21 libraries
    mid1 = MidiFile('input0.mid')
    notes = parse_notes(mid1)
    ticks_per_beat = mid1.ticks_per_beat

    mid2 = converter.parse('input0.mid')
    melody_key_name = mid2.analyze('key').tonic.name
    melody_key_mode = mid2.analyze('key').mode
    tonic_note = define_tonic(melody_key_name)

    # notes_set contains a set of all notes played in the melody
    notes_set = []
    for _ in range(12):
        notes_set.append(False)

    # set up lowest_note of the melody, total_time of all played notes, and notes_set of the melody
    lowest_note = 100
    total_time = 0
    for n in notes:
        total_time += n.time
        if n.int_note is not None:
            if n.int_note < lowest_note:
                lowest_note = n.int_note
            notes_set[n.int_note % 12] = True

    # make lowest_note lower so that the interval between the highest chord note and the lowest_note is at least 3
    lowest_note -= 3
    
    # start_note contains the lowest possible note of all the chords
    start_note = (lowest_note // 12) * 12 - 12
    if start_note < 0:
        start_note = 0

    # generate n_of_chords chords
    n_of_chords = math.ceil(total_time / ticks_per_beat)
    i = 0
    velocity = notes[0].velocity
    best_chords = []
    for k in range(n_of_chords):
        lowest_note_during_chord = 100
        chords = []
        notes_during_chord = []
        # temp_time - time of chord
        temp_time = ticks_per_beat

        # fitting note lengths to the chords, filling list of played notes during the chord, and finding the lowest note
        while temp_time > 0:
            if i >= len(notes):
                break
            if notes[i].int_note is not None:
                notes_during_chord.append(notes[i].int_note % 12)
                if notes[i].int_note < lowest_note_during_chord:
                    lowest_note_during_chord = notes[i].int_note
            temp_time -= notes[i].time
            notes[i].time = 0
            i += 1

        # if temp_time < 0 then we have subtracted too much from a long note
        if temp_time < 0:
            notes[i - 1].time = -temp_time
            i -= 1

        # random chords generation & score calculation via fit_test
        for _ in range(300):
            a = random.randint(0, 11)
            b = random.randint(0, 11)
            c = random.randint(0, 11)
            while (a == b) or (a == c) or (b == c):
                b = random.randint(0, 11)
                c = random.randint(0, 11)
            current_chord = Chord(a, b, c, 0, velocity)
            fit_test(current_chord, tonic_note, notes_set, notes_during_chord,
                     k - 1 == n_of_chords, melody_key_mode)
            chords.append(current_chord)

        # genetic algorithm
        selected = []
        for _ in range(3):
            selected = select(chords)
            selected = crossover(selected)
            selected = mutation(selected)
            for z in range(299):
                fit_test(selected[z], tonic_note, notes_set, notes_during_chord,
                         k + 1 == n_of_chords, melody_key_mode)

        # selection of the best chord
        selected = sorted(selected, key=lambda x: x.score, reverse=True)
        best_chord = selected[0]

        # make chord notes higher on start_note
        best_chord.notes_list[0] += start_note
        best_chord.notes_list[1] += start_note
        best_chord.notes_list[2] += start_note

        # if silence during chord
        if lowest_note_during_chord == 100:
            lowest_note_during_chord = lowest_note
        else:
            lowest_note_during_chord -= 8

        # adjust octaves
        best_chord.notes_list = sorted(best_chord.notes_list)
        while True:
            if best_chord.notes_list[0] + 12 <= lowest_note_during_chord:
                best_chord.notes_list[0] += 12
                if best_chord.notes_list[1] + 12 <= lowest_note_during_chord:
                    best_chord.notes_list[1] += 12
                    if best_chord.notes_list[2] + 12 <= lowest_note_during_chord:
                        best_chord.notes_list[2] += 12
                    else:
                        break
                else:
                    break
            else:
                break
        if best_chord.notes_list[2] >= lowest_note_during_chord:
            best_chord.notes_list[2] -= 12
            if best_chord.notes_list[1] >= lowest_note_during_chord:
                best_chord.notes_list[1] -= 12
                if best_chord.notes_list[0] >= lowest_note_during_chord:
                    best_chord.notes_list[0] -= 12

        # put the best chord in the list
        best_chords.append(best_chord)

    # save the midi file
    save_mid(mid1, best_chords, ticks_per_beat, 'output.mid')


if __name__ == "__main__":
    main()
