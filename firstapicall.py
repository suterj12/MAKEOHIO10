from google.cloud import videointelligence
from google.oauth2 import service_account


#Get the API credentials from the env file.
CREDENTIALS = service_account.Credentials.from_service_account_file(
    '.env')

video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
features = [videointelligence.Feature.LABEL_DETECTION]
operation = video_client.annotate_video(
    request={
        "features": features,
        "input_uri": "gs://cloud-samples-data/video/cat.mp4",
    }
)
print("\nProcessing video for label annotations:")

result = operation.result(timeout=180)
print("\nFinished processing.")

# first result is retrieved because a single video was processed
segment_labels = result.annotation_results[0].segment_label_annotations
for i, segment_label in enumerate(segment_labels):
    print("Video label description: {}".format(segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    for i, segment in enumerate(segment_label.segments):
        start_time = (
            segment.segment.start_time_offset.seconds
            + segment.segment.start_time_offset.microseconds / 1e6
        )
        end_time = (
            segment.segment.end_time_offset.seconds
            + segment.segment.end_time_offset.microseconds / 1e6
        )
        positions = "{}s to {}s".format(start_time, end_time)
        confidence = segment.confidence
        print("\tSegment {}: {}".format(i, positions))
        print("\tConfidence: {}".format(confidence))
    print("\n")