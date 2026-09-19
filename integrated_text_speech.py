import threading
import pyttsx3


def _speak_worker(text):

    try:

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            150
        )

        engine.setProperty(
            "volume",
            1.0
        )

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print(
            f"Speech error: {e}"
        )


def speak_text(text):

    if text and text.strip():

        thread = threading.Thread(
            target=_speak_worker,
            args=(text,),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":

    print(
        "Testing basic GazeMate text to speech..."
    )

    speak_text(
        "GazeMate text to speech is working."
    )