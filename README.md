# SpriteToCode

## About

SpriteToCode is a script to turn image data into code that can be
included in [Gamebuino Meta](https://gamebuino.com) projects.

It's a command line oriented script, written in Python 3.5+, with
automation in mind. It takes one or more images as input and writes
code following specified templates on the output.

## Usage

The script `codewriter.py` is called through a Python 3.5+ interpreter.
As of today, the script is only dependant on `Pillow`, see
`requirements.txt`.

### Script arguments

The script asks for the arguments:

```
usage: spritetocode.py [-h] [--to_palette] [--template_path TEMPLATE_PATH]
                       [--output_path OUTPUT_PATH] [--version]
                       file [file ...]

```

* `-h`: displays help
* `--to_palette`: forces palette usage. If the source image
was not in palette mode, it will use the **Gambuino Meta** palette
in the output data. If colors not in the palette are used, they will
be mapped to `Color.BLACK`.  
* `--template_path`: specifies the path where to find the templates.
The default value is `.` (current folder). A pair of template (.cpp/.h)
are present alongside the script.
* `--output`: specifies the output path, where the generated files will
be written. If the path doesn't exist, the script will try to create it.
* `--version`: writes the version on standard output.
* `file [file ...]`: one or more files to be converted.
See nomenclature below.

### Nomenclature

The input files that the script convert must follow a specific
nomenclature to allow easy configuration of the data.

The format is the following:

`{AssetName}_{Width}x{Height}_{fixed|loop frame}`

* `{AssetName}` gives a name to the asset. This name will be used by the
template and in the names of the output files.
* `{Width}` and `{Height}` give the **size** of a sprite (or frame) found in the
image (see below).
* `{fixed|loop frame}`: if `fixed` then the image describes one or several
sprites. If a number, it tells what is the frame loop (the speed of the
animation), turning the image into an animation.

### Multiple sprites

The script will convert sprite atlas to the **Gamebuino Meta** expected
format, where all the sprites are in a column one sprite wide. Thus,
it allows to work on textures that are rectangular, several sprite wide.

Example for a picture containing four 8x8 sprites:

```
Source layout, picture is 16px x 16px.

+---+---+
| 0 | 2 |
+---+---+
| 1 | 3 |
+---+---+
``` 

```
Output layout, picture is 8px x 32px.

+---+
| 0 |
+---+
| 1 |
+---+
| 2 |
+---+
| 3 |
+---+
``` 

## Limitations / To Do

* There is no support for transparent color yet.
* The script only outputs 8 bit data at the moment (Mode 1).
* The indentation handling on the data payload in output files can be
improved (it is fixed to 4, not following the indentation of the template).

