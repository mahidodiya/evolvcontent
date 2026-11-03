import cv2
import tempfile
import os

from app.modules.moderations.image import moderate_image
from app.modules.moderations.text import moderate_text


def extract_frames(video_path: str, interval: int = 5):

    capture = cv2.VideoCapture(video_path)

    frames = []

    fps = capture.get(cv2.CAP_PROP_FPS)

    if not fps or fps <= 0:
        capture.release()
        raise ValueError("Unable to determine video frame rate")

    interval_frames = max(int(fps * interval), 1)

    frame_count = 0

    while True:

        success, frame = capture.read()

        if not success:
            break

        if frame_count % interval_frames == 0:

            with tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            ) as temp:

                frame_path = temp.name

            cv2.imwrite(frame_path, frame)

            frames.append(frame_path)

        frame_count += 1

    capture.release()

    return frames


async def moderate_video_frames(frame_paths: list):

    results = []

    try:

        for frame_path in frame_paths:

            # Convert extracted frame into a data URL
            import base64

            with open(frame_path, "rb") as image_file:

                encoded = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            image_url = f"data:image/jpeg;base64,{encoded}"

            result = await moderate_image(image_url)

            results.append(result)

    finally:

        for frame_path in frame_paths:

            if os.path.exists(frame_path):
                os.remove(frame_path)

    return results