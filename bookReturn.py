import io

from google.cloud import videointelligence
from google.oauth2 import service_account

def video_detect_text():
    """Detect text in a local video."""
    #Get the API credentials from the env file.
    CREDENTIALS = service_account.Credentials.from_service_account_file('.env')

    video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
    features = [videointelligence.Feature.TEXT_DETECTION]

    with io.open("libraryPhotos/book1.JPG", "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]
    for text_annotation in annotation_result.text_annotations:
        print(text_annotation.text)

video_detect_text()