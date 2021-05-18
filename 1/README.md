# Regex-to-NFA Converter

## Usage

-   Install dependencies :
    ```bash
    pip install -r requirements.txt
    ```

-   Run tool :
    ```bash
    python convert.py "REGEX"
    ```
For example : `python convert.py "0(1+0)|0*"`

-   Output NFA and its directed graph will be exported to `out/` folder.

## Folder Structure

-   `src` folder : contains the source code of the converter :
    -   `build_nfa.py` : code for building _NFA_ from _Regex_.
    -   `visualize_nfa.py` : code for _NFA_ visualization.

-   `out` folder : contains the outputs.

-   `test_cases` folder : contains the results of the given test cases.

-   `convert.py` : main conveter driver.

-   `requirements.txt` : python dependencies.
