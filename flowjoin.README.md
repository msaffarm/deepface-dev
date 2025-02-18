# Building the docker image
```bash
docker build -f devgpu.Dockerfile -t deepface:gpu .
```


# Extracting faces from a video file

1. Make sure to copy the video file (mp4 file) to [`data`](./data/) directory.

2. Run the following command to extract faces from the video file.
```bash
docker run -it --rm --gpus all -v $PWD:/app deepface:gpu python /app/process_video.py --video_path /app/data/<your_video.mp4> --downsampling_rate 1
```

3. You can see the results created in a directory `/app/data/processed_video_retinaface` director inside [`data`](./data/) directory.


Example run with the sample video file in data directory:

```bash
docker run -it --rm --gpus all -v $PWD:/app deepface:gpu python /app/process_video.py --video_path /app/data/first_10_seconds.mp4 --downsampling_rate 2
```
