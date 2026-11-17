# In the Lobby · Skattefuten

En kontorkomedie på 3:21 om å vente i en digital møtelobby. Mens tiden går, gir Skattefuten datamusen navnet Steve. Til slutt blir han selv lobbyen.

[Lytt på bredland.no](https://www.bredland.no/musikk/in-the-lobby/) · [Melodi Grand Prompt](https://melodigrandprompt.ai/) · [Se konkurransevideoen (MP4)](https://cuiymilzhfafmwqmfabw.supabase.co/storage/v1/object/public/videos/videos/8e78ffbd-ba08-4ee4-9a27-921f9c49127a/In-the-Lobby-Skattefuten.mp4)

## Filer

| Fil | Innhold |
| --- | --- |
| [src/web/index.html](src/web/index.html) | Statisk låtside for bredland.no med video- og lydspiller |
| [src/web/in-the-lobby.mp3](src/web/in-the-lobby.mp3) | Hele låta i stereo |
| [src/web/in-the-lobby.mp4](src/web/in-the-lobby.mp4) | Ferdig musikkvideo med originalopptaket |
| [src/web/lobbyen.webp](src/web/lobbyen.webp) | Videoplakat med alle tolv illustrasjonene |
| [production/lobby-film-sheet.png](production/lobby-film-sheet.png) | Originalillustrasjonene som brukes i klippen |
| [production/render.py](production/render.py) | Skript for å klippe filmen etter lydsporet |

## Nettsiden

Åpne `src/web/index.html` lokalt for å spille av filene. Ved publisering kopieres innholdet i `src/web/` til `/musikk/in-the-lobby/` på bredland.no. Siden bruker nettstedets felles `/site.css` og `/favicon.ico`. En commit på GitHub publiserer ikke siden automatisk.

## Gjenskap videoen

Kjør `python production/render.py` fra prosjektroten på Windows med Python, Pillow, NumPy, FFmpeg på PATH og skrifttypene Impact og Consolas. Skriptet bruker illustrasjonene og MP3-filen og skriver over `src/web/in-the-lobby.mp4`.

## Kreditering og gjenbruk

Teksten bygger hovedsakelig på originaltekst av Lars Thomas Bredland, med engelsk oversettelse av ChatGPT. Musikken er generert med Suno og bearbeidet i Audacity.

Kode er tilgjengelig under MIT-lisensen. Tekst, lyd, illustrasjoner og video er tilgjengelig under CC BY 4.0. Du kan bruke, endre og dele materialet, også kommersielt, med kreditering. Se [LICENSE](LICENSE).

Foreslått kreditering er «In the Lobby – Skattefuten / Lars Thomas Bredland» med lenke til dette repoet. Oppgi også lisensen og eventuelle endringer. Lisensene gjelder rettighetene opphaveren selv disponerer.

Videoen i src/web er komprimert for opplasting til GitHub. Konkurransevideoen i lenken øverst er originalversjonen.
