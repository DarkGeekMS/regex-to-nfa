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
