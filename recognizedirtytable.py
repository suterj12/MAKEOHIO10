"""Object tracking in a local video."""
from google.cloud import videointelligence
from google.oauth2 import service_account
import io

#Get the API credentials from the env file.
CREDENTIALS = service_account.Credentials.from_service_account_file(
    '.env')

video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
features = [videointelligence.Feature.OBJECT_TRACKING]

with io.open("data/CoveredKSA1.MOV", "rb") as file:
    input_content = file.read()

operation = video_client.annotate_video(
    request={"features": features, "input_content": input_content}
)

print("\nProcessing video for object annotations.")
result = operation.result(timeout=500)
print("\nFinished processing.\n")

# The first result is retrieved because a single video was processed.
object_annotations = result.annotation_results[0].object_annotations

#Define objects that make tables dirty.
clutter = set(('bottle', 'packaged goods'))

# Get the object descriptions and print them.
object_descriptions = set()
for object_annotation in object_annotations:
   object_descriptions.add(object_annotation.entity.description)
print('Object descriptions: ', object_descriptions, '\n')

#Determine and report whether any of the item descriptions match known clutter.
clean_table = clutter.isdisjoint(object_descriptions)
if clean_table:
    print('The table is clean!\n')
else:
    print('The table is dirty!\n')

