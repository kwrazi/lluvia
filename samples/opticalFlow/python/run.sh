pushd $(git rev-parse --show-toplevel)
bazel build samples/opticalFlow:all
popd
LL_PATH=$(git rev-parse --show-toplevel) ./opticalFlow.py output-480p.mp4
