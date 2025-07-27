# Test Machine

Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]

# Version

```shell
brew install cmake cairo pkg-config
pip install manim==0.19.0
```

# Usage
```shell
# manim tutorials: https://docs.manim.community/en/stable/tutorials/index.html
manim -pql do.py SquareToCircle # output a directory named 'media/'
```
The structure of 'media/' is shown below. 
```
├── media
│   ├── images
│   │   └── do
│   └── videos
│       └── do
│           └── 480p15
│               ├── partial_movie_files
│               │   └── SquareToCircle
│               │       ├── 1185818338_250965708_223132457.mp4
│               │       ├── 624642324_1555521867_557880437.mp4
│               │       ├── 624642324_2071225070_557880437.mp4
│               │       └── partial_movie_file_list.txt
│               └── SquareToCircle.mp4
```
