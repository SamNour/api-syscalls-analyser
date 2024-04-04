### Table of contents
- [About](#about) 
- [Requirements](#requirements)
- [Architecture](#abstract-architecture)
- [How it works](#how-it-works)
- [Example](#example)
- [Setup-script](#setup-script)
- [run-script](#run-script)
- [Output files](#output-files)
  - [filtered_api_calls.json](#filtered_api_callsjson)
  - [system_calls_per_repo.txt](#system_calls_per_repotxt)
  - [syscalls_per_file_output_repos.txt](#syscalls_per_file_output_repostxt)
- [Help](#help)
## About
### System calls
- This tool is capable of extracting all the system calls for i386 arch from the repositories in a recursive manner; the references for the i386 calls are extracted from [strace syscallent.h](https://gitlab.com/strace/strace/-/blob/master/src/linux/i386/syscallent.h?ref_type=heads)
### API calls
- This tool leverages the Elixir Bootlin API and its project indexing capabilities. Its user-friendly nature sets it apart, allowing it to analyze multiple local or remote repositories. It extracts any API calls for user-specific indexed repositories and presents them in a readable JSON format. It also identifies the programming language used (C/C++), conducts lexical analysis on the source code, identifies functions, and retrieves them from the indexed database. 

- Currently, by using the ./setup.sh <git URL>, the tool is able to create the indexed database for any specified project, as long as:
  - Project sources are available in a Git repository
  - All project releases are associated with a specific **Git tag**.

Note: Currently, the only supported languages are C and C++.

## Requirements
- Python 3.0 +
- ```pip install -r ./requirements.txt```

## Abstract Architecture 
                                                .---------------.----------------.
                                                |           CLI tool             |
                                                |---------------|----------------.
                                                | Query API call| Query Syscall  |
                                                |---------------|----------------|
                                                |           Python script        |
                                                ----------------------------------
### Querying system calls - Component Diagram.
Below is a Component Diagram showing the main components of the tool in a very abstract manner. 
<div style="text-align:center;">
    <img src="https://github.com/SamNour/api-syscalls-analyser/assets/96638051/2dead32c-b9e5-4ebc-97ce-ebdcf380ad1d" alt="Selection_025" width="300">
</div>

      
## How it works
![pptF9C2 pptm  -  AutoRecovered](https://github.com/SamNour/api-syscalls-analyser/assets/96638051/851f92c2-6118-4677-84d2-4f941f76c861)
  
## Example
![ezgif-3-ade8c57462](https://github.com/SamNour/api-syscalls-analyser/assets/96638051/1a1b4b89-4ad8-48ec-b6e2-fa5d05b16b83)

## setup-script
- ```$ ./setup.sh <URL of the repo to be indexed>```
- You should open the setup.sh script to only make minor changes to the paths based on your preferences

  ```sh
  echo "Please enter the repo URL!"
  read URL
  url="https://github.com/SamNour/TUMbot.git"
  base_name=$(basename "$url" .git)
  echo $base_name
  git clone --bare $URL /home/location/usr/git/$base_name.git
  mkdir -p /home/location/elixir-data/projects/$base_name/data
  ln -s /home/location/usr/git/$base_name.git /home/location/elixir-data/projects/$base_name/repo
  python3 /home/bsp_projects/elixir/update.py 12  --  "12 - are the number of specified cores needed for indexing the DB"
  ```
## run-script
```
    ./query_sys.py  \
        --output=./output-$libname \
        --mrepo=$path \
        --compiler=/usr/include/ \
        --api \
        --sys \
        --version=$version
```
## Help
```$ ./query_sys.py -h```
<div style="text-align:center;">
    <img src="https://github.com/SamNour/api-syscalls-analyser/assets/96638051/05391cac-dfe5-4719-9860-521ae80c2bc8" alt="Selection_037" width="500">
</div>

## Output files
- The following section shows briefly how the analysis output should be represented
- User specifies the output directory containing the output for each specific repo analyzed.
- ```
  repo_1-glibc
  |
  |-
  repo-1-linux
  repo_2-linux
  ...
  ```

### filtered_api_calls.json
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

### system_calls_per_repo.txt
```

#############################################
System calls found in the ./directories/<repos directory>/startup.c
#############################################
 
{'exit',
 'ftruncate',
 'geteuid',
 'getpid',
 'getppid',
 'shutdown',
 'umask',
 'unlink'}
```


### syscalls_per_file_output_repos.txt

```
{'unlink is found in file ./directories/repos/ptpd/src/dep/startup.c': {634: 'unlink(rtOpts.lockFile);',
                                                                        642: 'unlink(rtOpts.statusLog.logPath);'},
 'unlink is found in file ./directories/repos/ptpd/src/dep/sys.c': {535: 'unlink(handler->logPath);'}},
{},
{},
{},
{},
{'bind is found in file ./directories/repos/ptpd/src/dep/net.c': {1245: 'if '
                                                                        '(bind(netPath->eventSock, '
                                                                        '(struct '
                                                                        'sockaddr '
                                                                        '*)&addr,',
                                                                  1247: 'PERROR("failed '
                                                                        'to '
                                                                        'bind '
                                                                        'event '
                                                                        'socket");',
```
