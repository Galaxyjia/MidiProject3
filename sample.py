# -*- coding: utf-8 -*-
import pretty_midi
import random

# ------------------------初期化------------------------- #
# PrettyMIDIオブジェクトを作成
pm = pretty_midi.PrettyMIDI(resolution=480, initial_tempo=120)

Cmajor = ['C4','D4','E4','F4','G4','A4','B4','C5',]
ChordPattern1 = ['A4','F4','G4','C4',]
ChordPattern2 = ['A4','F4','C4','G4',]

# ---------------------ランダム生成------------------------- #
melody = pretty_midi.Instrument(0) # メロディ
for i in range(10) :
    note_number = pretty_midi.note_name_to_number(random.choice(Cmajor))
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=i, end=i+1)
    melody.notes.append(note)

pm.instruments.append(melody)

bass = pretty_midi.Instrument(8) # ベース
note_number = pretty_midi.note_name_to_number('G4')
note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=1)
bass.notes.append(note)
pm.instruments.append(bass)

# -----------------------------出力----------------------- #
pm.write('test2.mid')
