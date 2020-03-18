# Text Mining - near duplicate document detection

Goal of this project is to find near duplicates of html web pages inside a warc IO archive using different hashing algorithms and measuring their time consumption.

## Getting Started

1. Enable the virtual environment in the projects root directory with:
```
. venv/bin/activate
```

2. Create or choose a config (you can find example configs in "conf/". ) and start the main script with it as parameter:
```
python3 main.py -c path/to/config.conf
```
(Don't forget to specify a valid warc.gz as source in the config file!)
3. Find the results in the path specified in the config (run.output_dir)

### Prerequisites

You need to have all dependencies available. Use a virtual environment or install them manually using the pip_requirements file in the projects root directoy:
```
python3 -m venv venv --no-site-packages && . venv/bin/activate && pip3 install -r pip_requirements.txt
```

## Authors

* **Alexander Krebs**
* **Robby Wagner**
* **Tim Wille**
* **Justus Stahlhelm**
* **Andre Soudah**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

