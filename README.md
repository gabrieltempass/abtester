[![Join the chat at https://gitter.im/ab-tester-app/community](https://badges.gitter.im/ab-tester-app/community.svg)](https://gitter.im/ab-tester-app/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# A/B Tester

A web application to help design and evaluate the results of A/B tests.

## Useful links

- A/B Tester: https://share.streamlit.io/gabrieltempass/ab-tester
- Get help: [https://gitter.im/ab-tester-app/community](https://gitter.im/ab-tester-app/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link)
- Report a bug: [https://github.com/gabrieltempass/ab-tester/issues/new](https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20issue%20title%20here&body=Your%20issue%20description%20here)

## How to run locally

1. Clone the git repository:

```
git clone git@github.com:gabrieltempass/ab-tester.git
```

2. Go to the project's directory.
3. Create the environment:

```
conda env create -f environment.yml
```

4. Activate the environment:

```
conda activate ab-tester
```

5. Run the application:

```
streamlit run streamlit_app.py
```