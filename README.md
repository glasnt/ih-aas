# [`ih`](https://github.com/glasnt/ih), as a service. 

[![Run on Google Cloud](https://storage.googleapis.com/cloudrun/button.png)](https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&&cloudshell_git_repo=https://github.com/glasnt/ih-aas)


## Local Usage

```shell
git clone https://github.com/glasnt/ih-aas
cd ih-aas
```
Then either:

```
FLASK_DEBUG=1 python app.py
```

or

```shell
docker build --no-cache -t ih-aas . && docker run --rm -p 8080:8080 ih-aas
```

