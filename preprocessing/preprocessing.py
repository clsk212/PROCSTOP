import argparse
import os
import pandas as pd

from moviepy.editor import VideoFileClip

def map_dataframe(df):
    modality_mapping = {
        1: 'full-AV',
        2: 'video-only',
        3: 'audio-only'
    }

    vocal_channel_mapping = {
        1: 'speech',
        2: 'song'
    }
    emotion_mapping = {
        1: 'neutral',
        2: 'calm',
        3: 'happy',
        4: 'sad',
        5: 'angry',
        6: 'fearful',
        7: 'disgust',
        8: 'surprised'
    }

    intensity_mapping = {
        1: 'normal',
        2: 'strong'
    }

    statement_mapping = {
        1: "Kids are talking by the door",
        2: "Dogs are sitting by the door"
    }

    repetition_mapping = {
        1: '1st repetition',
        2: '2nd repetition'
    }

    actor_mapping = {
        i: 'male' if i % 2 != 0 else 'female' for i in range(1, 25)
    }

    df['Modality'] = df['Modality'].map(modality_mapping)
    df['Vocal_channel'] = df['Vocal_channel'].map(vocal_channel_mapping)
    df['Emotion'] = df['Emotion'].map(emotion_mapping)
    df['Emotional_intensity'] = df['Emotional_intensity'].map(intensity_mapping)
    df['Statement'] = df['Statement'].map(statement_mapping)
    df['Repetition'] = df['Repetition'].map(repetition_mapping)
    df['Actor'] = df['Actor'].map(actor_mapping)
    return df

def extract_df_ravdess(raw_data_path, output_path):
    """Load and parse RAVDESS data from a specified directory and save to a DataFrame."""
    data = []
    
    if not os.path.exists(raw_data_path):
        raise Exception(f"Input directory does not exist: {raw_data_path}")

    for filename in os.listdir(raw_data_path):
        if filename.endswith(".mp4") or filename.endswith(".wav"):
            parts = filename.split('.')[0].split('-')
            file_info = {
                'Modality': int(parts[0]),
                'Vocal_channel': int(parts[1]),
                'Emotion': int(parts[2]),
                'Emotional_intensity': int(parts[3]),
                'Statement': int(parts[4]),
                'Repetition': int(parts[5]),
                'Actor': int(parts[6]),
                'Filename': filename
            }
            data.append(file_info)

    df = pd.DataFrame(data)
    df_mapped = map_dataframe(df)

    output_path = output_path + '/ravdess_data.csv'

    df_mapped.to_csv(output_path, index=False)
    print(f"Mapped data saved to {output_path}")
    return df_mapped

def process_videos(df, base_path):
    """
    Processes videos by extracting audio and saving the video without audio.
    Updates and returns the DataFrame with paths to the processed files.

    Args:
        df (pandas.DataFrame): DataFrame that includes a column 'Filename' with the names of MP4 files.
        base_path (str): Base path to the directory where the original video files are located.

    Returns:
        pandas.DataFrame: DataFrame updated with 'audio' and 'video' columns.
    """

    # Define the output directories
    audio_dir = os.path.join(base_path, 'data', 'audio')
    video_dir = os.path.join(base_path, 'data', 'video')

    # Ensure directories exist
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    # Prepare columns for audio and video paths
    audio_paths = []
    video_paths = []

    # Process each video in the DataFrame
    for filename in df['Filename']:
        video_file = os.path.join(base_path, filename)
        base_filename = os.path.splitext(os.path.basename(video_file))[0]

        # Load the video
        clip = VideoFileClip(video_file)

        # Define paths for the processed files
        audio_path = os.path.join(audio_dir, f'{base_filename}.mp3')
        video_path = os.path.join(video_dir, f'{base_filename}.mp4')

        # Save the audio
        clip.audio.write_audiofile(audio_path)

        # Save the video without audio
        clip.without_audio().write_videofile(video_path, codec='libx264')

        # Close the clip to release resources
        clip.close()

        # Store paths
        audio_paths.append(audio_path)
        video_paths.append(video_path)

    # Update the DataFrame with the paths
    df['audio'] = audio_paths
    df['video'] = video_paths

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process RAVDESS dataset into structured data.")
    parser.add_argument("-i", "--input", required=True, help="Input directory path for raw data.")
    parser.add_argument("-o", "--output", help="Output file path to save processed data.", default=r'../data')
    args = parser.parse_args()
    _raw_data_path = args.input
    _output_path = args.output

    df_mapped = extract_df_ravdess(_raw_data_path, _output_path)

    process_videos(df_mapped, _raw_data_path)


    

