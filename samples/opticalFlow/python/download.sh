#!/bin/bash
#
# Kiet To
# 2020-10-08

hash youtube-dl && \
    echo "youtube-dl found." || \
        pip install youtube_dl

URL="https://www.youtube.com/watch?v=iYsHmRytSUo"
# to check available quality and resolutions
#   youtube-dl -F "https://www.youtube.com/watch?v=iYsHmRytSUo"

[ -f output-1080p.mp4 ] && \
    echo "output-1080p.mp4 found." || \
        youtube-dl -f 137 --output "output-1080p.%(ext)s" "${URL}"
[ -f output-720p.mp4 ] && \
    echo "output-720p.mp4 found." || \
        youtube-dl -f 136 --output "output-720p.%(ext)s" "${URL}"
[ -f output-480p.mp4 ] && \
    echo "output-480p.mp4 found." || \
        youtube-dl -f 135 --output "output-480p.%(ext)s" "${URL}"
