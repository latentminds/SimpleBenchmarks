# PsyLLiuM


## Inspiration

All of the members in our team are interested in the way LLM shape society, what it allows us to do but also who they left behind. We wanted to find a robust and simple way to make biaises easy to understand for the general public.

## What it does

Anyone can create their own little dataset in the form of a mutli-answer form and submit them to the platform. On the platform, each LLM has a dedicated page with the results to each form that has been submitted. You can also see the LLM replies in details.

We made a first study using synthetic data generated and thoughfully handpicked from GPT-4 on minority discriminations biaises. This dataset is two forms of 75 questions each evaluating discriminations in gender, race, social status, etc. It declines in two varations: obvious biases and more subtle ones.

## How we built it

We used the huggingface transformers library to run the models locally. The interface is made with streamlit.

## Challenges we ran into

We started on langchain to make the LLM answer our questions but sometimes it refused to reply. To solve this issue, we directly looked at the last layer of the neural net and extracted the logprobabilities to work around the alignment. This also has the added benefit to be deterministic and give a confidence score in each answer.

The first synthetic dataset we used was unperfect from the get go and we had to make some efforts to use better prompting and have a rigourous selection process of what we would keep.

## Accomplishments that we're proud of

We think that theses kinds accessible ways to access benchamrks are a necessity with more and more people from different backgrounds getting into AI.
What we learned

Low level manupilation of LLMs using pytorch and transformers. Build fast interfaces with StreamLit
What's next for PsyLLiuM: LLM biaises evaluation made simple

We would like to push the project further and publish this as a huggingface space where people will be able to upload their own eval data.
