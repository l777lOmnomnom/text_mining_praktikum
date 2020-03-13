# Text Mining - Near duplicate document detection

Goal of this project is to find near duplicates of html web pages inside a warc IO archive using different hashing algorithms and whilst probing the hashing algorithms.

## Getting Started

1. Enable the virtual environment in the projects root directory with:
```
. venv/bin/acrtivate
```

2. Create or choose a config (you can find example configs in "conf/". ) and start the main script with it a parameter:
```
python3 main.py -c path/to/config.conf
```

3. Find the results in the path specified in the config (run.output_dir)

### Prerequisites

If you want to get all dependencies use the pip requirements file in the projects root directory:
```
pip3 install -r pip_requirements.txt
```

## Running the tests

There is a test script with a smaller subset of data contained in "test/".
```
python3 test.py
```

## Authors

* **Alexander Krebs**
* **Robby Wagner**
* **Tim**
* **Justus**
* **Andre**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

