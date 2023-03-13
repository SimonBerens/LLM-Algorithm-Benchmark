# LLM Algorithmic Thinking Benchmark

### About
I was curious how well LLMs could do "algorithmic thinking", i.e. how well they could reason about code.
One way of testing this is giving LLMs programs + inputs, and asking them to predict the outputs.

This repo provides a set of basic algorithms, data structures, and test inputs to run LLMs on.

The project also provides a simple and modular way to run these LLMs on the test cases and compare them against
what the code would actually output.

The /web directory contains the code for visualizing the result of running the default pipeline.

### Run locally
Install the python requirements with `pip install -r requirements.txt`.

To run the default pipeline, run `python run_default_pipeline.py`.

To run the web server, run `cd web && pnpm dev`.

To test the inputs, run `python validate_all_inputs.py`.


### Environment Variables
```bash
OPENAI_API_KEY
COHERE_API_KEY
```