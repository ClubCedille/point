# point

Transcription d'audio en texte grâce à Whisper.

# Utilisation

`point.py` est un service qui répond aux requêtes `POST` au chemin `/transcript` avec le texte correspondant à la transcription du fichier audio donné.

À la première requête, si le modèle Whisper n'est pas présent, il sera téléchargé dans le dossier `whisper-models` du dossier courant.

Par exemple,

```console
$ python3 point.py --port 5000
```

Et dans un autre terminal:

```console
$ curl -X POST -T '12 Still Alive.mp3' -H 'Content-Type: audio/mp3' http://127.0.0.1:5000/transcript
2024-06-20 19:54:40, transcript with base

 This was a triumph.
 I'm making a note here, huge success.
 It's hard to always date my sad inspection.
...
```

Ce n'est pas parfait, mais si le modèle utilisé est plus gros que `base` (comme `distil-large-v3`), ça devrait mieux fonctionner. Le langage est détecté automatiquement.
