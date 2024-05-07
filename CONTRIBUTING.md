# Contributing

Thanks for your interest in helping improve abtester! This
guide is for people who want to contribute code to the project. There are other
ways to contribute, such as [reporting a bug](https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20bug%20report%20title%20here&body=Your%20bug%20report%20description%20here)
or [requesting a feature](https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20feature%20request%20title%20here&body=Your%20feature%20request%20description%20here).
You can also just [ask a question](https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20question%20title%20here&body=Your%20question%20description%20here),
or join the discussions in the [community forum](https://discord.gg/RAt8XbRrKc).
Note that we have a [code of conduct](https://github.com/gabrieltempass/abtester/blob/main/CODE_OF_CONDUCT.md),
please follow it in all your interactions with the project.

## Before starting

If your contribution is more than a few lines of code, then prior to starting
to code on it please post in the respective issue saying you want to volunteer,
and then wait for a positive response. If there is no issue for it yet, create
it first. This helps make sure:

* Two people aren't working on the same thing
* This is something the project's maintainers believe should be implemented or
  fixed
* Any API, UI, or deeper architectural changes that need to be implemented have
  been fully thought through by the project's maintainers
* Your time is well spent!

## Style guide

We use [Black](https://black.vercel.app/?version=stable&state=_Td6WFoAAATm1rRGAgAhARYAAAB0L-Wj4ARsAnNdAD2IimZxl1N_WlkPinBFoXIfdFTaTVkGVeHShArYj9yPlDvwBA7LhGo8BvRQqDilPtgsfdKl-ha7EFp0Ma6lY_06IceKiVsJ3BpoICJM9wU1VJLD7l3qd5xTmo78LqThf9uibGWcWCD16LBOn0JK8rhhx_Gf2ClySDJtvm7zQJ1Z-Ipmv9D7I_zhjztfi2UTVsJp7917XToHBm2EoNZqyE8homtGskFIiif5EZthHQvvOj8S2gJx8_t_UpWp1ScpIsD_Xq83LX-B956I_EBIeNoGwZZPFC5zAIoMeiaC1jU-sdOHVucLJM_x-jkzMvK8Utdfvp9MMvKyTfb_BZoe0-FAc2ZVlXEpwYgJVAGdCXv3lQT4bpTXyBwDrDVrUeJDivSSwOvT8tlnuMrXoD1Sk2NZB5SHyNmZsfyAEqLALbUnhkX8hbt5U2yNQRDf1LQhuUIOii6k6H9wnDNRnBiQHUfzKfW1CLiThnuVFjlCxQhJ60u67n3EK38XxHkQdOocJXpBNO51E4-f9z2hj0EDTu_ScuqOiC9cI8qJ4grSZIOnnQLv9WPvmCzx5zib3JacesIxMVvZNQiljq_gL7udm1yeXQjENOrBWbfBEkv1P4izWeAysoJgZUhtZFwKFdoCGt2TXe3xQ-wVZFS5KoMPhGFDZGPKzpK15caQOnWobOHLKaL8eFA-qI44qZrMQ7sSLn04bYeenNR2Vxz7hvK0lJhkgKrpVfUnZrtF-e-ubeeUCThWus4jZbKlFBe2Kroz90Elij_UZBMFCcFo0CfIm75UxzLdMMp-XXRCzahizn0Ex32wRFDOpjVE9rszhHWIRPMyyAAArN1JGAnzo0EAAY8F7QgAAP01Vc6xxGf7AgAAAAAEWVo=),
with a line length of 80 characters, to format the code. Besides that,
[Streamlit's oficial style guide](https://github.com/streamlit/streamlit/wiki/Style-Guide)
is followed throughout the project. 

## Development

Ensure you have [Python 3.11+](https://www.python.org/downloads/) and
[Pipenv](https://pipenv.pypa.io/en/latest/installation.html) installed.

1. Fork [the repository](https://github.com/gabrieltempass/abtester)
via the user interface on GitHub and then do the following:

``` bash
git clone https://github.com/${YOUR_NAME}/abtester.git
```

``` bash
cd abtester
```

``` bash
git remote add remote https://github.com/gabrieltempass/abtester.git
git checkout develop
git submodule update --init
git checkout -b ${BRANCH_NAME}
```

2. Create the Python virtual environment, install the dependencies and activate it:

``` bash
pipenv install --dev
pipenv shell
```

3. Run the Streamlit app:
``` bash
streamlit run abtester.py
```

If all goes well, you should see something like this:

![Quickstart success](https://github.com/gabrieltempass/abtester/raw/main/images/development.png)

4. Modify the code and submit your pull request.
