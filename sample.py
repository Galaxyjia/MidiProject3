# -*- coding: utf-8 -*-
import pretty_midi
import random
import numpy as np
import re

def midi_create(imput_chords,filename='output.mid', base_note='C4',d_time=1,loop_times=1,tempo=60):
    base = pretty_midi.note_name_to_number(base_note)
    root = {'C':0,'C#':1,'D♭':1,'D':2,'D#':3,'E♭':3,'E':4,'F':5,'F#':6,'G♭':6,'G':7,'G#':8,'A♭':8,'A':9,'A#':10,'B♭':10,'B':11,}
    Cmajor = [' ', 'C4','D4','E4','F4','G4','A4','B4','C5',]
    Gate = [1/4, 1/4, 2/4, 2/4, 2/4, 3/4, 4/4]

    chord_type = {'':np.array([0, 4, 7]),
                  'm':np.array([0, 3, 7]),
                  '7':np.array([0, 4, 7, 10]),
                  'm7':np.array([0, 3, 7, 10]),
                  'mM7':np.array([0, 3, 7, 11]),
                  'M7':np.array([0, 4, 7, 11]),
                  'dim':np.array([0, 3, 6, 9]),
                  'aug':np.array([0, 4, 8]),
                  'add9':np.array([0, 4, 7, 14]),
                  'sus4':np.array([0, 5, 7]),
                  '7sus4':np.array([0, 5, 7, 10]),
                  'm6':np.array([0, 3, 7, 9]),
                  '6':np.array([0, 4, 7, 9]),
                  'm7-5':np.array([0, 3, 6, 10]),
                  '9':np.array([0, 4, 7, 10, 13]),
    }

    def split_chord(chord):
        j = chord    
        c = j
        if len(c) > 1:
            c = c[0:2]
            if c[1] == '#' or c[1] == '♭':
                c = c[0:2]
                j = j[2:]

            else:
                c = c[0:1]
                j = j[1:]
        else:
            j = ''
        return c, j

    # ここからmidi_create()関数の処理
    pm = pretty_midi.PrettyMIDI(resolution=480, initial_tempo=tempo)     
    instrument = pretty_midi.Instrument(4) # Eピアノ

    chords = np.array(re.split(" +", imput_chords.rstrip()))
    d_time = 1 #コードを鳴らす間隔（Gateで指定したい）
    time = 0

    for i in range(loop_times): # loop_timesぶんだけ繰り返す
        for chord in chords: # コードの処理
            croot, ctype = split_chord(chord) # ルート音と名前を取り出す
            notes = base + root[croot] # Base音を60に設定
            if ctype in chord_type:
                notes += chord_type[ctype]
            else:
                notes += np.array([0, 12]) # 存在しないコードの場合はオクターブ上の音を重ねる

            for note_number in notes:
                note = pretty_midi.Note(velocity=100, pitch=note_number, start=time, end=time+d_time) 
                instrument.notes.append(note)

            time = time + d_time

    time = 0.0
    melody = pretty_midi.Instrument(4) # Eピアノ
    while time < 4 * 4:
        d_time = random.choice(Gate)
        note_name = random.choice(Cmajor)
        if note_name == ' ':
            note = pretty_midi.Note(velocity=0, pitch=0, start=time, end=time+d_time)
        else :
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(velocity=100, pitch=note_number, start=time, end=time+d_time)
        melody.notes.append(note)
        time = time + d_time
    pm.instruments.append(melody)
    pm.instruments.append(instrument)

    pm.write(filename)

if __name__ == '__main__':
    chord1 = "C G Am7 Em F CM7 F G7 C"
    chord2 = "FM7 G7 Em7 Am"
    chord3 = "F G Em Am"
    for i in range(100):
        midi_create(filename='output' + str(i) + '.mid',imput_chords=chord2, base_note='C3',d_time=1,loop_times=4)
    