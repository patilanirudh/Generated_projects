# us-gpt-4-api-client
A CLI tool to query the GPT-4 API with a US-only service, providing access to AI-powered features without geographical restrictions.

## Getting Started

To use this tool, you'll need to install it via pip:

```bash
pip install -U git+https://github.com/your-repo/us-gpt-4-api-client.git
```

## Usage Examples

### Querying the API

You can query the GPT-4 API using the following command:

```bash
gpt4-api-client --prompt "What is the capital of France?"
```

This will return a response from the GPT-4 API.

### Customizing the Request

You can customize your request by adding additional parameters. For example, to set the maximum number of responses, you can use:

```bash
gpt4-api-client --max Responses 10 --prompt "What is the capital of France?"
```

This will return at most 10 responses from the GPT-4 API.

## Contributing

Contributions are welcome! Please submit a pull request with any changes or new features you'd like to add.