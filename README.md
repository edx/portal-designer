# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/edx/portal-designer/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                           |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| designer/\_\_init\_\_.py                                                       |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/\_\_init\_\_.py                                                  |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/\_\_init\_\_.py                                              |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/tests/\_\_init\_\_.py                                        |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/urls.py                                                      |        3 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/v1/\_\_init\_\_.py                                           |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/v1/serializers.py                                            |       59 |        2 |       18 |        4 |     92% |53->57, 57->61, 62, 138 |
| designer/apps/api/v1/test\_pages\_api.py                                       |      105 |        1 |       48 |        4 |     97% |75->79, 79->83, 84, 108->100 |
| designer/apps/api/v1/tests/\_\_init\_\_.py                                     |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/v1/urls.py                                                   |        3 |        0 |        0 |        0 |    100% |           |
| designer/apps/api/v1/views.py                                                  |       78 |       29 |       20 |        2 |     62% |38-39, 42, 47-50, 71-76, 129-153, 158-161 |
| designer/apps/branding/\_\_init\_\_.py                                         |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/migrations/0001\_initial.py                             |        7 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/migrations/0002\_auto\_20190703\_1512.py                |        5 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/migrations/0003\_remove\_cover\_texture\_image.py       |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/migrations/\_\_init\_\_.py                              |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/models.py                                               |        9 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/tests/\_\_init\_\_.py                                   |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/branding/tests/utils.py                                          |       15 |        0 |        4 |        0 |    100% |           |
| designer/apps/branding/utils.py                                                |        5 |        1 |        2 |        1 |     71% |        18 |
| designer/apps/core/\_\_init\_\_.py                                             |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/apps.py                                                     |        5 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/constants.py                                                |        3 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/context\_processors.py                                      |        3 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/management/commands/create\_program.py                      |       32 |        2 |        2 |        0 |     94% |     73-74 |
| designer/apps/core/management/commands/tests/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/management/commands/tests/test\_create\_program.py          |       31 |        0 |        4 |        0 |    100% |           |
| designer/apps/core/migrations/0001\_initial.py                                 |        8 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/migrations/0002\_auto\_20190819\_1515.py                    |       13 |        2 |        0 |        0 |     85% |     13-14 |
| designer/apps/core/migrations/0003\_last\_name\_max\_length\_150.py            |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/migrations/0004\_alter\_user\_first\_name.py                |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/migrations/\_\_init\_\_.py                                  |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/models.py                                                   |       17 |        0 |        2 |        0 |    100% |           |
| designer/apps/core/signals.py                                                  |       11 |        0 |        6 |        0 |    100% |           |
| designer/apps/core/tests/\_\_init\_\_.py                                       |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/tests/test\_context\_processors.py                          |        8 |        0 |        2 |        0 |    100% |           |
| designer/apps/core/tests/test\_models.py                                       |       30 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/tests/test\_signals.py                                      |       24 |        0 |        0 |        0 |    100% |           |
| designer/apps/core/tests/test\_views.py                                        |       32 |        0 |        4 |        0 |    100% |           |
| designer/apps/core/tests/utils.py                                              |       60 |        0 |       34 |        0 |    100% |           |
| designer/apps/core/views.py                                                    |       41 |        6 |        8 |        1 |     82% |43-44, 58, 96-98 |
| designer/apps/core/wagtailadmin/views.py                                       |       27 |       15 |        6 |        0 |     36% |19-21, 27-48 |
| designer/apps/pages/\_\_init\_\_.py                                            |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/apps.py                                                    |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0001\_initial.py                                |        7 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0002\_programpage.py                            |        6 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0003\_programpage\_uuid.py                      |        5 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0004\_auto\_20190613\_1955.py                   |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0005\_auto\_20190701\_1719.py                   |        6 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0006\_auto\_20190702\_1505.py                   |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0007\_auto\_20190703\_2043.py                   |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0008\_auto\_20190708\_1743.py                   |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0009\_programpage\_program\_documents.py        |        7 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0010\_programpage\_idp\_slug.py                 |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0011\_auto\_20190716\_2048.py                   |        9 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0012\_externalprogramwebsite.py                 |        7 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0013\_remove\_programpage\_idp\_slug.py         |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0014\_enterprisepage\_enterprisepagebranding.py |        6 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0015\_enterprisepage\_contact\_email.py         |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0016\_add\_page\_specific\_branding.py          |        6 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/0017\_copy\_existing\_program\_branding.py      |       15 |        6 |        2 |        1 |     59% | 10-14, 17 |
| designer/apps/pages/migrations/0018\_rename\_cover\_texture\_image\_fields.py  |        4 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/migrations/\_\_init\_\_.py                                 |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/models.py                                                  |       64 |        0 |        6 |        0 |    100% |           |
| designer/apps/pages/tests/\_\_init\_\_.py                                      |        0 |        0 |        0 |        0 |    100% |           |
| designer/apps/pages/tests/test\_create\_pages.py                               |      117 |       10 |       22 |        4 |     87% |140->145, 152->154, 162-172, 176-177, 186->188, 199 |
| designer/apps/pages/tests/utils.py                                             |       63 |        0 |       32 |        3 |     97% |33->exit, 53->exit, 106->exit |
| designer/apps/pages/utils.py                                                   |        5 |        0 |        4 |        0 |    100% |           |
| designer/docker\_gunicorn\_configuration.py                                    |       22 |       22 |        8 |        0 |      0% |      4-74 |
| designer/rich\_text.py                                                         |       11 |        1 |        4 |        2 |     80% |17, 19->22 |
| designer/settings/\_\_init\_\_.py                                              |        0 |        0 |        0 |        0 |    100% |           |
| designer/settings/base.py                                                      |       69 |        0 |        6 |        1 |     99% | 210->exit |
| designer/settings/devstack.py                                                  |       16 |       16 |        0 |        0 |      0% |      1-40 |
| designer/settings/local.py                                                     |       18 |       18 |        6 |        0 |      0% |      1-73 |
| designer/settings/production.py                                                |       22 |       22 |        8 |        0 |      0% |      1-48 |
| designer/settings/test.py                                                      |        3 |        0 |        0 |        0 |    100% |           |
| designer/settings/utils.py                                                     |       23 |        7 |        4 |        2 |     67% |11-15, 34, 110 |
| designer/urls.py                                                               |       19 |        0 |        0 |        0 |    100% |           |
|                                                                      **TOTAL** | **1208** |  **160** |  **262** |   **25** | **85%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/edx/portal-designer/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/edx/portal-designer/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/edx/portal-designer/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/portal-designer/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fedx%2Fportal-designer%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/portal-designer/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.