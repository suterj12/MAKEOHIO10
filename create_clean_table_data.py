"""
This file is intended to take series of images or 
videos are parse the objects seen in them into a file.
The images or videos must be passed as a single file.
To differentiate between each segment define the offset times 
from the beginning of the video in the segments variable.
The output will be printed to the location specified by
the "output_file_path" variable.
"""
from google.cloud import videointelligence
from google.oauth2 import service_account
import io

#Get the API credentials from the env file.
CREDENTIALS = service_account.Credentials.from_service_account_file('.env')

#Define the video segments.
segments = [
        { "start_time_offset": "0.5s", "end_time_offset" : "1.5s" },
        { "start_time_offset": "2.5s", "end_time_offset" : "3.5s" },
        { "start_time_offset": "4.5s", "end_time_offset" : "5.5s" },
        { "start_time_offset": "6.5s", "end_time_offset" : "7.5s" } 
]

#Set the output file name.
output_file_path = "data/clean_environment_objects.txt"

video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)
features = [videointelligence.Feature.OBJECT_TRACKING]

#Read in video.
video_path = "data/KSAMerged.MOV"
with io.open(video_path, "rb") as file:
    input_content = file.read()

#Call the api to annotate the video.
#Split the video into 4 distinct segments.
operation = video_client.annotate_video(
    request={ "features": features, "input_content": input_content, "video_context": {"segments": segments} }
)

print("\nProcessing video for object annotations.")
result = operation.result(timeout=500)
print("\nFinished processing.\n")

# Retrieve each of the four annotated segments.
object_annotations = []
for annotation in result.annotation_results:
    object_annotations.append(annotation.object_annotations)

#Open the file to write to.
with open(output_file_path, 'w') as f:

    #Iterate through each segment.
    for i in range(len(segments)):
        object_descriptions = set()
        f.write(f'instance{i}\n')
        for object_annotation in object_annotations[i]:
            object_descriptions.add(object_annotation.entity.description)
            f.write(f'{object_annotation.entity.description}\n')
        f.write('\n')
        print('Object descriptions in segment' , i, ':', object_descriptions, '\n')
