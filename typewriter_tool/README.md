# typewriter_tool
A command-line tool to help instructors track and prevent AI-written work in their classes.

## Installation

To install the typewriter_tool, run:

```bash
pip install -r requirements.txt
```

## Usage

### Tracking submissions

To track a submission, use the following command:

```bash
typewriter_tool track --submission-id <submission_id> --student-name <student_name>
```

Replace `<submission_id>` and `<student_name>` with the actual values.

### Preventing AI-written work

To prevent AI-written work, use the following command:

```bash
typewriter_tool prevent --assignment-id <assignment_id> --student-name <student_name>
```

Replace `<assignment_id>` and `<student_name>` with the actual values.

## Requirements

* Python 3.8+
* argparse
* requests

## Contributing

Contributions are welcome! Please submit pull requests to the main branch.

## License

This project is licensed under the MIT License. See LICENSE for details.