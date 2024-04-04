### Table of contents
- [About](#About) 
- [Requirements](#requirements)
- [Architecture](#architecture)
- [How it works](#how-it-works)
- [Example](#example)
- [setup-script](#setup-script)
## About
This tool leverages the Elixir Bootlin API and its project indexing capabilities. Its user-friendly nature sets it apart, allowing it to analyze multiple local or remote repositories. It extracts any API calls for user-specific indexed repositories and presents them in a readable JSON format. It also identifies the programming language used (C/C++), conducts lexical analysis on the source code, identifies functions, and retrieves them from the indexed database via the Elixir Bootlin API. This amalgamation of features aims to offer users a straightforward and comprehensible experience.

It relies on Elixir's straightforward modular architecture, enabling support for new source code projects.  Elixir supports any C/C++ project as long as:
- Project sources are available in a Git repository
- All project releases are associated with a specific Git tag, as Elixir only considers such tags.

Note: Currently, the only supported languages are C and C++.

## Requirements
- Python 3.0 +
- ```pip install -r ./requirements.txt```

## Architecture 
                                                .---------------.----------------.
                                                |           CLI tool             |
                                                |---------------|----------------.
                                                | Query API call| Query Syscall  |
                                                |---------------|----------------|
                                                |           Python script        |
                                                ----------------------------------
      
## How it works
![pptF9C2 pptm  -  AutoRecovered](https://github.com/SamNour/api-syscalls-analyser/assets/96638051/851f92c2-6118-4677-84d2-4f941f76c861)
  
## Example
![ezgif-3-ade8c57462](https://github.com/SamNour/api-syscalls-analyser/assets/96638051/1a1b4b89-4ad8-48ec-b6e2-fa5d05b16b83)

## setup-script
- ```$ ./setup.sh <URL of the repo to be indexed>```
- You should open the setup.sh script to only make minor changes to the paths based on your preferences

## Output files
- User specifies the output directory containing the output for each specific repo analyzed.
- ```
  repo_1-glibc
  |
  |-
  repo-1-linux
  repo_2-linux
  ...
  ```

### api_filter.json
- This file will contact all the extracted API calls according to the respective repository.
```yaml
{
"__kfree_skb": [
"prototype",
"function"
],
"ei_tx_timeout": [
"prototype",
"function"
],
"posix_lock_file": [
"prototype",
"function"
],
"dev_close": [
"prototype",
"member",
"function"
],
"dev_load": [
"prototype",
"function"
],
"skb_queue_head": [
 "prototype",
 "function"
 ]
 }
```

### api_filter.json


