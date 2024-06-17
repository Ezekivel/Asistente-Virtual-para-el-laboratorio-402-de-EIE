#!/bin/bash

i=1

while true
do
    rec -r 44100 -c 2 temp_audio.wav silence 1 0.1 1.8% 1 1.5 1.8%
    if [ -s temp_audio.wav ]; then  # Comprueba si el archivo no está vacío
        filename=$(printf "audio%03d.wav" "$i")
        mv temp_audio.wav "$filename"
        let i++
    else
        rm -f temp_audio.wav
    fi
done


