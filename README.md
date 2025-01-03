[![PyPI version](https://badge.fury.io/py/markdown-xblock.svg)](https://pypi.python.org/pypi/markdown-xblock)

# Markdown XBlock
### Based on the [HTML XBlock by OpenCraft](https://github.com/open-craft/xblock-html)

## Introduction
This XBlock allows course authors to create and edit course content in Markdown
and displays it as HTML.

## Installation with [Tutor](https://docs.tutor.edly.io)
You may install the markdown-xblock to your Tutor environment by adding it to the `OPENEDX_EXTRA_PIP_REQUIREMENTS` list in `config.yml`:
```
OPENEDX_EXTRA_PIP_REQUIREMENTS:
- markdown-xblock==2.1.0
```

Or, if you prefer to install directly from Git:
```
OPENEDX_EXTRA_PIP_REQUIREMENTS:
- git+https://github.com/citynetwork/markdown-xblock.git@v2.1.0
```
For additional information, please refer to the official [documentation](https://docs.tutor.edly.io/configuration.html#open-edx-customisation).

The minimum supported Python version is 3.8.

To enable this block, add `"markdown"` to the course's advanced module list. 
The option `Markdown` will appear in the advanced components.

Once you've added a new `Markdown` component to your course, you can also add custom CSS classes to the component
by selecting `EDIT`/`Settings` and adding to the `classes` list (Note: use double quotes `" "`). Example:
```
["custom-css-class-1", "custom-css-class-2"]
```

The `Markdown` block uses [markdown2](https://pypi.org/project/markdown2/) to translate the content into HTML, 
by default the following extras are included:

* "code-friendly"
* "fenced-code-blocks"
* "footnotes"
* "tables"
* "use-file-vars"

## Configuration
It is possible to configure more
[extras](https://github.com/trentm/python-markdown2/wiki/Extras), by
adding to the extras list under `"markdown"` key in `XBLOCK_SETTINGS`
in your [Tutor plugin](https://docs.tutor.edly.io/plugins/index.html) that patches `openedx-common-settings`

By default, the `safe_mode` for `markdown2` library is enabled and set
to `replace`, which means that writing inline HTML is not allowed and
if written, all tags will be replaced with `[HTML_REMOVED]`. You can
also set `safe_mode` to `escape`, which only replaces `<`, `>` and `&`
with `&lt;`, `&gt;` and `&amp;`. To disable safe mode altogether and
allow inline HTML, you'll need to set `safe_mode` to `False` or `None`
in `XBLOCK_SETTINGS`. Please note that setting `safe_mode` to the
empty string (`''`) *also* disables safe mode.

Example (YAML plugin):
```
name: markdown
version: 1.0.0
patches:
  openedx-common-settings: |
    XBLOCK_SETTINGS["markdown"] = {
        "extras": [
            "code-friendly",
            "fenced-code-blocks",
            "footnotes",
            "tables",
            "header-ids",
            "metadata",
            "pyshell",
            "smarty-pants",
            "strike",
            "target-blank-links",
            "use-file-vars",
            "wiki-tables",
            "tag-friendly"
        ],
        "safe_mode": "escape"
    }
```

## Usage notes

### Images

To include images in your markdown content, use the standard
Markdown inline image syntax. Your course images will normally live in
the `static/images` directory, relative to the root of your course, so
you would include an image like this:

```markdown
![alt text for example image](/static/images/example.png)
```

The XBlock will then mangle your image reference into a static asset
reference.

### Links

If Markdown XBlock content contains links to another course, and your
platform is configured with the XBlock's safe mode enabled, a link
like

```markdown
[link text](https://example.com/courses/course-v1:Org+Class+Version/about)
```

will, when rendered, turn its `+` characters into whitespace. That
isn't actually wrong, because both `+` and the `%20` escape sequence
in URLs are meant to represent whitespace, yet Open edX uses the `+`
character to mean something *other* than whitespace, and that's a bit
of a problem.

To preserve Open edX course URL references, please explicitly encode
the `+` character as `%2B`, like so:

```markdown
[link text](https://example.com/courses/course-v1:Org%2BClass%2BVersion/about)
```

## Development
If you'd like to develop on this repo in `Tutor`, follow the steps described in the
[documentation](https://docs.tutor.edly.io/tutorials/edx-platform.html#working-on-edx-platform-python-dependencies).


### Running tests
The testing framework is built on [tox](https://tox.readthedocs.io/en/latest/). After installing tox, you can run `tox` from your Git checkout of this repository.

To throw away and rebuild the testing environment, run:
```shell
$ tox -r
```
For running PEP-8 checks only:
```shell
$ tox -e flake8
```
