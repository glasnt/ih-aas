# [`ih`](https://github.com/glasnt/ih), as a service. 

This code deploys [`ih`](https://github.com/glasnt/ih), as a Cloud Run service. 

## Want to deploy your own? 

[![Run on Google Cloud](https://storage.googleapis.com/cloudrun/button.svg)](https://deploy.cloud.run)

## Local Usage

```shell
git clone https://github.com/glasnt/ih-aas
cd ih-aas
```
Then either:

```
python app.py
```

or

```shell
docker build --no-cache -t ih-aas . && docker run --rm -p 8080:8080 ih-aas
```


## curl 

```
curl -F 'image=@/path/to/image.png' http://localhost:8080 -F 'palette=lego' -F 'render=True'
```
