# Create_python_distroless_image_with_bazel

This repository is used to create Distroless Docker connector images for one mind automatically using Bazel.

## Build

```bash
make build
```

## Push

```bash
make push
```

## Clean
```
make clean #remove temporary files
or
make clean_repo #remove files generated during the build
```