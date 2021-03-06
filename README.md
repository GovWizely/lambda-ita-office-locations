[![CircleCI](https://circleci.com/gh/GovWizely/lambda-ita-office-locations/tree/master.svg?style=svg)](https://circleci.com/gh/GovWizely/lambda-ita-office-locations/tree/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/62f58865b96016ddca69/maintainability)](https://codeclimate.com/github/GovWizely/lambda-ita-office-locations/maintainability)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=GovWizely/lambda-ita-office-locations)](https://dependabot.com)

# ITA Office Locations Lambda

This project provides an AWS Lambda that creates a single JSON document from the two XML endpoints http://emenuapps.ita.doc.gov/ePublic/GetPost?type=oio and http://emenuapps.ita.doc.gov/ePublic/GetPost?type=odo.
It uploads that JSON file to a S3 bucket.

## Prerequisites

- This project is tested against Python 3.7+ in [CircleCI](https://app.circleci.com/github/GovWizely/lambda-ita-office-locations/pipelines).

## Getting Started

	git clone git@github.com:GovWizely/lambda-ita-office-locations.git
	cd lambda-ita-office-locations
	mkvirtualenv -p /usr/local/bin/python3.8 -r requirements-test.txt lambda-ita-office-locations

If you are using PyCharm, make sure you enable code compatibility inspections for Python 3.7/3.8.

### Tests

```bash
python -m pytest
```

## Configuration

* Define AWS credentials in either `config.yaml` or in the [default] section of `~/.aws/credentials`. To use another profile, you can do something like `export AWS_DEFAULT_PROFILE=govwizely`.
* Edit `config.yaml` if you want to specify a different AWS region, role, and so on.
* Make sure you do not commit the AWS credentials to version control.

## Invocation

	lambda invoke -v
 
## Deploy
    
To deploy:

	lambda deploy --requirements requirements.txt
