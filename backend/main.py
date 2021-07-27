from fastapi import FastAPI, File, UploadFile, status, HTTPException
import shutil
import glob
import os
from models import Music
from database import SessionLocal, engine
import eyed3
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
path_mp3 = os.environ["PATH_MP3"]

origins = [
    os.environ["SONGS"],
    os.environ["LOCALHOST"]
]


@app.post("/uploadfile/", status_code=status.HTTP_201_CREATED)
def create_upload_file(file: UploadFile = File(...)):
    os.chdir(path_mp3)
    buffer = open(file.filename, "wb")
    shutil.copyfileobj(file.file, buffer)

    def get_mp3_metadata():
        value = eyed3.load(file.filename)

        dict = {"song": file.filename,
                "title": value.tag.title,
                "artist": value.tag.artist,
                "album": value.tag.album,
                }
        try:

            dict["year"] = value.tag.getBestDate()._year
            return dict

        except AttributeError:

            dict["year"] = None
            return dict

    value = get_mp3_metadata()

    with SessionLocal() as db:
        music = Music(
            filename=value["song"],
            title=value["title"],
            artist=value["artist"],
            album=value["album"],
            year=value["year"]
        )
        db.add(music)
        db.commit()
        db.refresh(music)

    return get_mp3_metadata()


@app.get("/songs/", status_code=200)
def get_songs():
    with SessionLocal() as db:
        music = db.query(Music).all()
    return music


@app.get("/songs/{song_id}", status_code=200)
def get_song(song_id: int):
    with SessionLocal() as db:
        song = db.query(Music).filter(Music.id == song_id).one()
        if song is None:
            raise HTTPException(status_code=404, detail="music not found")
        return song


@app.get("/songs/{song_id}/file", status_code=200)
def get_song_file(song_id: int):
    with SessionLocal() as db:
        song = db.query(Music).filter(Music.id == song_id).one()
        if song is None:
            raise HTTPException(status_code=404, detail="music not found")
        return FileResponse(path=path_mp3 + song.filename,
                            media_type='application/octet-stream',
                            filename=song.filename)


@app.post("/songs/{song_id}/like", status_code=200)
def like_a_song(song_id: int):
    with SessionLocal() as db:
        song = db.query(Music).filter(Music.id == song_id).one()
        if song is None:
            raise HTTPException(status_code=404, detail="music not found")
        else:
            song.liked = not song.liked
            db.add(song)
            db.commit()
            db.refresh(song)
            return song


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StorgePrevioler:
    def __init__(self, direccion):
        self.direccion = direccion

    def get_files(self):
        os.chdir(self.direccion)
        files_path = [x for x in glob.glob("*.mp3")]
        return files_path
