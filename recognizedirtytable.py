"""Object tracking in a local video."""
from google.cloud import videointelligence
from google.oauth2 import service_account
import io

#Get the API credentials from the env file.
CREDENTIALS = service_account.Credentials.from_service_account_file(
    '.env')

video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
features = [videointelligence.Feature.OBJECT_TRACKING]

#Read in 4 videos.
video_path = "data/KSAMerged.MOV"
with io.open(video_path, "rb") as file:
    input_content = file.read()

#Call the api to annotate the video.
operation = video_client.annotate_video(
    request={ "features": features, "input_content": input_content, "video_context": {"segments": [
        { "start_time_offset": "0.5s", "end_time_offset" : "1.5s" },
        { "start_time_offset": "2.5s", "end_time_offset" : "3.5s" },
        { "start_time_offset": "4.5s", "end_time_offset" : "5.5s" },
        { "start_time_offset": "6.5s", "end_time_offset" : "7.5s" } ]}
    }
)

print("\nProcessing video for object annotations.")
result = operation.result(timeout=500)
print("\nFinished processing.\n")

# The first result is retrieved because a single video was processed.
object_annotations = []
for annotation in result.annotation_results:
    object_annotations.append(annotation.object_annotations)

#Define objects that make tables dirty.
clutter = set(('bottle', 'packaged goods'))

#Iterate through each segment.
for i in range(4):
    object_descriptions = set()
    for object_annotation in object_annotations[i]:
        object_descriptions.add(object_annotation.entity.description)
    print('Object descriptions in segment ' , i + 1, ': ', object_descriptions, '\n')
    #Determine and report whether any of the item descriptions match known clutter.
    clean_table = clutter.isdisjoint(object_descriptions)
    if clean_table:
        print('Table ', i + 1, ' is clean!\n')
    else:
        print('Table ', i + 1, ' is dirty!\n')

