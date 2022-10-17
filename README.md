# STG DjangoCon US 2022 Challenge

### Introduction

Welcome, Challenger!
Summit Technology Group (STG) is hosting a challenge for all Django Jedi Masters at Djangocon US 2022. Please see the below challenges for basic requirements and judging criteria. We will be choosing the best submission on the specified date with the grand prize being a new Oculus VR headset.

This website is a mock Spotify-Clone platform that is non-customer facing. It is currently under development but it will be used for internal metrics and business insights by backoffice users! Your help is needed in creating a dashboard!

### Challenge: Metrics Dashboard

1. Create a dashboard using the provided models and dummy data:
   - Detailed breakdown per Genre (# of Artists, # of Songs, # of Albums, etc.)
   - Detailed song breakdown (# of Songs per Artist, Average length of song, etc.)
   - Top 10 Artists by Monthly Listeners
   - Add up your queries in the provided dashboard view and hook it up with your preferred charting library
     - Chart.js is included already for your convenience (but any will work!)
1. Ensure the queries are as performant as possible. We will be judging on performance!

#### Deadline: Midnight PST 10/18/2022

_NOTE:_ [Chart.js](https://www.chartjs.org/) has been provided in the templates already for ease of use but any charting package of your preference is welcome. In addition to that, [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) has already been installed and is ready for use so you can fine-tune all of your queries.

### Getting Started

1. install docker / docker-compose
1. fork repo and clone locally
1. `make build`
1. `make run`
1. navigate to `localhost:8000`
   - django admin login: `admin / admin`

### Submission

When finished, please create a pull request from your fork. We will judge all submissions on the following criteria:

1. minimum requirements met
2. performance
3. submitted before the deadline

### Resources

- [GitHub Repo](https://github.com/Lenders-Cooperative/stg-spotify-clone)
- [Official Django Docs](https://docs.djangoproject.com/en/4.1/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Chart.js](https://www.chartjs.org/)
- [Summit Technology Group (STG)](https://thesummitgrp.com/company/careers-index.html)
