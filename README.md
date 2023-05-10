# Backend Coding Challenge

The first thing is to welcome you to this test, congratulations for successfully passing the previous steps, thank you
for the time invested in the process and of course good luck.

At Idoven we have a need, we want to set up a microservice that receives electrocardiograms (ECG) and returns a series
of information about them, for example, calculating the number of zero crossings of the signal.

An ECG is represented by a series of numerical values that can be either positive or negative.

The idea is to set up an API that acts as a service and with two endpoints, one to receive the ECGs to be processed and
another where we return information.

ECGs have this structure:

```
- id: unique identifier for each ECG
- date: creation date
- leads: list of:
  - name: lead identifier (for example: I, II, III, aVR, aVL and aVF, V1, V2…)
  - number of samples: sample size of the signal, this value does not always come
  - signal: list of integer values
```

The information that the endpoint must return will be the number of times that each of the ECG channels passes through
zero. For now we do not need more information.

Freedom is given to use language, technologies, frameworks, documentation, tests... We currently use Python 3.10.9,
FastAPI, JIRA, GitHub.

It must be taken into account that this service is going to scale, and more functionalities are going to be added to it
and the endpoint of obtaining information about an ECG is going to calculate more data.

In addition, we are thinking of opening this service to external clients, so we are considering using a user
authentication system for both endpoints. And with the necessary security to only be able to access the ECGs created by
yourself.
And it would be nice to have an ADMIN role that is in charge of registering new users. This user would not have access
to send or obtain information about the ECGs.

The test solution must be posted on this repository like a pull request.
