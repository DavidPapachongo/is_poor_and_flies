from fastapi import FastAPI, File, UploadFile, status, HTTPException
import shutil
import glob
import os
from models import Music
from database import SessionLocal, engine
from sqlalchemy.orm.exc import NoResultFound
import eyed3
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
path_mp3 = os.environ["PATH_MP3"]


def get_mp3_metadata(filepath):
    value = eyed3.load(filepath)

    dict = {"song": filepath,
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


@app.post("/uploadfile/", status_code=status.HTTP_201_CREATED)
def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    if file.filename.endswith(".mp3"):
        os.chdir(path_mp3)
        buffer = open(file.filename, "wb")
        shutil.copyfileobj(file.file, buffer)

        value = get_mp3_metadata(file.filename)

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
        return value
    else:
        raise HTTPException(status_code=400, detail="invalid file")


@app.get("/songs/", status_code=200)
def get_songs():
    with SessionLocal() as db:
        music = db.query(Music).all()
    return music


@app.get("/songs/{song_id}", status_code=200)
def get_song(song_id: int):
    with SessionLocal() as db:
        try:
            song = db.query(Music).filter(Music.id == song_id).one()
            return song
        except NoResultFound:
            raise HTTPException(status_code=404, detail="music not found")


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


origins = os.environ["ALLOW_ORIGINS"].split(",")

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
