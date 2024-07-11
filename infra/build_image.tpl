cd ${source}
gcloud auth configure-docker ${location}-docker.pkg.dev
docker build --platform linux/amd64 -t ${image_tag} .
docker push ${image_tag}
