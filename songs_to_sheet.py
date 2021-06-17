from pathlib import Path
from itertools import chain
from tinytag import TinyTag
from tqdm import tqdm
from time import sleep

# Logging function
def log_it(text, console_write = True):
    if console_write:
        print(text)
    with open(log_path, "a", encoding="utf-8", errors="ignore") as f:
        f.write(text + "\n")

# ID refs
single_id = "Singles"
double_id = "Doubles"
novice_id = "Novice"
easy_id   = "Easy"
medium_id = "Medium"
hard_id   = "Hard"
expert_id = "Expert"
edit_id   = "Edit"

delimiter = ";"
bad_characters = "☆"

# Column headings (5 main + 6 difficulty)
headings = ["Title", "Title (transliterated)", "Artist", "Song Pack", "Duration",
            novice_id, easy_id, medium_id, hard_id, expert_id, edit_id]

# Lookup tables
chart_mode_map = {"dance-single" : single_id, "dance-double" : double_id,
                  "single"       : single_id, "double"       : double_id}

chart_difficulty_map = {"beginner"  : novice_id,  "beginner" : novice_id,
                        "easy"      : easy_id,    "basic"    : easy_id, 
                        "medium"    : medium_id,  "another"  : medium_id,
                        "hard"      : hard_id,    "maniac"   : hard_id,
                        "challenge" : expert_id , "smaniac"  : expert_id,
                        "edit"      : edit_id}

difficulty_indicies = {novice_id : 0, easy_id : 1, medium_id : 2, hard_id : 3, expert_id : 4, edit_id : 5}

# Paths
songs_dir = Path("..") / "Songs"
output_dir = Path(".") / "output"
output_dir.mkdir(exist_ok=True)

singles_path = output_dir / f"{single_id}.csv"
doubles_path = output_dir / f"{double_id}.csv"

log_path = output_dir / "log.txt"
with open(log_path, "w", encoding="utf-8", errors="ignore") as f:
    f.write("StepMania Songs to Sheet Log:\n\n")

song_files = []
songs = []
song_errors = []

# Directory count in Songs
if songs_dir.exists():
    packs_installed = set([i for i in songs_dir.iterdir() if i.is_dir()])
    songs_installed = set([j for i in songs_dir.iterdir() if i.is_dir() for j in i.iterdir() if j.is_dir()])
    log_it(f"{len(packs_installed)} pack installs found")
    log_it(f"{len(songs_installed)} song installs found")
else:
    log_it("No song installs found. Is Songs to Sheet in the correct location?")
    log_it("Exiting ...")
    sleep(3)
    exit()

log_it("Scanning for song definitions ...")
# glob "**" is recursive to sub folders
ssc_files = songs_dir.glob("**/*.ssc")
sm_files = songs_dir.glob("**/*.sm")
dwi_files = songs_dir.glob("**/*.dwi")

# Culling duplicates, some have multiple chart definitions (.ssc, .sm, .dwi)
songs_done = set()
for song_file in chain(ssc_files, sm_files, dwi_files):

    # 1 song : 1 directory, ssc > sm > dwi
    if song_file.parent in songs_done:
        continue

    # Remove from installed list as found
    if song_file.parent in songs_installed:
        songs_installed.remove(song_file.parent)

    # Detecting songs in the wrong directory
    if song_file.parts[-4] != "Songs":
        song_errors.append(f"Bad install    - {song_file}")
        continue

    # Detecting bad characters in file names StepMania can't handle
    if any(bad in part for part in song_file.parts for bad in bad_characters):
        song_errors.append(f"Bad file chars - {song_file}")
        continue

    song_files.append(song_file)
    songs_done.add(song_file.parent)

# Any left over after culling are empty folders
for song_install in songs_installed:
    song_errors.append(f"Bad install    - {song_install}")

# Nothing found, exit early
if len(song_files) == 0:
    log_it("No song definitions found. Is Songs to Sheet in the correct location?")
    log_it("Exiting ...")
    sleep(3)
    exit()

log_it("Parsing song data ...", False)
for song_file in tqdm(song_files,
                      ncols=50,
                      desc="Parsing song data",
                      bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"):

    try:
        # Files are UTF-8, UTF-8 BOM, ANSI and probably some other stuff
        # We don't care about weird characters so we dump them
        with open(song_file, encoding="utf-8", errors="ignore") as f:
            lines = f.read()
            if lines.startswith("\ufeff"): # Handling BOM
                lines = lines[1:]
            lines = lines.split("\n")

        title, title_translit, artist, song_pack, duration = "", "", "", "", ""
        music_path = ""
        charts = []

        # Most pattern detection is hardcoded
        # See 'notes.txt' for details of known patterns
        # Assume named entries can be out of order
        # Assume files are correctly formatted (catch all errors and skip the song)
        lines_iter = iter(lines)
        for line in lines_iter:
            
            # Named entries always begin with '#', small speed up 
            if not line.startswith("#"):
                continue

            if line.startswith("#TITLE:"):
                title = line[7:-1]
            elif line.startswith("#TITLETRANSLIT:"):
                title_translit = line[15:-1]
            elif line.startswith("#ARTIST:"):
                artist = line[8:-1]
            elif line.startswith("#MUSIC:"): # sm/ssc music
                music_path = Path(line[7:-1])
            elif line.startswith("#FILE:"):  # dwi music
                candidate_path = Path(line[6:-1])
                music_path = Path()
                #  Handling dwi file paths relative to StepMania base directory
                if len(candidate_path.parts) != 1:
                    music_path = music_path / ".." / ".." / ".."
                music_path = music_path / candidate_path

            chart_mode, chart_difficulty, chart_meter = None, None, None

            if song_file.suffix == ".ssc":
                if line.startswith("#NOTEDATA:"):
                    while not chart_mode or not chart_difficulty or not chart_meter:
                        line = next(lines_iter)
                        if line.startswith("#STEPSTYPE:"):
                            chart_mode = line[11:-1].lower()
                        elif line.startswith("#DIFFICULTY:"):
                            chart_difficulty = line[12:-1].lower()
                        elif line.startswith("#METER:"):
                            chart_meter = line[7:-1]

            elif song_file.suffix == ".sm":
                if line.startswith("#NOTES:"):
                    chart_mode = next(lines_iter).strip()[:-1].lower()
                    next(lines_iter)
                    chart_difficulty = next(lines_iter).strip()[:-1].lower()
                    chart_meter = next(lines_iter).strip()[:-1]

            elif song_file.suffix == ".dwi":
                if line.startswith("#SINGLE:") or line.startswith("#DOUBLE:"):
                    chart_mode = line[1:7].lower()
                    diff_end_index = line.find(":", 8)
                    chart_difficulty = line[8:diff_end_index].lower()
                    chart_meter = line[diff_end_index + 1]

            # If we didn't find a chart, or it's not one we care about
            if not chart_mode or chart_mode not in chart_mode_map:
                continue

            charts.append((chart_mode_map[chart_mode], chart_difficulty_map[chart_difficulty], chart_meter))

        # Resolve music file location, if valid
        music_path = song_file.parent / music_path
        if not music_path.is_file():
            # Find the best valid music file, if any (ogg > wav > mp3)
            for child in song_file.parent.iterdir():
                # Some songs have multiple *redundant* music files ...
                if child.suffix == ".ogg":
                    music_path = child
                    break
                elif child.suffix == ".wav":
                    music_path = child
                elif music_path.suffix != ".wav" and child.suffix == ".mp3":
                    music_path = child

        # Some songs don't have music ... ... wha?
        if not music_path.exists():
            song_errors.append(f"Music missing  - {song_file}")
            continue

        # Detecting bad characters in music file names StepMania can't handle
        if any(bad in part for part in music_path.parts for bad in bad_characters):
            song_errors.append(f"Bad file chars - {song_file}")
            continue

        # Song duration formatted for mm:ss
        tag = TinyTag.get(music_path)
        duration = f"{int(tag.duration // 60)}:{int(tag.duration % 60):02}"

        # Song pack is defined as the containing folder name
        song_pack = song_file.parts[-3]

        songs.append([title, title_translit, artist, song_pack, duration, charts])
    
    # Assume any other error is a bad song definition
    except Exception:
        song_errors.append(f"Bad definition - {song_file}")

# Error logging
if song_errors:
    log_it(f"{len(song_errors)} songs with errors, see log for details")
    log_it("Song Errors:", False)
    for song_error in song_errors:
        log_it("    " + str(song_error), False)

log_it("Writing output ...")
singles_csv = []
doubles_csv = []
for song in songs:

    # Replacing some entries and abbreviating
    song[0] = song[0] or "[No Title]"
    song[1] = song[1] or song[0]
    song[2] = song[2] or "[No Artist]"

    song[3] = song[3].replace("Dance Dance Revolution", "DDR")
    song[3] = song[3].replace("In The Groove", "ITG")
    song[3] = song[3].replace("Dancing Stage", "DS")

    # Removing characters StepMania will filter out
    for i in range(3):
        song[i] = song[i].replace("\\", "")
        song[i] = song[i].replace("#", "")
        song[i] = song[i].replace(";", "")

    # Removing delimiter occurrences (we won't handle these)
    for i in range(4):
        song[i] = song[i].replace(delimiter, "")

    # Construct meters
    singles_meters = [""] * 6
    doubles_meters = [""] * 6
    for chart in song[-1]:
        index = difficulty_indicies[chart[1]]
        if chart[0] == single_id:
            singles_meters[index] = chart[2]
        else:
            doubles_meters[index] = chart[2]

    # Format song data (cull empties)
    main_details = delimiter.join(song[:-1]) + delimiter
    if not singles_meters == [""] * 6:
        singles_csv.append(main_details + delimiter.join(singles_meters) + delimiter)
    if not doubles_meters == [""] * 6:
        doubles_csv.append(main_details + delimiter.join(doubles_meters) + delimiter)
    y = 9

headings = delimiter.join(headings)

# Need to ignore errors on output also. Still have some weird characters.
with open(singles_path, "w", encoding="utf-8", errors="ignore") as f:
    f.write(headings + "\n" + "\n".join(singles_csv))

with open(doubles_path, "w", encoding="utf-8", errors="ignore") as f:
    f.write(headings + "\n" + "\n".join(doubles_csv))

log_it(f"{len(songs)} songs written ({len(singles_csv)} singles) ({len(doubles_csv)} doubles)")
log_it("Done")
sleep(3)
