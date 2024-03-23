"""Object tracking in a local video."""
from google.cloud import videointelligence
from google.oauth2 import service_account
import io

#Get the API credentials from the env file.
CREDENTIALS = service_account.Credentials.from_service_account_file(
    '.env')

video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
features = [videointelligence.Feature.OBJECT_TRACKING]

with io.open("data/DirtyFront.MOV", "rb") as file:
    input_content = file.read()

operation = video_client.annotate_video(
    request={"features": features, "input_content": input_content}
)
print("\nProcessing video for object annotations.")

result = operation.result(timeout=500)
print("\nFinished processing.\n")

# The first result is retrieved because a single video was processed.
object_annotations = result.annotation_results[0].object_annotations

# Get only the first annotation for demo purposes.
object_annotation = object_annotations[0]
print("Entity description: {}".format(object_annotation.entity.description))
if object_annotation.entity.entity_id:
    print("Entity id: {}".format(object_annotation.entity.entity_id))

print(
    "Segment: {}s to {}s".format(
        object_annotation.segment.start_time_offset.seconds
        + object_annotation.segment.start_time_offset.microseconds / 1e6,
        object_annotation.segment.end_time_offset.seconds
        + object_annotation.segment.end_time_offset.microseconds / 1e6,
    )
)

print("Confidence: {}".format(object_annotation.confidence))

# Here we print only the bounding box of the first frame in this segment
frame = object_annotation.frames[0]
box = frame.normalized_bounding_box
print(
    "Time offset of the first frame: {}s".format(
        frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
    )
)
print("Bounding box position:")
print("\tleft  : {}".format(box.left))
print("\ttop   : {}".format(box.top))
print("\tright : {}".format(box.right))
print("\tbottom: {}".format(box.bottom))
print("\n")