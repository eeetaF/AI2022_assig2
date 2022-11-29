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


def fit_test(current_chord, tonic_note, notes_set, notes_during_chord):
    chord_notes = current_chord.notes_list
    for current_note in chord_notes:
        if current_note == tonic_note:
            current_chord.score += 5
        elif notes_set[current_note]:
            current_chord.score += 3

        if current_note in notes_during_chord:
            current_chord.score += 8

    chord_notes.sort()
    length1 = chord_notes[1] - chord_notes[0]
    length2 = chord_notes[2] - chord_notes[1]
    length3 = chord_notes[2] - chord_notes[0]

    if length1 == 1:
        current_chord.score -= 100
    elif length1 == 2:
        current_chord.score -= 30
    elif length1 == 3:
        current_chord.score += 4
    elif length1 == 4:
        current_chord.score += 4
    elif length1 == 6 or length1 == 7:
        current_chord.score -= 1
    elif length1 == 8:
        current_chord.score -= 2
    elif length1 == 10:
        current_chord.score -= 30
    elif length1 == 11:
        current_chord.score -= 100

    if length2 == 1:
        current_chord.score -= 100
    elif length2 == 2:
        current_chord.score -= 30
    elif length2 == 3:
        current_chord.score += 4
    elif length2 == 4:
        current_chord.score += 4
    elif length2 == 6 or length2 == 7:
        current_chord.score -= 1
    elif length2 == 8:
        current_chord.score -= 2
    elif length2 == 10:
        current_chord.score -= 30
    elif length2 == 11:
        current_chord.score -= 100

    if length3 == 1:
        current_chord.score -= 100
    elif length3 == 2:
        current_chord.score -= 30
    elif length3 == 3:
        current_chord.score -= 10
    elif length3 == 4:
        current_chord.score -= 5
    elif length3 == 5:
        current_chord.score -= 1
    elif length3 == 7:
        current_chord.score += 4
    elif length3 == 8:
        current_chord.score += 2
    elif length3 == 9:
        current_chord.score += 1
    elif length3 == 10:
        current_chord.score -= 30
    elif length3 == 11:
        current_chord.score -= 100


def select(chords):
    selected = []
    for _ in range(300):
        a = random.randint(0, 299)
        b = random.randint(0, 299)
        c = random.randint(0, 299)
        d = random.randint(0, 299)
        while (a == b) or (a == c) or (b == c) or (a == d) or (b == d) or (c == d):
            b = random.randint(0, 299)
            c = random.randint(0, 299)
            d = random.randint(0, 299)
        temp = [chords[a], chords[b], chords[c], chords[d]]
        temp = sorted(temp, key=lambda x: x.score, reverse=True)
        selected.append(temp[0])
    return selected


def check_intersection(chord1, chord2):
    if (chord1.notes_list[0] == chord1.notes_list[1] or
            chord1.notes_list[1] == chord1.notes_list[2] or
            chord1.notes_list[0] == chord1.notes_list[2] or
            chord2.notes_list[0] == chord2.notes_list[1] or
            chord2.notes_list[1] == chord2.notes_list[2] or
            chord2.notes_list[0] == chord2.notes_list[2]):
        return True
    return False


def crossover(selected):
    for _ in range(149):
        if random.randint(0, 7) == 0:
            continue
        chord1 = selected[_]
        chord2 = selected[_ + 149]
        temp1 = random.randint(0, 2)
        temp2 = random.randint(0, 2)
        a = chord1.notes_list[temp1]
        b = chord2.notes_list[temp2]
        chord1.notes_list[temp1] = b
        chord2.notes_list[temp2] = a
        if check_intersection(chord1, chord2):
            chord1.notes_list[temp1] = a
            chord2.notes_list[temp2] = b

    return selected


def mutation(selected):
    for _ in range(299):
        if random.randint(0, 3) == 0:
            continue
        current_chord = selected[_]
        temp = random.randint(0, 2)
        a = random.randint(0, 11)
        b = current_chord.notes_list[temp]
        current_chord.notes_list[temp] = a
        if (current_chord.notes_list[0] == current_chord.notes_list[1] or
                current_chord.notes_list[1] == current_chord.notes_list[2] or
                current_chord.notes_list[0] == current_chord.notes_list[2]):
            current_chord.notes_list[temp] = b

    return selected


def update_mid(mid, chords, ticks_per_beat):
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


def main():
    # 'barbiegirl_mono.mid' 'input1.mid' 'input2.mid' 'input3.mid'
    mid1 = MidiFile('input2.mid')

    notes = parse_notes(mid1)

    mid2 = converter.parse('input2.mid')

    melody_key_name = mid2.analyze('key').tonic.name
    melody_key_mode = mid2.analyze('key').mode

    notes_set = []

    for _ in range(12):
        notes_set.append(False)

    lowest_note = 100
    total_time = 0
    for n in notes:
        total_time += n.time
        if n.int_note is not None:
            if n.int_note < lowest_note:
                lowest_note = n.int_note
            notes_set[n.int_note % 12] = True

    tonic_note = define_tonic(melody_key_name)
    if tonic_note == 12:
        print("Error! Tonic is undefined")

    print(melody_key_name)
    print(melody_key_mode)
    print(notes_set)
    print(lowest_note)
    print(tonic_note)

    start_note = lowest_note - ((lowest_note % 12 - tonic_note + 12) % 12) - 12

    ticks_per_beat = mid1.ticks_per_beat

    n_of_chords = math.ceil(total_time / ticks_per_beat)
    i = 0
    velocity = notes[0].velocity
    best_chords = []
    for k in range(n_of_chords):
        lowest_note_in_chord = 100
        chords = []
        notes_during_chord = []
        j = i
        temp_time = ticks_per_beat
        while temp_time > 0:
            if j >= len(notes):
                break
            if notes[j].int_note is not None:
                notes_during_chord.append(notes[j].int_note % 12)
                if notes[j].int_note < lowest_note_in_chord:
                    lowest_note_in_chord = notes[j].int_note
            temp_time -= notes[j].time
            notes[j].time = 0
            j += 1
        if temp_time < 0:
            notes[j - 1].time = -temp_time
            j -= 1
        i = j

        for _ in range(300):
            a = random.randint(0, 11)
            b = random.randint(0, 11)
            c = random.randint(0, 11)
            while (a == b) or (a == c) or (b == c):
                b = random.randint(0, 11)
                c = random.randint(0, 11)
            current_chord = Chord(a, b, c, 0, velocity)
            fit_test(current_chord, tonic_note, notes_set, notes_during_chord)
            chords.append(current_chord)

        selected = []
        for _ in range(3):
            selected = select(chords)
            selected = crossover(selected)
            selected = mutation(selected)
            for z in range(299):
                fit_test(selected[z], tonic_note, notes_set, notes_during_chord)
        selected = sorted(selected, key=lambda x: x.score, reverse=True)
        best_chord = selected[0]
        best_chord.notes_list[0] += start_note
        best_chord.notes_list[1] += start_note
        best_chord.notes_list[2] += start_note
        if lowest_note_in_chord == 100:
            lowest_note_in_chord = lowest_note
        lowest_note_in_chord -= 5
        best_chord.notes_list = sorted(best_chord.notes_list)
        while True:
            if best_chord.notes_list[0] + 12 <= lowest_note_in_chord:
                best_chord.notes_list[0] += 12
                if best_chord.notes_list[1] + 12 <= lowest_note_in_chord:
                    best_chord.notes_list[1] += 12
                    if best_chord.notes_list[2] + 12 <= lowest_note_in_chord:
                        best_chord.notes_list[2] += 12
                    else:
                        break
                else:
                    break
            else:
                break

        if best_chord.notes_list[2] >= lowest_note_in_chord:
            best_chord.notes_list[2] -= 12
            if best_chord.notes_list[1] >= lowest_note_in_chord:
                best_chord.notes_list[1] -= 12
                if best_chord.notes_list[0] >= lowest_note_in_chord:
                    best_chord.notes_list[0] -= 12
        best_chords.append(best_chord)

    mid1.tracks.append(MidiTrack())
    mid1.tracks.append(MidiTrack())
    mid1.tracks.append(MidiTrack())
    update_mid(mid1, best_chords, ticks_per_beat)
    mid1.save('output2.mid')


if __name__ == "__main__":
    main()
