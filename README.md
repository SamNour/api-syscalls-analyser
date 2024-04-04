### Table of contents
- [About](#About) 
- [Requirements](#requirements)
- [Architecture](#architecture)
- [How it works](#how-it-works)
- [Example](#example)
- 
### About
This tool leverages the Elixir Bootlin API and its project indexing capabilities. Its user-friendly nature sets it apart, allowing it to analyze multiple repositories, whether local or remote. It extracts Linux API calls and presents them in a readable JSON format. It also identifies the programming language used (C/C++), conducts lexical analysis on the source code, identifies functions, and retrieves them from the indexed database via the Elixir Bootlin API. This amalgamation of features aims to offer users a straightforward and comprehensible experience.

It relies on Elixir's straightforward modular architecture, enabling support for new source code projects.  Elixir supports any C/C++ project as long as:
- Project sources are available in a Git repository
- All project releases are associated with a specific Git tag, as Elixir only considers such tags.

Note: Currently, the only supported languages are C and C++.

### Requirements
- Python 3.0 +
- ```pip install -r ./requirements.txt```

### Architecture 
                                                .---------------.----------------.
                                                |           CLI tool             |
                                                |---------------|----------------.
                                                | Query API call| Query Syscall  |
                                                |---------------|----------------|
                                                |           Python script        |
                                                ----------------------------------
      
### How it works
- https://github.com/SamNour/api-syscalls-analyser/assets/96638051/61bb9a70-00a3-4686-9c86-66567840eca5

### Example
- https://github.com/SamNour/api-syscalls-analyser/assets/96638051/7778a3b3-74c2-49fa-9f69-d1dabe83d142


